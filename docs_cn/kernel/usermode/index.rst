.. _usermode_api:

User Mode
#########

Zephyr 提供了以缩减的权限级别（我们称之为用户模式）运行线程的能力。当前实现面向具有 MPU（内存保护单元）硬件的设备。

有关创建以用户模式运行的线程的详细信息，请参阅 :ref:`lifecycle_v2`。

.. toctree::
    :maxdepth: 2

    overview.rst
    memory_domain.rst
    kernelobjects.rst
    syscalls.rst
    mpu_stack_objects.rst
    mpu_userspace.rst
