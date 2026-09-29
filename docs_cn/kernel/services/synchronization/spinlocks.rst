.. _spinlocks:

自旋锁
#########

.. contents::
  :local:
  :depth: 2

自旋锁是 Zephyr 中最低级别的互斥原语。
它保护一个短暂的关键区，
使任一时刻只有一个执行上下文能访问一个共享资源。
发现锁已被持有的上下文会"自旋"，
忙等待直到锁变为可用，
而不是阻塞并让出 CPU。
这就是自旋锁仅适用于短关键区的原因。

获取自旋锁还会在本地 CPU 上屏蔽中断，
持续时间为锁被持有的时长。
正是这一点使自旋锁可以安全地在
线程和中断处理程序之间共享：
当某上下文持有锁时，
同一 CPU 上的任何 ISR 都无法抢占它，
且没有其他 CPU 能获取同一把锁，
因此两者都无法在更新中途观察或
破坏受保护的数据。
出于这些原因，:c:struct:`k_spinlock` 是
Zephyr 内核自身内部使用的主要
同步原语，
保护对其核心数据结构的访问。

应用代码也可以直接使用它，
但通常建议改用更高
级别的同步原语，
如 :c:struct:`k_mutex` 或 :c:struct:`k_sem`。

用法
*****

为每个需要保护的独立资源
声明一个 :c:struct:`k_spinlock`。
用 :c:func:`k_spin_lock` 获取它，
它返回一个 :c:type:`k_spinlock_key_t`，
必须将其传回
:c:func:`k_spin_unlock` 以释放锁：

.. code-block:: c

   static struct k_spinlock lock;

   void update_shared_state(void)
   {
           k_spinlock_key_t key = k_spin_lock(&lock);

           /* critical section: exclusive access */

           k_spin_unlock(&lock, key);
   }

:c:macro:`K_SPINLOCK` 辅助宏
在所包含代码块的持续时间内
获取锁，
并在退出代码块时自动释放它。

.. code-block:: c

       K_SPINLOCK(&lock) {
               /* critical section: exclusive access */
       }

代码块要么运行到其末尾，
要么用 :c:macro:`K_SPINLOCK_BREAK` 离开。
用普通的 ``break``、``goto`` 或 ``return``
离开会跳过释放并泄漏锁：

.. code-block:: c

   K_SPINLOCK(&lock) {
           if (nothing_to_do) {
                   K_SPINLOCK_BREAK;
           }

           /* critical section: exclusive access */
   }

无自旋获取
==========================

:c:func:`k_spin_trylock`
尝试获取锁一次，
失败时报告而不是等待，
这在调用者有其他工作要做
或不能停顿时很有用。
成功时它存储键，
释放方式与 :c:func:`k_spin_lock`
完全相同：

.. code-block:: c

   k_spinlock_key_t key;

   if (k_spin_trylock(&lock, &key) == 0) {
           /* critical section: exclusive access */
           k_spin_unlock(&lock, key);
   } else {
           /* lock is held elsewhere, do something else */
   }

规则
=====

使用自旋锁时请遵循以下规则：

* 将关键区保持尽可能短。
  持有锁期间本地 CPU 上的
  中断被屏蔽，
  且其他 CPU 可能正在其上自旋。
* 持有自旋锁期间
  永远不要执行阻塞或睡眠操作。
* 不要递归获取自旋锁。
  已持有锁的上下文
  不得尝试再次获取它，
  否则会死锁。
  嵌套**不同**的自旋锁
  是允许的，
  但必须遵循一致的
  锁顺序以避免死锁。

单处理器系统上的自旋锁
*********************************

在禁用 :kconfig:option:`CONFIG_SMP`
构建的内核中，
自旋锁实际上不会自旋。
只有一个 CPU 时没有可竞争的对象，
因此 :c:func:`k_spin_lock` 退化为
在本地 CPU 上屏蔽中断。
这阻止 ISR 和上下文切换
在更新中途观察受保护的数据，
这正是单处理器上互斥
所需的全部。

自旋锁验证
*******************

一个验证层（用 :kconfig:option:`CONFIG_SPIN_VALIDATE`
启用）可用于检测自旋锁的
各种误用。
它可以检测以下情况：

* 递归获取自旋锁
* 释放当前上下文未持有的自旋锁
* 乱序释放自旋锁
  （内部锁仍被持有时释放外部锁）
* 持有自旋锁期间上下文切换，
  或嵌套 :c:func:`irq_lock`
  屏蔽中断期间上下文切换

在单处理器系统上，
只有递归获取检查有意义。
其他误用不会发生，
因为没有竞争，
且持有锁期间中断被屏蔽。

公平自旋锁
******************

默认自旋锁实现
基于单个 ``atomic_t`` 变量，
不保证竞争 CPU 之间的公平性：
一个 CPU 可能反复赢得竞争，
从而使其他 CPU 饥饿。
在这重要的地方，
启用 :kconfig:option:`CONFIG_TICKET_SPINLOCKS`
会切换到基于票据的实现，
以稍大的锁对象为代价，
按 FIFO 顺序
将被竞争的锁
授予请求的 CPU。

建议用法
******************

使用自旋锁保护一个短暂的关键区，
该关键区在线程和中断处理程序
之间共享，
或在 SMP 系统上的 CPU 之间共享。

当另一种原语更合适时
优先使用它：

* :c:struct:`k_mutex` 用于
  可能较长、可能阻塞或可能睡眠的
  关键区。
  只有线程能获取互斥锁。
* :c:struct:`k_sem` 用于
  上下文之间的信号传递，
  以及对资源池的计数访问。
* 当共享状态是一个
  可以用单个原子操作更新的字时，
  使用 :ref:`原子服务 <atomic_v2>`，
  此时不需要锁。

API 参考
******************

.. doxygengroup:: spinlock_apis
