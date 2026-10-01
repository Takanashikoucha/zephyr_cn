.. _bbram_api:

电池备份 RAM（BBRAM）
##########################

BBRAM API 允许访问该内存区域的独特属性。以下常见类型的 BBRAM 属性可通过此 API 轻松获取：

- IBBR（无效）状态 —— 检查 BBRAM 是否未损坏。
- VSBY（电压待机）状态 —— 检查 BBRAM 是否处于待机电压。
- VCC（活动供电）状态 —— 检查 BBRAM 是否处于正常供电。
- 容量 —— 获取 BBRAM 区域的大小（以字节为单位）。

除上述属性外，该 API 还通过 :c:func:`bbram_read` 和 :c:func:`bbram_write` 分别提供读取和写入该内存区域的手段。这两个函数预期仅在 BBRAM 处于有效状态且操作限定在内存区域内时才会成功。

API 参考
*************

.. doxygengroup:: bbram_interface
