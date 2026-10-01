.. _cs_trace_defmt:

ARM Coresight Trace Deformatter
###############################

Formatter 为将多个 trace streams（由 7 bit ID 指定）封装为
单个输出 stream 的方法。Formatter 用 16 byte frames（封装最多 15 bytes 的
data。例如（其被 ETR (Embedded Trace Router) 使用（其为 circular RAM
buffer（各种 trace streams 的 data 可存储于此。通常 tracing data
由 host 离线解码（但 deformatter 可在-chip 用于
application runtime 期间解码 data。

Usage
*****

Deformatter 用 user callback 初始化。Data 用
:c:func:`cs_trace_defmt_process` 以 16 bytes chunks 解码。每次 stream 变更或
到达 chunk 末尾时调用 callback。Callback 包含 stream ID 和
data。

API documentation
*****************

.. doxygengroup:: cs_trace_defmt
