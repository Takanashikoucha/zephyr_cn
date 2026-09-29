.. _bbram_api:

Battery
Backed
RAM
（BBRAM）
##########################

BBRAM
APIs
允许
与
这
个
memory
region
的
独特
属性
交互。
以下
常见
类型
的
BBRAM
属性
可以
通过
这
个
API
轻松
访问：

- IBBR
  （invalid）
  state
  -
  检查
  BBRAM
  不
  是
  corrupt
  的。
- VSBY
  （voltage
  standby）
  state
  -
  检查
  BBRAM
  是否
  使用
  standby
  voltage。
- VCC
  （active
  power）
  state
  -
  检查
  BBRAM
  是否
  在
  normal
  power
  上。
- Size
  -
  获取
  BBRAM
  region
  的
  size
  （以
  bytes
  计）。

连同
这些，
API
提供
通过
:c:func:`bbram_read`
和
:c:func:`bbram_write`
分别
向
memory
region
读取
和
写入
的
手段。
两
个
函数
都
被
期望
只
在
BBRAM
处于
valid
state
且
operation
被
bound
到
memory
region
时
成功。

API
Reference
*************

.. doxygengroup::
   bbram_interface
