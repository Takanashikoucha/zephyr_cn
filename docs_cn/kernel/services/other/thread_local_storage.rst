.. _thread_local_storage:

线程局部存储（TLS）
##########################

线程局部存储（TLS）允许按线程为单位分配变量。
这些变量存储在线程栈中，这意味着
每个线程都拥有这些变量自己的副本。

Zephyr 目前要求工具链支持 TLS。


配置
*************

要在 Zephyr 中启用线程局部存储，
需要启用 :kconfig:option:`CONFIG_THREAD_LOCAL_STORAGE`。
注意，如果架构或 SoC 未启用隐藏选项
:kconfig:option:`CONFIG_ARCH_HAS_THREAD_LOCAL_STORAGE`，
则该选项可能不可用，这意味着
架构或 SoC 没有支持线程局部存储
所需的代码，和/或工具链不支持 TLS。

:kconfig:option:`CONFIG_ERRNO_IN_TLS` 可以与
:kconfig:option:`CONFIG_ERRNO` 一起启用，
使变量 ``errno`` 成为线程局部
变量。这允许用户线程在不
发起系统调用的情况下访问 ``errno`` 的值。


声明和使用线程局部变量
******************************************

宏 ``Z_THREAD_LOCAL`` 可用于声明线程局部变量。

例如，在头文件中声明线程局部变量：

.. code-block:: c

   extern Z_THREAD_LOCAL int i;

并在源文件中声明实际变量：

.. code-block:: c

   Z_THREAD_LOCAL int i;

关键字 ``static`` 也可用于将变量限制在单个源文件内：

.. code-block:: c

   static Z_THREAD_LOCAL int j;

使用线程局部变量与其他变量相同，例如：

.. code-block:: c

   void testing(void) {
       i = 10;
   }
