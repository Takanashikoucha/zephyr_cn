.. _usermode_api:

用户模式
#########

Zephyr 提供了以缩减权限级别运行线程的能力，
我们称之为用户模式。当前实现
针对具有 MPU 硬件的设备设计。

有关创建以用户模式运行的线程的详细信息，
请参阅
:ref:`lifecycle_v2`。

.. toctree::
    :maxdepth: 2

    overview.rst
    memory_domain.rst
    kernelobjects.rst
    syscalls.rst
    mpu_stack_objects.rst
    mpu_userspace.rst
