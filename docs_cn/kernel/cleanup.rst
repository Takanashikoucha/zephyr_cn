.. _cleanup_api:

基于作用域的清理助手
###########################

.. contents::
    :local:
    :depth: 2

概述
********

清理助手 API（Cleanup Helper API）提供了一种机制，在变量离开作用域时自动执行资源清理。
这与 C++ 中的 RAII 或 Go 中的 defer 语句类似。借助编译器对 ``__cleanup`` 属性的支持，
该 API 通过确保清理代码自动执行，帮助防止资源泄漏并简化错误处理。

需要设置 :kconfig:option:`CONFIG_SCOPE_CLEANUP_HELPERS` 才能启用此功能，它特别适用于：

* 自动解锁互斥锁（mutex）和信号量（semaphore）
* 自动释放动态分配的内存
* 确保清理动作在所有代码路径（包括提前返回）上都会发生
* 减少样板式的清理代码

.. warning::

    清理机制使用 ``__cleanup`` 属性实现。
    如果工具链不支持该属性，则此 API 不可用。

    因此，此 API 仅面向用户应用，不用于内核本身或其他子系统。

核心概念
*************

清理 API 提供三个主要抽象：

作用域变量
================

作用域变量（scoped variable）定义一种带有自动初始化和退出行为的类型。
使用作用域变量类型声明的变量通过 init 函数初始化，并在离开作用域时
自动通过 exit 函数清理。

作用域守卫
================

作用域守卫（scoped guard）是专门的作用域变量，在初始化时自动获取锁或
资源，在离开作用域时释放它。该模式常与互斥锁、信号量和其他同步原语一起使用。

作用域延迟
================

作用域延迟（scoped defer）在变量离开作用域时执行指定的函数，
初始化时不获取任何东西。这与 Go 等语言中的 ``defer`` 语句类似。

定义作用域类型
*********************

自定义作用域变量
======================

使用 :c:macro:`SCOPE_VAR_DEFINE` 定义带有 init 和 exit 函数的自定义作用域变量类型：

.. code-block:: c

    static inline struct flash_area *flash_area_init(int area_id)
    {
        struct flash_area *fa;

        if (flash_area_open(area_id, &fa) < 0) {
            return NULL;
        }

        return fa;
    }

    static inline void flash_area_exit(struct flash_area *fa)
    {
        if (fa != NULL) {
            flash_area_close(fa);
        }
    }

    // Define the scoped variable type
    SCOPE_VAR_DEFINE(flash_area, struct flash_area *, flash_area_exit(_T),
                     flash_area_init(area_id), int area_id);

    static int some_function(void)
    {
        // Declare 'fa' with automatic cleanup
        scope_var(flash_area, fa)(PARTITION_ID(storage_partition));
        if (fa == NULL) {
            return -EINVAL;  // Exit function is still called
        }

        // Use fa normally
        printk("Has driver: %d\n", flash_area_has_driver(fa));

        // No need to manually close - exit function is called automatically
        return 0;
    }

exit 函数表达式中的 ``_T`` 变量包含正在被清理的变量的值。

作用域守卫
================

使用 :c:macro:`SCOPE_GUARD_DEFINE` 定义一个守卫，在初始化时获取锁，
在作用域退出时释放它：

.. code-block:: c

    // Example guard definition (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_GUARD_DEFINE(k_mutex, struct k_mutex *,
                       (void)k_mutex_lock(_T, K_FOREVER),
                       (void)k_mutex_unlock(_T));

    static K_MUTEX_DEFINE(lock);

    void critical_section(void)
    {
        scope_guard(k_mutex)(&lock);

        // Lock is held here
        // Perform critical operations

        // Lock is automatically released when guard goes out of scope
    }

块作用域守卫
==================

:c:macro:`scope_guard` 会持有守卫直到*外层*作用域结束，而
:c:macro:`scoped_guard` 将守卫绑定到紧随其后的花括号块，
在该块一退出就释放它。这使得短小的临界区更明确，并让锁对象紧邻其保护的代码：

.. code-block:: c

    static K_MUTEX_DEFINE(lock);

    void worker(void)
    {
        // ... work that does not need the lock ...

        scoped_guard(k_mutex, &lock) {
            // lock held only inside these braces
        }
        // lock released here

        // ... more work without the lock held ...
    }

该块恰好执行一次。无论从块中以任何方式退出（包括 ``break``、``return`` 和 ``goto``），
锁都会被释放。注意 ``continue`` 是离开该块（其行为类似 ``break``），而不是重新执行该块。

条件守卫
================

用 :c:macro:`SCOPE_GUARD_DEFINE` 定义的守卫总是获取锁（它们以
``K_FOREVER`` 阻塞）。要表达一个获取可能失败的守卫（例如非阻塞的
``K_NO_WAIT`` 尝试加锁），请配合 :c:macro:`scoped_cond_guard` 使用
:c:macro:`SCOPE_COND_GUARD_DEFINE`。获取表达式会按成功与否求值：
失败时守卫存储 ``NULL``，提供的失败语句被执行，该块被跳过。

.. code-block:: c

    // Example guard definition (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_COND_GUARD_DEFINE(k_mutex_try, struct k_mutex *,
                            k_mutex_lock(_T, K_NO_WAIT) == 0,
                            (void)k_mutex_unlock(_T));

    static K_MUTEX_DEFINE(lock);

    int try_critical_section(void)
    {
        scoped_cond_guard(k_mutex_try, return -EBUSY, &lock) {
            // runs only if the lock was acquired
            // released automatically when the block is exited
        }

        return 0;
    }

失败语句可以是任意语句，例如 ``break``、``return -EBUSY``，
或者用 ``{}`` 静默跳过该块。

作用域延迟
================

使用 :c:macro:`SCOPE_DEFER_DEFINE` 定义一个执行清理函数的 defer：

.. code-block:: c

    // Define a defer for a custom cleanup function
    static void cleanup_resources(void)
    {
        // Cleanup code here
    }

    SCOPE_DEFER_DEFINE(cleanup_resources);

    void some_function(void)
    {
        scope_defer(cleanup_resources)();

        // Do work...

        // cleanup_resources() is called automatically
    }

对于带参数的函数：

.. code-block:: c

    // Example deferred k_free (already provided by <zephyr/cleanup/kernel.h>)
    SCOPE_DEFER_DEFINE(k_free, void *);

    void allocate_and_use(void)
    {
        void *ptr = k_malloc(100);
        scope_defer(k_free)(ptr);

        // Use ptr...

        // k_free(ptr) is called automatically
    }

使用须知
***********

清理顺序
================

清理函数按声明的逆序（LIFO——后进先出）调用，这与资源的自然嵌套相符：

.. code-block:: c

    {
        scope_guard(k_mutex)(&lock);           // Acquired first
        void *ptr = k_malloc(100);
        scope_defer(k_free)(ptr);              // Registered second

        // Do work...

    }  // ptr is freed first, then mutex is unlocked

作用域规则
================

清理在变量离开作用域时发生，包括：

* 到达块的末尾
* 提前 return 语句
* 循环中的 break 或 continue
* 跳出作用域的 goto 语句

.. code-block:: c

    void example_with_early_exit(struct k_mutex *lock)
    {
        scope_guard(k_mutex)(lock);

        if (error_condition) {
            return;  // Guard cleanup happens here
        }

        // Normal path

    }  // Guard cleanup also happens here

API 参考
*************

.. doxygengroup:: cleanup_interface
