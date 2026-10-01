.. _usb_device_stack_api:

USB device stack API (deprecated)
#################################

API reference
*************

有两种传输 data 的方式（用 'low' level read/write API 或
'high' level transfer API。

Low level API
  向 host 传输 data 时（class driver 应调用 usb_write()。
  完成后将调用注册的 endpoint callback。发送
  另一 packet 前（class driver 应等待前一 write 完成。
  收到 data 时（调用注册的 endpoint callback。
  应用 usb_read() 检索收到的 data。
  对 CDC ACM sample driver（这通过 endpoint array (cdc_acm_ep_data) 中提到的
  OUT bulk endpoint handler
  (cdc_acm_bulk_out) 发生。

High level API
  usb_transfer method 可用于向/从 host 传输 data。
  Transfer API 将根据 endpoint max packet size 自动将
  data 传输拆分为一个或多个
  USB transaction(s)。Class driver
  无需实现 endpoint callback（且应将此 callback 设为
  通用 usb_transfer_ep_callback。

.. doxygengroup:: _usb_device_core_api
