.. _async_notification:

异步通知
##########################

Zephyr 的 API 通常包含 :ref:`api_term_async` 函数，其中操作被发起后，
应用需要在操作完成时收到通知，并知道该操作是否成功。
使用 :c:func:`k_poll` 通常是一个好方法，但某些应用架构可能更适合回调通知，
而启用时钟和电源轨等操作可能需要在内核函数可用之前调用，
因此可能需要忙等待完成。

该 API 旨在嵌入到特定子系统中，例如 :ref:`resource_mgmt_onoff`
以及其他支持异步事务的 API。子系统封装层负责从包含通知元素的请求中
提取操作特定的数据，并使用 API 所需的参数调用回调。

一个限制是该 API 不适用于 :ref:`syscalls`，因为：

* :c:struct:`sys_notify` 不是内核对象；
* 从用户空间复制通知内容会破坏实现函数中 :c:macro:`CONTAINER_OF` 的使用；
* 自旋等待和回调通知方法都无法从用户空间调用者接受。

当从用户模式线程发起的异步操作需要通知时，子系统或驱动应提供一个
使用 :c:struct:`k_poll_signal` 进行通知的 syscall API。

API 参考
*************

.. doxygengroup:: sys_notify_apis
