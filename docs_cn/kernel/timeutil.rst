.. _timeutil_api:

时间工具
##############

概览
********

Zephyr 中的 :ref:`kernel_timing_uptime` 基于一个节拍（tick）计数器。
使用默认的 :kconfig:option:`CONFIG_TICKLESS_KERNEL` 时，
该计数器从系统启动瞬间的零开始，以名义上恒定的速率前进。
该计数器的 POSIX 等价物类似于 ``CLOCK_MONOTONIC``，
或者在 Linux 中是 ``CLOCK_MONOTONIC_RAW``。
:c:func:`k_uptime_get()` 提供该时间的毫秒表示。

应用程序通常需要把 Zephyr 的内部时间与日常生活中使用的外部时间尺度关联起来，
例如本地时间或协调世界时（Coordinated Universal Time）。
这些系统以不同的方式解释时间，并且可能因
`闰秒（leap seconds） <https://what-if.xkcd.com/26/>`__
以及夏令时（daylight saving time）等本地时间偏移而出现不连续。

由于这些不连续性，以及周期计数器底层时钟的显著不准确性，
从 Zephyr 时钟估计的时间与"真实"民用时间尺度中实际时间之间的偏移
并不是恒定的，在 Zephyr 应用程序运行期间可能大幅变化。

时间工具 API 支持：

* :ref:`在时间表示之间转换 <timeutil_repr>`
* :ref:`同步和对齐时间尺度 <timeutil_sync>`
* :ref:`比较、添加和减去表示 <timeutil_manip>`

支持这些函数所用的术语和概念，参见 :ref:`timeutil_concepts`。

时间工具 API
*****************

.. _timeutil_repr:

表示转换
=============================

时间尺度上的时刻（instant）可以有多种表示方式，包括：

* 自纪元（epoch）以来的秒数。这种形式的 POSIX 时间表示包括
  ``time_t`` 和 ``struct timespec``，通常被解释为"UNIX 时间"（UNIX Time）
  的表示（参见 :rfc:`8536#section-2`）。

* 日历时间（calendar time），即相对于纪元的年、月、日、时、分、秒。
  这种形式的 POSIX 时间表示包括 ``struct tm``。

请记住，这些只是时间表示，必须相对于某个时间尺度来解释，
该时间尺度可能是本地时间、UTC，或其他某种连续或不连续的尺度。

某些必要的转换在标准 C 库例程中可用。例如，
测量自 POSIX 纪元以来秒数的 ``time_t`` 可以用
`gmtime() <https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime.html>`__
转换为表示日历时间的 ``struct tm``。
``struct timespec`` 这类亚秒时间戳也可以用它产生日历时间表示，
并单独处理亚秒偏移。

逆转换没有标准化：``mktime()`` 之类的 API 期望提供时区信息。
Zephyr 通过 :c:func:`timeutil_timegm` 和 :c:func:`timeutil_timegm64` 提供该转换。

要在 ``struct timespec`` 和 ``k_timeout_t`` 持续时间之间转换，
使用 :c:func:`timespec_to_timeout` 和 :c:func:`timespec_from_timeout`。

.. code-block:: c

    k_timeout_t to;
    struct timespec ts;

    timespec_from_timeout(K_FOREVER, &ts);
    to = timespec_to_timeout(&ts); /* to == K_FOREVER */

    timespec_from_timeout(K_MSEC(100), &ts);
    to = timespec_to_timeout(&ts); /* to == K_MSEC(100) */

.. doxygengroup:: timeutil_repr_apis

.. _timeutil_sync:

时间尺度同步
==========================

影响时间尺度同步的因素有若干：

* 离散时刻表示变化的速率。例如，Zephyr 的运行时间以节拍（ticks）跟踪，
  这些节拍以名义上 :kconfig:option:`CONFIG_SYS_CLOCK_TICKS_PER_SEC` 赫兹
  发生的事件前进，而外部时间源可能以整数或分数秒（例如微秒）提供数据。
* 在单个时刻对齐两个尺度所需的绝对偏移。
* 每个尺度中可观察时刻之间的相对误差，用于一致地对齐多个时刻。
  例如，由 1 脉冲/秒（1-pulse-per-second）GPS 信号驯服的参考时钟，
  会比由误差为 +/- 250 ppm 的 RC 振荡器驱动的 Zephyr 系统时钟准确得多。

时间尺度之间的同步或对齐通过一个多步骤过程完成：

* 时间尺度中的一个时刻由一个（无符号）64 位整数表示，
  假定它以固定的名义速率前进。
* :c:struct:`timeutil_sync_config` 记录参考时间尺度/源（例如 TAI）
  的本地时间源（例如 :c:func:`k_uptime_ticks`）的名义速率。
* :c:struct:`timeutil_sync_instant` 记录单个时刻在参考时间尺度
  和本地时间尺度中的表示。
* :c:struct:`timeutil_sync_state` 提供一个初始时刻、一个最近接收的
  第二次观测，以及一个可校正每个时间尺度实际速率中相对误差的
  偏斜（skew）的存储。
* :c:func:`timeutil_sync_ref_from_local()` 和
  :c:func:`timeutil_sync_local_from_ref()` 将一个时间尺度中的时刻
  转换为另一个时间尺度中的时刻，其中考虑的偏斜可由
  :c:func:`timeutil_sync_estimate_skew` 从状态结构中存储的两个时刻实例估计得出。

.. doxygengroup:: timeutil_sync_apis

.. _timeutil_manip:

``timespec`` 操作
=========================

可以用 :c:func:`timespec_is_valid` 检查 ``timespec`` 的有效性。

.. code-block:: c

    struct timespec ts = {
        .tv_sec = 0,
        .tv_nsec = -1, /* out of range! */
    };

    if (!timespec_is_valid(&ts)) {
        /* error-handing code */
    }

在某些情况下，无效的 ``timespec`` 对象可以用 :c:func:`timespec_normalize` 重新规范化。

.. code-block:: c

    if (!timespec_normalize(&ts)) {
        /* error-handling code */
    }

    /* ts should be normalized */
    __ASSERT(timespec_is_valid(&ts) == true, "expected normalized timespec");

可以用 :c:func:`timespec_equal` 比较两个 ``timespec`` 对象是否相等。

.. code-block:: c

    if (timespec_equal(then, now)) {
        /* time is up! */
    }

可以用 :c:func:`timespec_compare` 比较（有效的）``timespec`` 对象
并对其进行完全排序。

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

可以用 :c:func:`timespec_add`、:c:func:`timespec_sub` 和
:c:func:`timespec_negate` 分别对 ``timespec`` 对象进行加、减和取反。
与 :c:func:`timespec_normalize` 类似，这些函数在结果不会导致溢出时
输出规范化的 ``timespec``。成功时这些函数返回 ``true``。
如果将发生溢出，函数返回 ``false``。

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

Zephyr 时间支持的基础概念
******************************************

来自 `ISO/TC 154/WG 5 N0038
<https://www.loc.gov/standards/datetime/iso-tc154-wg5_n0038_iso_wd_8601-1_2016-02-16.pdf>`__
（ISO/WD 8601-1）和其他地方的术语：

* *时间轴*（time axis）是把时间表示为时刻的有序序列的表示。
* *时间尺度*（time scale）是相对于作为纪元（epoch）的原点（origin）
  来表示时刻的方式。
* 如果连续时刻的表示值从不减小，则该时间尺度是*单调的*（monotonic，递增的）。
* 如果表示在值上没有突变（例如在连续时刻之间向前或向后跳跃），
  则该时间尺度是*连续的*（continuous）。
* `民用时间（Civil time） <https://en.wikipedia.org/wiki/Civil_time>`__
  通常指由民事机构（如地方政府）以法律定义的时间尺度，
  通常用于把本地午夜与太阳时对齐。

相关时间尺度
==================

`国际原子时（International Atomic Time，TAI）
<https://en.wikipedia.org/wiki/International_Atomic_Time>`__
是一种基于对以国际单位制（SI）秒计数的时钟取平均的时间尺度。
TAI 是单调且连续的时间尺度。

`世界时（Universal Time，UT） <https://en.wikipedia.org/wiki/Universal_Time>`__
是一种基于地球自转的时间尺度。UT 是不连续的时间尺度，
因为它需要偶尔进行调整（`闰秒（leap seconds）
<https://en.wikipedia.org/wiki/Leap_second>`__）
以维持与地球自转变化的对齐。因此 TAI 与 UT 之间的差值随时间变化。
UT 有若干变体，其中 `UTC <https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`__
最为常见。

UT 时间独立于位置。UT 是标准时间（或"本地时间"，即某一特定位置的时间）的基础。
标准时间在任何给定时刻都有相对于 UT 的固定偏移，主要受经度影响，
但该偏移可能经过调整（"夏令时"）以使标准时间与本地太阳时对齐。
从某种意义上说，本地时间比 UT "更不连续"。

POSIX 时间（参见 :rfc:`8536#section-2`）是一种从 1970-01-01T00:00:00Z
（即 1970 UTC 开始）的"POSIX 纪元"起计算秒数的时间尺度。
UNIX 时间是 POSIX 时间的扩展，使用负值表示 POSIX 纪元之前的时间。
这两个尺度都假定每天恰好有 86400 秒。在正常使用中，
这些尺度中的时刻对应 UTC 尺度中的时间，因此继承了 UTC 的不连续性。

其连续等价物是 UNIX 闰时（UNIX Leap Time），
即 UNIX 时间加上 POSIX 纪元之后添加的所有闰秒修正
（当时 TAI-UTC 为 8 秒）。

时间尺度差异示例
---------------------------------

2016 年底引入了一个正闰秒，使 TAI 与 UTC 之间的差值从 36 秒增加到 37 秒。
1999 年底没有引入闰秒，当时 TAI 与 UTC 之间的差值只有 32 秒。
下表显示了若干尺度中相关的民用时间和纪元时间：

==================== ========== =================== ======= ==============
UTC 日期             UNIX 时间  TAI 日期            TAI-UTC UNIX 闰时
==================== ========== =================== ======= ==============
1970-01-01T00:00:00Z 0          1970-01-01T00:00:08 +8      0
1999-12-31T23:59:28Z 946684768  2000-01-01T00:00:00 +32     946684792
1999-12-31T23:59:59Z 946684799  2000-01-01T00:00:31 +32     946684823
2000-01-01T00:00:00Z 946684800  2000-01-01T00:00:32 +32     946684824
2016-12-31T23:59:59Z 1483228799 2017-01-01T00:00:35 +36     1483228827
2016-12-31T23:59:60Z 未定义     2017-01-01T00:00:36 +36     1483228828
2017-01-01T00:00:00Z 1483228800 2017-01-01T00:00:37 +37     1483228829
==================== ========== =================== ======= ==============

功能需求
-----------------------

Zephyr 的节拍计数器没有闰秒或标准时间偏移的概念，是一种连续的时间尺度。
但它可能相对不准确，漂移最多可达每小时三分钟
（假设使用容差为 5% 的 RC 定时器）。

支持 Zephyr 时间与常见人类时间尺度之间的转换需要两个阶段：

* 连续但不准确的 Zephyr 时间尺度与准确的外部稳定时间尺度之间的转换；
* 稳定时间尺度与（可能不连续的）民用时间尺度之间的转换。

围绕 :c:func:`timeutil_sync_state_update()` 的 API
支持连续时间尺度之间转换的第一步。

第二步需要外部信息，包括闰秒时间表和当地时间偏移变化。
这最好由外部库提供，目前不属于时间工具 API 的一部分。

选择外部源和时间尺度
-------------------------------------------

如果应用程序需要几秒以内的民用时间精度，可以使用 UTC 作为稳定的时间源。
然而，如果外部源对闰秒进行了调整，就会出现不连续：
以 1 Hz 获取的两次观测之间经过的时间，
不等于它们时间戳之间的数值差。

对于精确的活动，使用独立于本地调整和太阳时调整的连续尺度会大大简化事情。
适合的连续尺度包括：

- GPS 时间：纪元为 1980-01-06T00:00:00Z，连续跟随 TAI，偏移为 TAI-GPS=19 秒。
- 蓝牙 Mesh 时间：纪元为 2000-01-01T00:00:00Z，连续跟随 TAI，偏移为 -32。
- UNIX 闰时：纪元为 1970-01-01T00:00:00Z，连续跟随 TAI，偏移为 -8。

由于 C 和 Zephyr 库函数支持使用 UNIX 纪元在整数时间与日历时间表示之间转换，
UNIX 闰时是外部时间尺度的理想选择。

用于填充同步点的机制并不重要：它可能涉及从本地高精度 RTC 外设读取、
使用 NTP 或 PTP 等协议通过网络交换报文，
或处理从 GPS 接收的 NMEA 报文（无论有无 1pps 信号）。

``timespec`` 概念
=====================

``struct timespec`` 最初来自 POSIX，自 C11 起是 C 标准的一部分。
``struct timespec`` 的定义如下所示。

.. code-block:: c

   struct timespec {
       time_t tv_sec;  /* seconds */
       long   tv_nsec; /* nanoseconds */
   };

``tv_nsec`` 字段仅在 ``[0, 999999999]`` 范围内的值有效。
``tv_sec`` 字段是自纪元以来的秒数。
如果 ``struct timespec`` 用于表示一个差值，``tv_sec`` 字段可能落入负值范围。
