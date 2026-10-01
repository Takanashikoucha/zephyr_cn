.. _syscalls:

系统调用
##########

用户线程运行的权限集比超级用户线程少：
某些 CPU 指令不可使用，且只能访问内存映射的
有限部分。系统调用（可以）允许用户线程执行
对其不直接可用的操作。

在定义系统调用时，必须确保对 API 私有数据的
访问只通过系统调用接口进行。私有内核数据
绝不能直接暴露给用户模式线程。例如，
``k_queue`` API 被故意不暴露，因为它把队列的
簿记信息直接存储在队列缓冲区中，而这些缓冲区
从用户模式可见。

允许用户注册在超级用户模式下运行的回调函数的
API 绝不能暴露为系统调用。将这些 API 保留给
超级用户模式访问。

本节描述如何声明新的系统调用，并讨论与它们
相关的若干实现细节。

组件
**********

所有系统调用具有以下组件：

* 带 :c:macro:`__syscall` 前缀的 **C 原型**，用于该 API。
  它声明在 ``include/`` 下的某个头文件或另一个
  ``SYSCALL_INCLUDE_DIRS`` 目录中。此原型从不手动
  实现，而是由 :ref:`gen_syscalls.py` 脚本生成。
  生成的是一个内联函数：从超级用户模式调用时
  直接调用实现函数；从用户模式调用时则经过
  权限提升和验证步骤。

* **实现函数**，即系统调用的真正实现。
  如果从用户模式调用，实现函数可以假定
  所有传入参数都已被验证。

* **验证函数**，包装实现函数并对所有
  传入参数进行验证。

* **解包函数**，一个自动生成的处理函数，
  用户源代码必须包含它。

C 原型
***********

C 原型表示 API 从用户模式或超级用户模式
被调用的方式。例如，初始化信号量：

.. code-block:: c

    __syscall void k_sem_init(struct k_sem *sem, unsigned int initial_count,
                              unsigned int limit);

:c:macro:`__syscall` 属性非常特殊。对 C 编译器而言，
它只是展开为 'static inline'。但对构建后的
:ref:`parse_syscalls.py` 脚本而言，它表示该 API
是系统调用。:ref:`parse_syscalls.py` 脚本会对函数
原型进行解析，以确定其返回值和参数的数据类型，
并且存在一些限制：

* 数组参数必须以指针形式传入，不能以数组形式
  传入。例如，``int foo[]`` 或 ``int foo[12]``
  不允许，应改为 ``int *foo``。

* 函数指针会严重困扰有限的解析器。解决办法
  是先 typedef 函数指针，然后在参数列表中用
  该 typedef 表示。

* :c:macro:`__syscall` 必须是原型中的第一项。

在确定要生成的系统调用集合时，故意不使用
预处理器。但是，任何实际上没有定义验证函数的
生成的系统调用（因为相关特性未在内核配置中
启用），将指向未实现系统调用的特殊验证函数。
API 的数据类型定义对编译器不应有条件可见性。

声明系统调用的任何头文件必须在文件最底部包含
一个特殊生成的头文件。该头文件遵循命名约定
``syscalls/<头文件名>``。例如，在
:zephyr_file:`include/zephyr/drivers/sensor.h` 的底部：

.. code-block:: c

    #include <zephyr/syscalls/sensor.h>

C 原型函数必须声明在 CMake 变量
``SYSCALL_INCLUDE_DIRS`` 列出的目录之一中。
当设置了 ``CONFIG_APPLICATION_DEFINED_SYSCALL``
时，此列表始终包含 ``APPLICATION_SOURCE_DIR``；
当设置了 ``CONFIG_ZTEST`` 时包含
``${ZEPHYR_BASE}/subsys/testsuite/ztest/include``。
可以通过 CMake 命令行或在运行
``find_package(Zephyr ...)`` 之前执行的 CMake
代码向列表添加额外路径。``${ZEPHYR_BASE}/include``
始终会被扫描以查找潜在的系统调用原型。

注意并非所有系统调用都会包含在最终二进制文件中。
CMake 函数 ``zephyr_syscall_header`` 和
``zephyr_syscall_header_ifdef`` 用于指定哪些头文件
包含的系统调用原型必须存在于最终二进制文件中。
注意，CMake 变量 ``SYSCALL_INCLUDE_DIRS`` 列出的
目录中的头文件，其系统调用始终会存在于最终
二进制文件中。要强制所有系统调用都包含在最终
二进制文件中，请启用 :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`。

调用上下文
================

如果已知某个 C 文件内的所有代码都仅运行在
用户模式或仅运行在超级用户模式，那么使用
系统调用 API 的源代码可以变得更高效。系统会
查找宏 :c:macro:`__ZEPHYR_SUPERVISOR__` 或
:c:macro:`__ZEPHYR_USER__` 的定义，通常这些宏
会由构建系统添加到相关文件的编译器标志中。

* 如果未启用 :kconfig:option:`CONFIG_USERSPACE`，
  所有 API 都直接调用实现函数。

* 否则，默认情况是进行运行时检查，查看处理器
  当前是否运行在用户模式，然后相应地执行
  系统调用或直接调用实现函数。

* 如果定义了 :c:macro:`__ZEPHYR_SUPERVISOR__`，
  则假定所有代码都运行在超级用户模式，所有
  API 都直接调用实现函数。如果代码实际运行在
  用户模式，那么一旦尝试执行不允许的操作，
  就会立即触发 CPU 异常。

* 如果定义了 :c:macro:`__ZEPHYR_USER__`，则假定
  所有代码都运行在用户模式，系统调用无条件执行。

实现细节
====================

使用 :c:macro:`__syscall` 声明一个 API，会使
:ref:`gen_syscalls.py` 脚本在 C 文件和头文件中
生成一些代码，全部位于项目输出目录的
``include/generated/`` 下：

* 系统调用被添加到系统调用 ID 的枚举类型中，
  表达在 ``include/generated/zephyr/syscall_list.h``
  中。它是 API 名称的大写形式，前缀为
  ``K_SYSCALL_``。

* 在分派表 ``_k_syscall_table`` 中为该系统调用
  创建条目，表达在
  ``include/generated/zephyr/syscall_dispatch.c`` 中

  * 该表仅包含其对应原型在头文件中声明的
    系统调用（当启用
    :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS` 时）：

    * 由 CMake 函数 ``zephyr_syscall_header`` 和
      ``zephyr_syscall_header_ifdef`` 指定，或

    * 在 CMake 变量 ``SYSCALL_INCLUDE_DIRS``
      指定的目录下。

* 声明一个弱验证函数，它只是"未实现系统调用"
  验证函数的别名。这是必要的，因为真正的验证
  函数可能根据内核配置而构建或不构建。例如，
  如果用户线程调用了传感器子系统 API，但传感器
  子系统未启用，则会调用弱验证函数。

* 在 ``include/generated/zephyr/syscalls/<name>_mrsh.c``
  中定义解包函数

API 的函数体在生成的系统头文件中创建。以
:c:func:`k_sem_init()` 为例，该 API 声明在
:zephyr_file:`include/zephyr/kernel.h` 中。
在 :zephyr_file:`include/zephyr/kernel.h`
的底部是::

    #include <zephyr/syscalls/kernel.h>

在该头文件内部是 :c:func:`k_sem_init()` 的函数体::

    static inline void k_sem_init(struct k_sem * sem, unsigned int initial_count, unsigned int limit)
    {
    #ifdef CONFIG_USERSPACE
            if (z_syscall_trap()) {
                    arch_syscall_invoke3(*(uintptr_t *)&sem, *(uintptr_t *)&initial_count, *(uintptr_t *)&limit, K_SYSCALL_K_SEM_INIT);
                    return;
            }
            compiler_barrier();
    #endif
            z_impl_k_sem_init(sem, initial_count, limit);
    }

这会生成一个接受三个参数、返回值为 void 的
内联函数。根据上下文，它要么直接调用实现函数，
要么经过系统调用权限提升。实现函数的原型也会
自动生成。

最后一层是系统调用本身的调用。所有实现系统调用的
架构都必须实现七个内联函数
:c:func:`_arch_syscall_invoke0` 到
:c:func:`_arch_syscall_invoke6`。这些函数将参数
打包到指定的 CPU 寄存器中并执行必要的权限提升。
API 内联函数的参数在作为参数传递给系统调用之前，
会被 C 强制转换为 ``uintptr_t``，以匹配寄存器的大小。
上述规则的例外是在 32 位系统上传递 64 位参数，
此时 64 位参数会被拆分为低 32 位和高 32 位，
作为两个连续参数传递。
始终有一个 ``uintptr_t`` 类型的返回值，
如果不需要可以忽略。

.. figure:: syscall_flow.png
   :alt: 系统调用执行流程
   :width: 80%
   :align: center

   系统调用执行流程

某些系统调用可能有超过六个参数，但所有架构
通过寄存器传递的参数数量都限制为六个。
额外的参数需要通过源内存空间中的一个数组传递，
该数组在验证函数中必须被视为不可信内存。
这段代码（打包、解包和验证）会在上述存根和
解包函数中按需自动生成。

系统调用返回 ``uintptr_t`` 类型的值，
由包装器 C 强制转换为 API 原型声明的返回类型。
这意味着在 32 位系统上，64 位值可能无法
直接从系统调用返回到其包装器。
为解决该问题，自动生成的包装器函数在其栈上
定义一个 64 位中间变量（被视为**不可信**缓冲区），
并将指向该变量的指针作为最后一个参数传递给系统调用。
从系统调用返回时，写入该缓冲区的值将由包装器函数返回。
在能够直接返回 64 位值的 64 位系统上不存在该问题。

实现函数
***********************

实现函数是实际为 API 完成工作的函数。
Zephyr 通常很少或不做参数错误检查，
或者用断言进行这类检查。编写实现函数时，
参数验证是可选的，应使用断言完成。

所有实现函数必须遵循命名约定，即 API 名称
前加 ``z_impl_`` 前缀。实现函数可以声明在
与 API 相同的头文件中（作为 static inline 函数），
也可以声明在某个 C 文件中。实现函数不需要原型，
它们会自动生成。

验证函数
*********************

验证函数在用户线程执行系统调用时在内核侧运行。
当用户线程触发软件中断以提升到超级用户模式时，
通用系统调用入口点使用用户提供的系统调用 ID
查找该系统调用对应的解包函数并跳转到它，
进而调用验证函数。

验证函数和解包函数仅在从用户模式调用系统调用
API 时运行。如果 API 从超级用户模式调用，
则直接调用实现函数，没有软件陷阱。

验证函数的目的是验证所有传入的参数，包括：

* 提供的任何内核对象指针。例如，信号量 API
  必须确保传入的信号量对象是有效的信号量，
  且调用线程对它拥有权限。

* 从用户模式传入的任何内存缓冲区。必须检查
  调用线程对提供的缓冲区拥有读或写权限。

* 有效值范围有限的任何其他参数。

验证函数涉及大量样板代码，
:zephyr_file:`include/zephyr/internal/syscall_handler.h`
中的一些宏使其简化。验证函数应使用这些宏声明。

参数验证
================

存在若干用于验证参数的宏：

* :c:macro:`K_SYSCALL_OBJ()` 检查内存地址，
  断言它是预期类型的有效内核对象、
  调用线程对它拥有权限，且对象已初始化。

* :c:macro:`K_SYSCALL_OBJ_INIT()` 与
  :c:macro:`K_SYSCALL_OBJ()` 相同，区别在于
  提供的对象可以未初始化。这对对象初始化
  函数的验证函数很有用。

* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()` 与
  :c:macro:`K_SYSCALL_OBJ()` 相同，区别在于
  提供的对象必须未初始化。这不常用，
  目前仅用于 :c:func:`k_thread_create()`。

* :c:macro:`K_SYSCALL_MEMORY_READ()` 验证
  特定大小的内存缓冲区。调用线程必须对
  整个缓冲区拥有读权限。

* :c:macro:`K_SYSCALL_MEMORY_WRITE()` 与
  :c:macro:`K_SYSCALL_MEMORY_READ()` 相同，
  但调用线程还必须拥有写权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()` 验证
  一个数组，其总大小用元素数量和元素大小两个
  独立参数表示。该宏在计算总大小时正确处理
  乘法溢出。调用线程必须对总大小拥有读权限。

* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()` 与
  :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()` 相同，
  但调用线程还必须拥有写权限。

* :c:macro:`K_SYSCALL_VERIFY_MSG()` 对某个布尔
  表达式进行运行时检查，该表达式必须求值为真，
  否则检查失败。变体 :c:macro:`K_SYSCALL_VERIFY`
  不接受消息参数，而是在失败时打印被测试的
  表达式。后者只应用于最明显的测试。

* :c:macro:`K_SYSCALL_DRIVER_OP()` 在运行时检查
  驱动实例能否执行某个特定操作。虽然该宏可以
  单独使用，但它主要是为每个驱动子系统自动
  生成的宏的构建块。例如，要验证 GPIO 驱动，
  可以使用 :c:macro:`K_SYSCALL_DRIVER_GPIO()` 宏。

* :c:macro:`K_SYSCALL_SPECIFIC_DRIVER()` 是一个
  运行时检查，验证提供的指针是特定设备驱动的
  有效实例、调用线程对它拥有权限，且驱动已
  初始化。它通过检查存储在驱动实例内的 API
  结构指针并确保其匹配提供的值（应为特定驱动
  的 API 结构地址）来完成。

如果任何检查失败，这些宏将返回非零值。
宏 :c:macro:`K_OOPS()` 可用于触发内核 oops，
从而杀死调用线程。这样做而不是返回某个错误
条件，是为了保持从超级用户模式调用时 API 的
行为一致。

.. _syscall_verification:

验证函数定义
================

所有系统调用都分派到基于系统调用、
以 ``z_vrfy_`` 为前缀命名的验证函数。
它们的返回类型和参数类型与所包装的系统调用
完全相同。它们的任务是在验证所有参数之后
执行系统调用（通常通过调用实现函数）。

验证函数本身由自动生成的解包函数调用，
解包函数负责从架构层解包寄存器参数并将它们
转换为正确的类型。解包函数定义在一个头文件中，
该头文件必须从用户代码中包含，通常在翻译单元中
验证函数定义之后的某处（以便可以内联）。

例如：

.. code-block:: c

    static int z_vrfy_k_sem_take(struct k_sem *sem, int32_t timeout)
    {
        K_OOPS(K_SYSCALL_OBJ(sem, K_OBJ_SEM));
        return z_impl_k_sem_take(sem, timeout);
    }
    #include <zephyr/syscalls/k_sem_take_mrsh.c>


验证内存访问策略
===================================

按引用传递给系统调用的参数需要特殊处理，
因为这些参数的值可以被任何能访问该参数所指向
内存的用户线程随时修改。如果内核基于该内存的
内容做出任何逻辑决策，即使做了检查，这也可能
使内核暴露于攻击。这是一类被称为 TOCTOU
（检查时刻到使用时刻）的利用方式。

缓解这些攻击的正确做法是在验证函数中制作副本，
只对副本进行参数检查（用户线程永远无法访问副本）。
实现函数接收的是副本而不是用户发送的原始数据。
:c:func:`k_usermode_to_copy()` 和
:c:func:`k_usermode_from_copy()` API 就是为此目的而存在的。

从用户模式传入的 C 字符串需要类似的小心处理，
因为它们的长度无法预先知道，且必须在不读取
调用者可访问内存之外的情况下定位结尾的 ``NUL``
字符。:c:func:`k_usermode_string_copy()` 和
:c:func:`k_usermode_string_alloc_copy()` 辅助函数
会在使用前安全地验证并将用户提供的字符串复制到
内核控制的内存中。

有一个例外情况，针对仅用于提供内存区域的大数据
缓冲区：该区域要么只被写入，要么其内容从不用于
任何验证或控制流。本节稍后进一步讨论。

作为第一个示例，考虑一个用作某个整数值
输出参数的参数：


.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        int local_out_param;
        int ret;

        ret = z_impl_some_syscall(&local_out_param);
        K_OOPS(k_usermode_to_copy(out_param, &local_out_param, sizeof(*out_param)));
        return ret;
    }

这里我们在栈上分配了 ``local_out_param``，
将其地址传递给实现函数，然后用
:c:func:`k_usermode_to_copy()` 填充
调用者传入的内存。

可能会想做更简洁的事情：

.. code-block:: c

    int z_vrfy_some_syscall(int *out_param)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(out_param, sizeof(*out_param)));
        return z_impl_some_syscall(out_param);
    }

但是，如果实现函数的逻辑中对该内存有任何读取，
这样做就不安全。例如，它可能被用来存储某个
计数器值，而拥有该内存访问权限的用户线程
可以篡改它。对于小的整数值，最安全的做法
是像第一个示例那样做复制。

某些参数可能是输入/输出参数。例如，常见看到
这样的 API：传入一个指向某个 ``size_t`` 的指针
（表示最大允许大小），然后由实现函数更新它
以反映实际处理的字节数。这也应该使用栈上副本：

.. code-block:: c

    int z_vrfy_in_out_syscall(size_t *size_ptr)
    {
        size_t size;
        int ret;

        K_OOPS(k_usermode_from_copy(&size, size_ptr, sizeof(size);
        ret = z_impl_in_out_syscall(&size);
        K_OOPS(k_usermode_to_copy(size_ptr, &size, sizeof(size)));
        return ret;
    }

许多系统调用传入结构体，甚至是链式数据结构。
所有这些都应该复制。通常通过在栈上分配副本来完成：

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        ...
        struct bar *bar_left;
        struct bar *bar_right;
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar bar_right_copy;
        struct bar bar_left_copy;

        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));
        K_OOPS(k_usermode_from_copy(&bar_right_copy, foo_copy.bar_right,
                                sizeof(struct bar)));
        foo_copy.bar_right = &bar_right_copy;
        K_OOPS(k_usermode_from_copy(&bar_left_copy, foo_copy.bar_left,
                                sizeof(struct bar)));
        foo_copy.bar_left = &bar_left_copy;

        return z_impl_must_alloc(&foo_copy);
    }

在某些情况下，数据量在编译时未知或可能太大
而无法在栈上分配。在这种情况下，可能需要通过
:c:func:`z_thread_malloc()` 从调用者的资源池中
分配内存。这应始终视为最后手段。功能安全编程
指南强烈不推荐使用堆，且使用资源池这一事实
必须清楚地记录。任何分配问题都必须通过向调用者
返回 ``-ENOMEM`` 来报告。绝不应使用 ``K_OOPS()``
来验证资源分配是否成功。

.. code-block:: c

    struct bar {
        ...
    };

    struct foo {
        size_t count;
        struct bar *bar_list; /* size 为 count 的 struct bar 数组 */
    };

    int z_vrfy_must_alloc(struct foo *foo)
    {
        int ret;
        struct foo foo_copy;
        struct bar *bar_list_copy;
        size_t bar_list_bytes;

        /* 安全地将 foo 复制到 foo_copy */
        K_OOPS(k_usermode_from_copy(&foo_copy, foo, sizeof(*foo)));

        /* 在我们制作的副本中对 count 成员做边界检查 */
        if (foo_copy.count > 32) {
            return -EINVAL;
        }

        /* 为 bar_list 分配 RAM，替换 foo_copy 中的指针 */
        bar_list_bytes = foo_copy.count * sizeof(struct_bar);
        bar_list_copy = z_thread_malloc(bar_list_bytes);
        if (bar_list_copy == NULL) {
            return -ENOMEM;
        }
        K_OOPS(k_usermode_from_copy(bar_list_copy, foo_copy.bar_list,
                                bar_list_bytes));
        foo_copy.bar_list = bar_list_copy;

        ret = z_impl_must_alloc(&foo_copy);

        /* 内存使用完毕，释放并返回 */
        k_free(foo_copy.bar_list_copy);
        return ret;
    }

最后，必须考虑大数据缓冲区。这些代表用户内存的
区域，数据要么从中复制出来，要么复制进去。
允许将这些指针直接传递给实现函数。调用者对
缓冲区的访问仍必须用 ``K_SYSCALL_MEMORY`` API 验证。
需要满足以下约束：

 * 如果缓冲区被实现函数用于写入数据（例如从
   某个 MMIO 区域捕获的数据），实现函数必须
   只写入这些数据，绝不能读取它们。

 * 如果缓冲区被实现函数用于读取数据（例如要
   写入某个硬件目的地的内存块），这些数据
   必须不做任何处理地读取。不能根据数据缓冲区
   的内容实现任何条件逻辑。如果需要这样的逻辑，
   就必须制作副本。

 * 缓冲区必须只与调用同步使用。实现函数绝不能
   保存缓冲区地址并异步使用它，例如在中断触发时
   使用。

.. code-block:: c

    int z_vrfy_get_data_from_kernel(void *buf, size_t size)
    {
        K_OOPS(K_SYSCALL_MEMORY_WRITE(buf, size));
        return z_impl_get_data_from_kernel(buf, size);
    }

验证返回值策略
================================

验证系统调用时，需要注意哪些类型的验证失败
应该向调用者传播返回值，哪些应该直接调用
:c:macro:`K_OOPS()`（杀死调用线程）。当前约定如下：

#. 对于已定义但未编译的系统调用，对这些缺失
   系统调用的调用会被路由到
   :c:func:`handler_no_syscall()`，
   该函数调用 :c:macro:`K_OOPS()`。

#. ``K_SYSCALL_MEMORY`` API 集、
   :c:func:`k_usermode_from_copy()`、
   :c:func:`k_usermode_to_copy()` 发现的任何
   无效内存访问都应触发 :c:macro:`K_OOPS`。
   这发生在调用者对内存缓冲区没有适当权限
   或某个大小计算发生溢出时。

#. 大多数系统调用以内核对象指针作为参数，
   用 ``K_SYSCALL_OBJ`` 系列函数之一、
   ``K_SYSCALL_DRIVER_nnnnn`` 或手动使用
   :c:func:`k_object_validate()` 检查。
   这些可能因各种原因失败：缺少驱动 API、
   无效的内核对象指针、错误的内核对象类型
   或不正确的初始化状态。这些问题应始终
   调用 :c:macro:`K_OOPS()`。

#. 由内存堆分配失败（通常来自调用
   :c:func:`z_thread_malloc()`）导致的任何错误，
   应向调用者传播 ``-ENOMEM``。

#. 通用参数检查应在实现函数中完成，
   大多数情况下使用 ``CHECKIF()``。

    * ``CHECKIF()`` 的行为取决于内核配置，
      但如果启用了用户模式，则强制执行
      :kconfig:option:`CONFIG_RUNTIME_ERROR_CHECKS`，
      保证这些检查会被执行并传播返回值。

#. 严禁从用户模式注册任何类型的内核模式
   回调函数。仅安装回调的 API 不应暴露为
   系统调用。某些驱动子系统 API 可能接受
   可选的函数回调指针。这些 API 的用户模式
   验证函数必须强制这些指针为 NULL，
   否则应调用 :c:macro:`K_OOPS()`。

#. 某些参数检查仅在用户模式下强制执行。
   这些应在验证函数中检查，并在可能时
   向调用者传播返回值。

Zephyr 中目前存在以下这些策略的已知例外：

* :c:func:`k_thread_join()` 和
  :c:func:`k_thread_abort()` 在线程对象未初始化时
  是空操作。这是因为对于线程，初始化位身兼二职，
  用于指示线程是否正在运行（退出时清除）。
  参见 #23030。

* :c:func:`k_thread_create()` 对参数检查调用
  :c:macro:`K_OOPS()`，因为大量现有代码忽略
  其返回值。这也将由 #23030 处理。

* :c:func:`k_thread_abort()` 在关键线程被中止时
  调用 :c:macro:`K_OOPS()`，因为该函数没有返回值。

* 与日志记录相关的某些系统调用在传入错误
  参数时调用 :c:macro:`K_OOPS()`，
  因为它们不传播错误。

配置选项
*********************

相关配置选项：

* :kconfig:option:`CONFIG_USERSPACE`
* :kconfig:option:`CONFIG_EMIT_ALL_SYSCALLS`

API
****

创建系统调用验证函数的辅助宏在
:zephyr_file:`include/zephyr/internal/syscall_handler.h`
中提供：

* :c:macro:`K_SYSCALL_OBJ()`
* :c:macro:`K_SYSCALL_OBJ_INIT()`
* :c:macro:`K_SYSCALL_OBJ_NEVER_INIT()`
* :c:macro:`K_OOPS()`
* :c:macro:`K_SYSCALL_MEMORY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_WRITE()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_READ()`
* :c:macro:`K_SYSCALL_MEMORY_ARRAY_WRITE()`
* :c:macro:`K_SYSCALL_VERIFY_MSG()`
* :c:macro:`K_SYSCALL_VERIFY`

调用系统调用的函数在
:zephyr_file:`include/zephyr/syscall.h` 中定义：

* :c:func:`_arch_syscall_invoke0`
* :c:func:`_arch_syscall_invoke1`
* :c:func:`_arch_syscall_invoke2`
* :c:func:`_arch_syscall_invoke3`
* :c:func:`_arch_syscall_invoke4`
* :c:func:`_arch_syscall_invoke5`
* :c:func:`_arch_syscall_invoke6`
