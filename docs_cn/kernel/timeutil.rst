.. _timeutil_api:

时间工具
##############

概述
********

Zephyr 中的 :ref:`kernel_timing_uptime` 基于 tick 计数器。
使用默认的 :kconfig:option:`CONFIG_TICKLESS_KERNEL`，
此计数器从系统启动瞬间的零开始
以名义上恒定的速率推进。
此计数器的 POSIX 等效物
类似于 ``CLOCK_MONOTONIC``
或
在
Linux
中
的
``CLOCK_MONOTONIC_RAW``。
:c:func:`k_uptime_get()`
提供
此
时间
的
毫秒
表示。

应用
通常
需要
将
Zephyr
内部
时间
与
日常
生活
中
使用
的
外部
时间
尺度
关联，
例如
本地
时间
或
协调
世界时。
这些
系统
以
不同
方式
解释
时间，
且
可能
因
`leap seconds <https://what-if.xkcd.com/26/>`__
和
本地
时间
偏移
（如
夏令时）
而
存在
不
连续
性。

由于
这些
不
连续
性，
以及
周期
计数器
底层
时钟
的
显著
不
准确
性，
从
Zephyr
时钟
估计
的
时间
与
"真实"
民用
时间
尺度
中
的
实际
时间
之间
的
偏移
不
是
常数，
且
在
Zephyr
应用
的
运行
时间
内
可以
大幅
变化。

时间
工具
API
支持：

* :ref:`时间表示之间的转换 <timeutil_repr>`
* :ref:`时间尺度的同步和对齐 <timeutil_sync>`
* :ref:`表示的比较、加法和减法 <timeutil_manip>`

支持
这些
功能
的
术语
和
概念
请参阅
:ref:`timeutil_concepts`。

时间
工具
API
*****************

.. _timeutil_repr:

表示
转换
=============================

时间
尺度
瞬间
可以
用
多种
方式
表示，
包括：

* 自
  epoch
  以来
  的
  秒数。
  POSIX
  中
  此
  形式
  的
  时间
  表示
  包括
  ``time_t``
  和
  ``struct timespec``，
  通常
  被
  解释
  为
  "UNIX
  Time"
  的
  表示
  （请参阅
  :rfc:`8536#section-2`）。

* 自
  epoch
  以来
  的
  年、
  月、
  日、
  时、
  分、
  秒
  的
  日历
  时间。
  POSIX
  中
  此
  形式
  的
  时间
  表示
  包括
  ``struct tm``。

注意
这些
只是
时间
表示，
必须
相对于
时间
尺度
解释，
该
尺度
可能
是
本地
时间、
UTC
或
其他
连续
或
不
连续
的
尺度。

某些
必要
的
转换
在
标准
C
库
例程
中
可用。
例如，
测量
自
POSIX
EPOCH
以来
秒数
的
``time_t``
通过
`gmtime()
<https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime.html>`__
转换
为
表示
日历
时间
的
``struct tm``。
像
``struct timespec``
这样的
亚
秒
时间
戳
也
可以
使用
此
来
产生
日历
时间
表示
并
单独
处理
亚
秒
偏移。

逆
转换
不
是
标准
化
的：
像
``mktime()``
这样的
API
期望
时区
信息。
Zephyr
通过
:c:func:`timeutil_timegm`
和
:c:func:`timeutil_timegm64`
提供
此
转换。

要
在
``struct timespec``
和
``k_timeout_t``
持续时间
之间
转换，
使用
:c:func:`timespec_to_timeout`
和
:c:func:`timespec_from_timeout`。

.. code-block:: c

    k_timeout_t to;
    struct timespec ts;

    timespec_from_timeout(K_FOREVER, &ts);
    to = timespec_to_timeout(&ts); /* to == K_FOREVER */

    timespec_from_timeout(K_MSEC(100), &ts);
    to = timespec_to_timeout(&ts); /* to == K_MSEC(100) */

.. doxygengroup:: timeutil_repr_apis

.. _timeutil_sync:

时间
尺度
同步
==========================

有
若干
因素
影响
时间
尺度
的
同步：

* 离散
  瞬间
  表示
  变化
  的
  速率。
  例如，
  Zephyr
  运行时间
  以
  tick
  跟踪，
  tick
  在
  名义上
  以
  :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC`
  赫兹
  发生
  的
  事件
  处
  推进，
  而
  外部
  时间
  源
  可能
  以
  整
  秒
  或
  分数
  秒
  （例如
  微秒）
  提供
  数据。
* 将
  两个
  尺度
  在
  单个
  瞬间
  对齐
  所
  需
  的
  绝对
  偏移。
* 每个
  尺度
  中
  可
  观察
  瞬间
  之间
  的
  相对
  误差，
  用于
  一致
  地
  对齐
  多个
  瞬间。
  例如，
  被
  1-pulse-per-second
  GPS
  信号
  驯化
  的
  参考
  时钟
  将
  比
  由
  +/-
  250
  ppm
  误差
  的
  RC
  振荡器
  驱动
  的
  Zephyr
  系统
  时钟
  准确
  得多。

时间
尺度
之间
的
同步
或
对齐
通过
多
步骤
过程
完成：

* 时间
  尺度
  中
  的
  瞬间
  由
  （无
  符号）
  64 位
  整数
  表示，
  假设
  以
  固定
  名义
  速率
  推进。
* :c:struct:`timeutil_sync_config`
  记录
  参考
  时间
  尺度/源
  （例如
  TAI）
  和
  本地
  时间
  源
  （例如
  :c:func:`k_uptime_ticks`）
  的
  名义
  速率。
* :c:struct:`timeutil_sync_instant`
  记录
  单个
  瞬间
  在
  参考
  和
  本地
  时间
  尺度
  中
  的
  表示。
* :c:struct:`timeutil_sync_state`
  提供
  初始
  瞬间、
  最近
  接收
  的
  第二
  次
  观察
  和
  可以
  校正
  每个
  时间
  尺度
  实际
  速率
  中
  相对
  误差
  的
  偏斜
  的
  存储。
* :c:func:`timeutil_sync_ref_from_local()`
  和
  :c:func:`timeutil_sync_local_from_ref()`
  将
  一个
  时间
  尺度
  中
  的
  瞬间
  转换
  为
  另一个，
  考虑
  可以
  从
  状态
  结构
  中
  存储
  的
  两个
  实例
  估计
  的
  偏斜
  （由
  :c:func:`timeutil_sync_estimate_skew`
  估计）。

.. doxygengroup:: timeutil_sync_apis

.. _timeutil_manip:

``timespec``
操作
=========================

检查
``timespec``
的
有效性
可以
通过
:c:func:`timespec_is_valid`
完成。

.. code-block:: c

    struct timespec ts = {
        .tv_sec = 0,
        .tv_nsec = -1, /* out of range! */
    };

    if (!timespec_is_valid(&ts)) {
        /* error-handing code */
    }

在
某些
情况
下，
无效
的
``timespec``
对象
可以
使用
:c:func:`timespec_normalize`
重新
规范化。

.. code-block:: c

    if (!timespec_normalize(&ts)) {
        /* error-handling code */
    }

    /* ts should be normalized */
    __ASSERT(timespec_is_valid(&ts) == true, "expected normalized timespec");

可以
使用
:c:func:`timespec_equal`
比较
两个
``timespec``
对象
的
相等性。

.. code-block:: c

    if (timespec_equal(then, now)) {
        /* time is up! */
    }

可以
使用
:c:func:`timespec_compare`
比较
并
完全
排序
（有效
的）
``timespec``
对象。

.. code-block:: c

    int cmp = timespec_compare(a, b);

    switch (cmp) {
    case 0:
        /* a == b */
        break;
    case -1:
        /* a < b */
        break;
    case +1:
        /* a > b */
        break;
    }

可以
分别
使用
:c:func:`timespec_add`、
:c:func:`timespec_sub`
和
:c:func:`timespec_negate`
对
``timespec``
对象
执行
加、
减
和
取负。
像
:c:func:`timespec_normalize`
一样，
这些
函数
在
这样做
不
会
导致
溢出
时
输出
规范化
的
``timespec``。
成功
时，
这些
函数
返回
``true``。
如果
会
发生
溢出，
函数
返回
``false``。

.. code-block:: c

    /* a += b */
    if (!timespec_add(&a, &b)) {
        /* overflow */
    }

    /* a -= b */
    if (!timespec_sub(&a, &b)) {
        /* overflow */
    }

    /* a = -a */
    if (!timespec_negate(&a)) {
        /* overflow */
    }

.. doxygengroup:: timeutil_timespec_apis


.. _timeutil_concepts:

Zephyr
时间
支持
的
底层
概念
******************************************

来自
`ISO/TC 154/WG 5 N0038
<https://www.loc.gov/standards/datetime/iso-tc154-wg5_n0038_iso_wd_8601-1_2016-02-16.pdf>`__
（ISO/WD 8601-1）
和
其他
地方
的
术语：

* *时间轴*
  是
  时间
  作为
  有序
  瞬间
  序列
  的
  表示。
* *时间尺度*
  是
  相对于
  作为
  epoch
  的
  原点
  表示
  瞬间
  的
  方式。
* 如果
  连续
  时间
  瞬间
  的
  表示
  值
  从不
  减小，
  则
  时间
  尺度
  是
  *单调*
  （递增）
  的。
* 如果
  表示
  没有
  值
  的
  突然
  变化
  （例如
  在
  连续
  瞬间
  之间
  向前
  或
  向后
  跳跃），
  则
  时间
  尺度
  是
  *连续*
  的。
* `民用时间 <https://en.wikipedia.org/wiki/Civil_time>`__
  通常
  指
  由
  民用
  当局
  （如
  地方
  政府）
  法律
  定义
  的
  时间
  尺度，
  通常
  将
  本地
  午夜
  对齐
  到
  太阳
  时间。

相关
时间
尺度
====================

`International Atomic Time
<https://en.wikipedia.org/wiki/International_Atomic_Time>`__
（TAI）
是
基于
以
SI
秒
计数
的
时钟
平均
的
时间
尺度。
TAI
是
单调
且
连续
的
时间
尺度。

`Universal Time <https://en.wikipedia.org/wiki/Universal_Time>`__
（UT）
是
基于
地球
自转
的
时间
尺度。
UT
是
不
连续
的
时间
尺度，
因为
它
需要
偶尔
调整
（`leap seconds
<https://en.wikipedia.org/wiki/Leap_second>`__）
以
保持
与
地球
自转
变化
的
对齐。
因此
TAI
和
UT
之间
的
差
随
时间
变化。
UT
有
若干
变体，
其中
`UTC
<https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`__
最
常见。

UT
时间
独立
于
位置。
UT
是
标准
时间
（或
"本地
时间"）
的
基础，
即
特定
位置
的
时间。
标准
时间
在
任何
给定
瞬间
与
UT
有
固定
偏移，
主要
受
经度
影响，
但
偏移
可能
被
调整
（"夏令时"）
以
将
标准
时间
对齐
到
本地
太阳
时间。
在
某种
意义
上
本地
时间
比
UT
"更
不
连续"。

POSIX
Time
（请参阅
:rfc:`8536#section-2`）
是
计数
自
"POSIX
epoch"
1970-01-01T00:00:00Z
（即
1970
UTC
开始）
以来
秒数
的
时间
尺度。
UNIX
Time
是
POSIX
time
的
扩展，
使用
负值
表示
POSIX
epoch
之前
的
时间。
这两个
尺度
都
假设
每天
恰好
有
86400
秒。
在
正常
使用
中
这些
尺度
中
的
瞬间
对应
UTC
尺度
中
的
时间，
因此
继承
了
不
连续
性。

连续
的
类似
物
是
UNIX
Leap
Time，
即
UNIX
time
加
上
POSIX
epoch
之后
添加
的
所有
leap-second
校正
（当时
TAI-UTC
为
8
s）。

时间
尺度
差异
示例
---------------------------------

2016
年底
引入
了
一个
正
leap
second，
将
TAI
和
UTC
之间
的
差
从
36
秒
增加
到
37
秒。
1999
年底
没有
引入
leap
second，
当时
TAI
和
UTC
之间
的
差
只有
32
秒。
以下
表格
显示
若干
尺度
中
相关
的
民用
和
epoch
时间：

==================== ========== =================== ======= ==============
UTC
Date             UNIX
time  TAI
Date            TAI-UTC
UNIX
Leap
Time
==================== ========== =================== ======= ==============
1970-01-01T00:00:00Z
0          1970-01-01T00:00:08
+8      0
1999-12-31T23:59:28Z
946684768  2000-01-01T00:00:00
+32     946684792
1999-12-31T23:59:59Z
946684799  2000-01-01T00:00:31
+32     946684823
2000-01-01T00:00:00Z
946684800  2000-01-01T00:00:32
+32     946684824
2016-12-31T23:59:59Z
1483228799
2017-01-01T00:00:35
+36     1483228827
2016-12-31T23:59:60Z
undefined  2017-01-01T00:00:36
+36     1483228828
2017-01-01T00:00:00Z
1483228800
2017-01-01T00:00:37
+37     1483228829
==================== ========== =================== ======= ==============

功能
需求
-----------------------

Zephyr
tick
计数器
没有
leap
second
或
标准
时间
偏移
的
概念，
是
连续
的
时间
尺度。
但
它
可能
相对
不
准确，
漂移
最多
每
小时
三
分钟
（假设
5%
容差
的
RC
定时器）。

支持
Zephyr
时间
与
常见
人类
时间
尺度
之间
转换
需要
两个
阶段：

* 连续
  但
  不
  准确
  的
  Zephyr
  时间
  尺度
  与
  准确
  的
  外部
  稳定
  时间
  尺度
  之间
  的
  转换；
* 稳定
  时间
  尺度
  与
  （可能
  不
  连续
  的）
  民用
  时间
  尺度
  之间
  的
  转换。

:c:func:`timeutil_sync_state_update()`
周围
的
API
支持
连续
时间
尺度
之间
转换
的
第一
步。

第二
步
需要
外部
信息，
包括
leap
second
计划
和
本地
时间
偏移
变化。
这
可能
最好
由
外部
库
提供，
目前
不
是
时间
工具
API
的
一部分。

选择
外部
源
和
时间
尺度
-------------------------------------------

如果
应用
需要
几
秒
内
的
民用
时间
精度，
则
可以
使用
UTC
作为
稳定
时间
源。
但
如果
外部
源
调整
到
leap
second，
将
存在
不
连续
性：
以
1
Hz
采集
的
两次
观察
之间
的
经过
时间
不
等于
其
时间
戳
之间
的
数值
差。

对
精确
活动，
独立
于
本地
和
太阳
调整
的
连续
尺度
大大
简化
事情。
合适
的
连续
尺度
包括：

- GPS
  time：
  epoch
  为
  1980-01-06T00:00:00Z，
  连续
  跟随
  TAI，
  偏移
  TAI-GPS=19
  s。
- Bluetooth
  Mesh
  time：
  epoch
  为
  2000-01-01T00:00:00Z，
  连续
  跟随
  TAI，
  偏移
  -32。
- UNIX
  Leap
  Time：
  epoch
  为
  1970-01-01T00:00:00Z，
  连续
  跟随
  TAI，
  偏移
  -8。

由于
C
和
Zephyr
库
函数
支持
使用
UNIX
epoch
在
整数
和
日历
时间
表示
之间
转换，
UNIX
Leap
Time
是
外部
时间
尺度
的
理想
选择。

用于
填充
同步
点
的
机制
不
重要：
它
可能
涉及
从
本地
高精度
RTC
外设
读取，
使用
NTP
或
PTP
等
协议
通过
网络
交换
数据包，
或
处理
从
GPS
接收
的
NMEA
消息
（有
或
没有
1pps
信号）。

``timespec``
概念
=====================

最初
来自
POSIX，
``struct timespec``
自
C11
以来
是
C
标准
的
一部分。
``struct timespec``
的
定义
如
下
所示。

.. code-block:: c

   struct timespec {
       time_t tv_sec;  /* seconds */
       long   tv_nsec; /* nanoseconds */
   };

``tv_nsec``
字段
仅
在
``[0, 999999999]``
范围
内
的
值
有效。
``tv_sec``
字段
是
自
epoch
以来
的
秒数。
如果
``struct timespec``
用于
表示
差值，
``tv_sec``
字段
可能
落入
负值
范围。
