.. _twister_script:

测试
运行器
（Twister）
#####################

Twister
扫描
git
仓库
中
的
测试
应用
集
并
尝试
执行
它们。
默认
情况
下，
它
尝试
在
board
定义
文件
中
标记
为
default
的
boards
上
构建
每个
测试
应用。

默认
选项
将
在
定义
的
board
集
上
构建
大多数
测试
应用
并
在
可
用
的
情况
下
在
模拟
环境
中
运行
（如果
为
被
测试
的
架构
或
配置
可
用）。

由于
有限
的
测试
执行
覆盖
范围，
twister
不能
保证
本地
更改
在
完整
构建
环境
中
会
成功，
但
它
通过
为
不同
boards
和
不同
配置
构建
samples
和
tests
执行
足够
的
测试
帮助
保持
完整
代码
树
可
构建。

当
使用
（至少）
一个
``-v``
选项
时，
twister
的
控制台
输出
显示
每个
测试
应用
测试
如何
运行
（qemu、native_sim
等）
或
二进制
文件
只
被
构建。
测试
的
结果
:ref:`status
<twister_statuses>`
同样
被
报告
在
``twister.json``
和
其他
报告
文件
中。
有
一些
原因
为什么
twister
只
构建
测试
而
不
运行
它：

- 测试
  在
  其
  ``.yaml``
  配置
  文件
  中
  被
  标记
  为
  ``build_only:
  true``。
- 测试
  配置
  定义
  了
  ``harness``
  但
  你
  不
  有
  它
  或
  没
  有
  设置
  它。
- 目标
  设备
  未
  连接
  且
  不
  可
  用
  于
  烧录
- 你
  或
  某
  个
  更
  高
  层
  自动化
  用
  ``--build-only``
  调用
  twister。

要
在
本地
树
中
运行
Twister，
遵循
以下
步骤：

.. code-block:: console

   $
   west
   twister

.. note::

   本
   文档
   中
   的
   示例
   用
   ``west
   twister``
   调用
   Twister，
   :ref:`west
   <west>`
   扩展
   命令，
   在
   所有
   主机
   操作系统
   上
   工作
   方式
   相同。
   以下
   调用
   等价：

   * ``west
     twister
     ...``
     （推荐）。
   * ``python
     .\scripts\twister
     ...``
     （Windows）：
     直接
     调用
     脚本。
     这
     需要
     先
     设置
     Zephyr
     环境
     （``source
     zephyr-env.sh``
     或
     ``zephyr-env.cmd``）。

   所有
   形式
   接受
   相同
   的
   命令行
   选项。

如果
你
想
在
一
个
或多
个
特定
平台
上
运行
测试，
你
可以
用
``--platform``
选项，
它
是
测试
的
平台
过滤器，
带
这
个
选项，
测试
套件
只
会
在
指定
的
平台
上
构建/
运行。
这
个
选项
也
支持
同一
board
的
不同
版本，
你
可以
用
``--platform
board@revision``
在
特定
版本
上
测试。

twister
支持
的
命令行
选项
列表
可以
用
``west
twister
--help``
查看。
参考
:ref:`twister_commandline_options`
获取
完整
的
选项
集。

以下
页面
覆盖
额外
的
Twister
主题：

.. toctree::
   :maxdepth:
   1

   commandline
   pytest
   twister_statuses
   twister_blackbox

.. _twister_board_configuration:

Board
配置
*******************

要
为
特定
board
构建
测试
并
在
真实
硬件
或
QEMU
等
模拟
环境
中
执行
一些
测试
需要
一
个
board
配置
文件
它
足够
通用
可以
用
于
其他
需要
board
清单
的
任务
带
关于
board
和
其
配置
的
细节
否则
只
在
构建
时
可
用。

board
元数据
文件
位于
board
目录
中
并
用
YAML
标记
语言
结构化。
下面
的
示例
显示
一
个
board
带
此
特定
board
最佳
测试
覆盖
所需
的
数据：

.. code-block:: yaml

   identifier:
   frdm_k64f
   name:
   NXP
   FRDM-K64F
   type:
   mcu
   arch:
   arm
   toolchain:
     -
     zephyr
     -
     gnuarmemb
   supported:
     -
     arduino_gpio
     -
     arduino_i2c
     -
     netif:eth
     -
     adc
     -
     i2c
     -
     nvs
     -
     spi
     -
     gpio
     -
     usb_device
     -
     watchdog
     -
     can
     -
     pwm
   testing:
     default:
     true


identifier:
   一
   个
   匹配
   board
   在
   构建
   系统
   中
   如何
   定义
   的
   字符串。
   这
   同一
   字符串
   在
   构建
   时
   使用，
   例如
   调用
   ``west
   build``
   或
   ``cmake``
   时：

   .. code-block:: console

      #
      with
      west
      west
      build
      -b
      reel_board
      #
      with
      cmake
      cmake
      -DBOARD=reel_board
      ..

name:
   board
   在
   营销
   材料
   中
   出现
   的
   实际
   名称。
vendor:
   board
   供应商。
   用
   于
   ``vendor_allow``
   和
   ``vendor_exclude``
   测试
   场景
   过滤器。
tier:
   一
   个
   可选
   整数
   指示
   board
   支持
   层级。
   用
   于
   报告
   和
   按
   支持
   级别
   分组
   平台。
type:
   board
   或
   配置
   的
   类型。
   ``mcu``、
   ``qemu``、
   ``sim``、
   ``unit``
   或
   ``native``
   之一。
simulation:
   用
   来
   模拟
   平台
   的
   模拟器
   （例如
   qemu）。

   .. code-block:: yaml

      simulation:
        -
        name:
        qemu
        -
        name:
        armfvp
        exec:
        FVP_Some_Platform
        -
        name:
        custom
        exec:
        AnotherBinary

   默认
   情况
   下，
   测试
   用
   simulation
   数组
   中
   的
   第一
   个
   条目
   执行。
   另一
   个
   simulation
   可以
   用
   ``--simulation
   <simulation_name>``
   选择。
   ``exec``
   属性
   是
   可选
   的。
   如果
   它
   被
   设置
   但
   所需
   模拟器
   不
   可
   用，
   测试
   只
   被
   构建。
   如果
   它
   未
   设置
   且
   所需
   模拟器
   不
   可
   用
   测试
   将
   运行
   失败。
   simulation
   名称
   必须
   匹配
   ``SUPPORTED_EMU_PLATFORMS``
   的
   元素
   之一。
arch:
   board
   的
   架构
toolchain:
   可以
   构建
   这
   个
   board
   的
   支持
   工具链
   列表。
   这
   应该
   匹配
   命令行
   构建
   时
   用
   于
   :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
   的
   值
   之一。
   Twister
   过滤
   掉
   工具链
   不
   在
   这
   个
   列表
   中
   的
   任何
   测试
   实例，
   除非
   给出
   ``--force-toolchain``。
   这
   个
   列表
   说明
   哪些
   工具链
   *可能*
   构建
   board，
   它
   不
   选择
   一
   个；
   参考
   :ref:`twister_toolchain_selection`。
preferred_toolchain:
   Twister
   应该
   为
   这
   个
   平台
   使用
   的
   工具链
   当
   没有
   其他
   选择
   一
   个
   时。
   这
   对
   名义
   上
   可以
   用
   多
   个
   工具链
   构建
   但
   应该
   用
   特定
   一
   个
   测试
   的
   boards
   有用。
   参考
   :ref:`twister_toolchain_selection`。
build_toolchains:
   一
   个
   可选
   的
   工具链
   列表
   分配
   给
   这
   个
   平台
   的
   每个
   测试
   应该
   用
   它
   构建。
   Twister
   为
   列表
   中
   的
   每个
   工具链
   创建
   一
   个
   测试
   实例，
   每个
   在
   自己
   的
   构建
   目录
   中，
   而
   非
   为
   平台
   选择
   单一
   工具链。
   例如，
   要
   在
   ``native_sim``
   上
   用
   GCC
   和
   Clang
   构建
   一切：

   .. code-block:: yaml

      build_toolchains:
        -
        host/gnu
        -
        host/llvm

   由于
   这
   使
   构建
   时间
   倍增，
   通常
   最好
   将
   它
   排除
   在
   board
   定义
   之外
   并
   只
   为
   CI
   启用
   用
   :ref:`Twister
   configuration
   file
   <twister_test_config>`
   的
   ``build_toolchains``
   选项。
   参考
   :ref:`twister_toolchain_selection`。
ram:
   board
   上
   可用
   的
   RAM
   （以
   KB
   指定）。
   这
   用
   于
   匹配
   测试
   场景
   需求。
   如果
   未
   指定
   我们
   默认
   为
   128KB。
flash:
   board
   上
   可用
   的
   FLASH
   （以
   KB
   指定）。
   这
   用
   于
   匹配
   测试
   场景
   需求。
   如果
   未
   指定
   我们
   默认
   为
   512KB。


.. note::

   以下为原文（待翻译）

    of a testsuite or testcase.

modules: <list of module names>
    Build and run this test scenario only when all of the listed
    :ref:`modules <modules>` are present in the workspace. Scenarios that
    require a module which is not available are filtered out.

type: <string> (default integration)
    Test type of the scenario. Set to ``unit`` for unit tests that are built
    for the :ref:`unit_testing board <unit_testing_board>` and run on the host
    without the full Zephyr build system.

testcases: <list of test case names>
    Explicitly declare the list of test case names that make up this scenario.
    This is normally detected automatically (for example from the ztest source)
    and only needs to be set for harnesses that cannot be introspected.

ignore_faults: <True|False> (default False)
    Do not mark the test scenario as failed if a fault is detected in the
    output while the test is running.

ignore_qemu_crash: <True|False> (default False)
    Do not mark the test scenario as failed if QEMU crashes while the test is
    running.

The set of test scenarios that actually run depends on directives in the test scenario
file and options passed in on the command line. If there is any confusion,
running with ``-v`` or examining the :ref:`test plan <twister_output>`
(:file:`testplan.json`) can help show why particular test scenarios were
filtered out.

To load arguments from a file, add ``+`` before the file name, e.g.,
``+file_name``. File content must be one or more valid arguments separated by
line break instead of white spaces.

Most everyday users will run with no arguments.

.. _twister_module_dir_vars:

Expanding paths with module directory variables
===============================================

Path options in the test scenario file (e.g. ``required_applications``,
``harness_config: pytest_root``) are expanded before use. In addition to
environment variables, Twister expands Zephyr module directory
variables, which mirror the CMake variables defined for every module:

* ``ZEPHYR_<MODULE>_MODULE_DIR`` - absolute path to the module's root.
* ``ZEPHYR_<MODULE>_MODULE_NAME`` - the module's name.

``<MODULE>`` is upper-cased with non-alphanumeric characters replaced by ``_``,
exactly as CMake does (for example ``$ZEPHYR_HAL_NORDIC_MODULE_DIR`` for the
``hal_nordic`` module). Unknown references are left unchanged.

Managing tests timeouts
=======================

There are several parameters which control tests timeouts on various levels:

* ``timeout`` option in each test scenario. See :ref:`here <twister_test_case_timeout>` for more
  details.
* ``timeout_multiplier`` option in board configuration. See
  :ref:`here <twister_board_timeout_multiplier>` for more details.
* ``--timeout-multiplier`` twister option which can be used to adjust timeouts in exact twister run.
  It can be useful in case of simulation platform as simulation time may depend on the host
  speed & load or we may select different simulation method (i.e. cycle accurate but slower
  one), etc...

Overall test scenario timeout is a multiplication of these three parameters.

.. _twister_dt_filter_expressions:

Devicetree Filtering Expressions
================================

Expressions starting with "dt_*" are used to filter boards based on specific
devicetree properties, such as compatibles, aliases, node labels, node
properties, chosen nodes, etc. when selecting test scenarios.

.. note::

   The source code for these expressions can be found at
   :zephyr_file:`scripts/pylib/twister/expr_parser.py`.

Expressions
-----------

``dt_compat_enabled(compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if any DT node with the specified compatible string (``compat``) is enabled.

**Parameters:**
   - ``compat``: The compatible string to match.

``dt_alias_exists(alias)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if any DT node with the specified alias exists and is enabled.

**Parameters:**
   - ``alias``: The alias (defined in ``aliases`` node) to match.

``dt_enabled_alias_with_parent_compat(alias, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if the DT has an enabled alias node whose parent has the specified compatible string.
   Useful for nodes like ``gpio-leds`` child nodes, which may not have their own compatible.

**Parameters:**
   - ``alias``: The alias (defined in ``aliases`` node) to match.
   - ``compat``: The parent node’s compatible string to match.

``dt_label_with_parent_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT node with the specified label exists, is enabled, and its parent has the
   specified compatible string.

**Parameters:**
   - ``label``: The node label to match.
   - ``compat``: The parent node’s compatible string to match.

``dt_label_compat_enabled(label, compat)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT node with the specified label exists, is enabled, and has the
   specified compatible string.

**Parameters:**
   - ``label``: The node label to match.
   - ``compat``: The node compatible string to match.

``dt_chosen_enabled(chosen)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT chosen property with the specified name exists and the node assigned to it
   is enabled.

**Parameters:**
   - ``chosen``: The name of the chosen property.

``dt_nodelabel_enabled(label)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT node with the specified label exists and is enabled.

**Parameters:**
   - ``label``: The node label to match.

``dt_nodelabel_prop_enabled(label, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT node with the specified label exists, is enabled, and has the specified property
   with a non-empty value.

**Parameters:**
   - ``label``: The node label to match.
   - ``prop``: The node's property to check.

``dt_node_has_prop(node_id, prop)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose:**
   Checks if a DT node (specified by alias or path) has the specified property, regardless of its
   status. Useful for nodes that do not have a status, like ``zephyr,user`` node.

**Parameters:**
   - ``node_id``: The node alias (defined in ``aliases`` node) or node path to match.
   - ``prop``: The node's property to check.

Usage
-----

These expressions are used in Twister’s test scenarios filtering logic to select boards that match
specific DT conditions. For example:

.. code-block:: yaml

   tests:
     - test: my_test
       filter: dt_compat_enabled("my-compat-string")

The test scenario ``my_test`` will only build for boards where a DT node with ``my-compat-string``
is enabled.

.. _twister_harnesses:

Harnesses
*********

A *harness* is the mechanism Twister uses to run a test and decide whether it
passed or failed. After a test image is built and started on its target (real
hardware, an emulator, or the host), the harness drives the interaction with
the running image -- providing input, capturing output, or handing execution
over to an external test runner -- and interprets the result to assign a
:ref:`status <twister_statuses>` to each test case.

A test scenario selects a harness with the ``harness:`` entry in its
``tests.yaml`` and tunes its behavior through ``harness_config``. When no
harness is specified, the default ``test`` harness is used. Different harnesses
serve different needs: some parse the device's console output against expected
patterns, while others delegate execution to an external framework such as
pytest, Robot Framework, or ctest. The pages linked below describe each
supported harness and its ``harness_config`` options.

Harnesses ``ztest``, ``gtest`` and ``console`` are based on parsing of the
output and matching certain phrases. ``ztest`` and ``gtest`` harnesses look
for pass/fail/etc. frames defined in those frameworks.

Some widely used harnesses that are not supported yet:

- keyboard
- net
- bluetooth

The following is an example yaml file with a few harness_config options.

.. code-block:: yaml

      sample:
        name: HTS221 Temperature and Humidity Monitor
      common:
        tags:
          - sensor
        harness: console
        harness_config:
          type: multi_line
          ordered: false
          regex:
            - "Temperature:(.*)C"
            - "Relative Humidity:(.*)%"
          fixture: i2c_hts221
      tests:
        test:
          tags:
            - sensors
          depends_on: i2c

.. toctree::
   :maxdepth: 1

   harness/ctest
   harness/gtest
   harness/pytest
   harness/console
   harness/robot
   harness/power
   harness/display_capture
   harness/script
   harness/bsim
   harness/shell


.. _twister_sidecars:

Sidecars
********

Some tests need a host-side resource to exist for the duration of a run: a
daemon the emulated guest talks to, a shared memory region the host reads back
afterwards, or a network interface the guest attaches to. A *sidecar* models
this. It is selected with the ``sidecar:`` entry in a test scenario's
:file:`tests.yaml` and is orthogonal to the harness: the
harness interprets the guest's output while the sidecar provisions the host side
around the run. Any harness (``console`` for a sample, ``ztest`` for a test,
...) can therefore be paired with any sidecar.

.. code-block:: yaml

   tests:
     some.test:
       harness: ztest
       sidecar: <name>

A sidecar has a small lifecycle, driven by Twister for each test instance:

#. **configure** -- the sidecar reads what it needs from the instance and its
   ``sidecar_config`` block before anything is provisioned.
#. **host check** -- at test-plan time the sidecar reports whether the host
   provides what it needs (for example, that a required daemon binary is
   installed). When it does not, the test is *built only* and not executed,
   exactly like a platform whose simulator is not installed.
#. **setup** -- called just before the handler runs the test image; it brings
   the host resource up (starts a daemon, creates an interface, ...). If the
   host side still turns out to be unavailable -- for example bringing the
   resource up needs privileges that are not present -- setup reports this and
   Twister *skips* execution instead of failing the test.
#. **teardown** -- called after the handler returns, in a ``finally`` block, so
   it always runs even if the test failed or timed out. It releases the resource
   and may also collect data the guest left behind (for example reading a shared
   memory region back into the build directory).

Because provisioning is decoupled from output processing, Twister can also
attach a sidecar to an instance itself, without the test opting in -- for
example to route coverage data off a guest that has no other host transport.

Each sidecar defines its own configuration keys under a block of
``sidecar_config`` named after the sidecar. Namespacing by sidecar name keeps
each sidecar's keys separate, so only the block matching the scenario's
``sidecar:`` value is consumed. For example, the ``virtiofs`` sidecar shares a
host directory seeded from a template with:

.. code-block:: yaml

   tests:
     some.test:
       harness: console
       sidecar: virtiofs
       sidecar_config:
         virtiofs:
           shared: shared


Selecting platform scope
************************

One of the key features of Twister is its ability to decide on which platforms a given
test scenario should run. This behavior has its roots in Twister being developed as
a test runner for Zephyr's CI. With hundreds of available platforms and thousands of
tests, the testing tools should be able to adapt the scope and select/filter out what
is relevant and what is not.

Twister always prepares an initial list of platforms in scope for a given test,
based on command line arguments and the :ref:`test's configuration <test_config_args>`. Then,
platforms that don't fulfill the conditions required in the configuration yaml
(e.g. minimum ram) are filtered out from the scope.
Using ``--force-platform`` allows to override filtering caused by ``platform_allow``,
``platform_exclude``, ``arch_allow`` and ``arch_exclude`` keys in test configuration
files.

Command line arguments define the initial scope in the following way:

* ``-p/--platform <platform_name>`` (can be used multiple times): only platforms
  passed with this argument;
* ``-l/--all``: all available platforms;
* ``-G/--integration``: all platforms from an ``integration_platforms`` list in
  a given test configuration file. If a test has no ``integration_platforms``
  *"scope presumption"* will happen;
* No scope argument: *"scope presumption"* will happen.

*"Scope presumption"*: A list of Twister's :ref:`default platforms <twister_default_testing_board>`
is used as the initial list. If nothing is left after the filtration, the ``platform_allow`` list
is used as the initial scope.

Running in Integration Mode
***************************

This mode is used in continuous integration (CI) and other automated
environments used to give developers fast feedback on changes. The mode can
be activated using the ``--integration`` option of twister and narrows down
the scope of builds and tests if applicable to platforms defined under the
integration keyword in the test configuration file (``tests.yaml``).


Running tests on custom emulator
********************************

Apart from the already supported QEMU and other simulated environments, Twister
supports running any out-of-tree custom emulator defined in the board's :file:`board.cmake`.
To use this type of simulation, add the following properties to
:file:`custom_board/custom_board.yaml`:

.. code-block:: yaml

   simulation:
     - name: custom
       exec: <name_of_emu_binary>

This tells Twister that the board is using a custom emulator called ``<name_of_emu_binary>``,
make sure this binary exists in the PATH.

Then, in :file:`custom_board/board.cmake`, set the supported emulation platforms to ``custom``:

.. code-block:: cmake

   set(SUPPORTED_EMU_PLATFORMS custom)

Finally, implement the ``run_custom`` target in :file:`custom_board/board.cmake`.
It should look something like this:

.. code-block:: cmake

   add_custom_target(run_custom
     COMMAND
     <name_of_emu_binary to invoke during 'run'>
     <any args to be passed to the command, i.e. ${BOARD}, ${APPLICATION_BINARY_DIR}/zephyr/zephyr.elf>
     WORKING_DIRECTORY ${APPLICATION_BINARY_DIR}
     DEPENDS ${logical_target_for_zephyr_elf}
     USES_TERMINAL
     )


Running Tests in Random Order
*****************************
Enable ZTEST framework's :kconfig:option:`CONFIG_ZTEST_SHUFFLE` config option to
run your tests in random order.  This can be beneficial for identifying
dependencies between test cases. For native_sim platforms, you can provide
the seed to the random number generator by providing ``--seed=value`` as an
argument to twister. See :ref:`Shuffling Test Sequence <ztest_shuffle>` for more
details.


Running Tests on Hardware
*************************

Beside being able to run tests in QEMU and other simulated environments,
twister supports running most of the tests on real devices and produces
reports for each run with detailed FAIL/PASS results.


Executing tests on a single device
==================================

To use this feature on a single connected device, run twister with
the following new options:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

	      west twister --device-testing --device-serial /dev/ttyACM0 \
	      --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

   .. group-tab:: Windows

      .. code-block:: bat

	      west twister --device-testing --device-serial COM1 \
	      --device-serial-baud 115200 -p frdm_k64f  -T tests/kernel

The ``--device-serial`` option denotes the serial device the board is connected to.
This needs to be accessible by the user running twister. You can run this on
only one board at a time, specified using the ``--platform`` option.
If the platform supports multiple serial ports, you can provide ``--device-serial``
multiple times, and it will be passed to the pytest harness. Alternatively you can use
the hardware map, see :ref:`multi-core testing <twister_multi_core_testing>` for more details

The ``--device-serial-baud`` option is only needed if your device does not run at
115200 baud.

To support devices without a physical serial port, use the ``--device-serial-pty``
option. In this cases, log messages are captured for example using a script.
In this case you can run twister with the following options:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --device-serial-pty "script.py" \
         -p intel_adsp/cavs25 -T tests/kernel

   .. group-tab:: Windows

      .. note::

         Not supported on Windows OS

The script is user-defined and handles delivering the messages which can be
used by twister to determine the test execution status.

The ``--device-flash-timeout`` option allows to set explicit timeout on the
device flash operation, for example when device flashing takes significantly
large time.

The ``--device-flash-with-test`` option indicates that on the platform
the flash operation also executes a test scenario, so the flash timeout is
increased by a test scenario timeout.

Executing tests on multiple devices
===================================

To build and execute tests on multiple devices connected to the host PC, a
hardware map needs to be created with all connected devices and their
details such as the serial device, baud and their IDs if available.
Run the following command to produce the hardware map:

.. code-block:: console

   $ west twister --generate-hardware-map map.yml

The generated hardware map file (map.yml) will have the list of connected
devices, for example:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
         - connected: true
           id: "000683759358"
           platform: unknown
           product: J-Link
           runner: unknown
           serial: /dev/cu.usbmodem0006837593581

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM1
         - connected: true
           id: "000683759358"
           platform: unknown
           product: unknown
           runner: unknown
           serial: COM2


Any options marked as ``unknown`` need to be changed and set with the correct
values, in the above example the platform names, the products and the runners need
to be replaced with the correct values corresponding to the connected hardware.
In this example we are using a reel_board and an nrf52840dk/nrf52840:

.. tabs::

   .. group-tab:: Linux

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: /dev/cu.usbmodem146114202
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: /dev/cu.usbmodem0006837593581
           baud: 9600

   .. group-tab:: Windows

      .. code-block:: yaml

         - connected: true
           id: "OSHW000032254e4500128002ab98002784d1000097969900"
           platform: reel_board
           product: DAPLink CMSIS-DAP
           runner: pyocd
           serial: COM1
           baud: 9600
         - connected: true
           id: "000683759358"
           platform: nrf52840dk/nrf52840
           product: J-Link
           runner: nrfjprog
           serial: COM2
           baud: 9600

The baud entry is only needed if not running at 115200.

If the map file already exists, then new entries are added and existing entries
will be updated. This way you can use one single master hardware map and update
it for every run to get the correct serial devices and status of the devices.

With the hardware map ready, you can run any tests by pointing to the map

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister --device-testing --hardware-map map.yml -T samples/hello_world/

   .. group-tab:: Windows

      .. code-block:: bat

         west twister --device-testing --hardware-map map.yml -T samples\hello_world

The above command will result in twister building tests for the platforms
defined in the hardware map and subsequently flashing and running the tests
on those platforms.

.. note::

  Currently only boards with support for pyocd, nrfjprog, jlink, openocd, or dediprog
  are supported with the hardware map features. Boards that require other runners to flash the
  Zephyr binary are still work in progress.

Hardware map allows to set ``--device-flash-timeout`` and ``--device-flash-with-test``
command line options as ``flash-timeout`` and ``flash-with-test`` fields respectively.
These hardware map values override command line options for the particular platform.

Serial PTY support using ``--device-serial-pty``  can also be used in the
hardware map:

.. code-block:: yaml

   - connected: true
     id: None
     platform: intel_adsp/cavs25
     product: None
     runner: intel_adsp
     serial_pty: path/to/script.py
     runner_params:
       - --remote-host=remote_host_ip_addr
       - --key=/path/to/key.pem


The runner_params field indicates the parameters you want to pass to the
west runner. For some boards the west runner needs some extra parameters to
work. It is equivalent to following west and twister commands.

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west flash --remote-host remote_host_ip_addr --key /path/to/key.pem

         west twister -p intel_adsp/cavs25 --device-testing --device-serial-pty script.py
         --west-flash="--remote-host=remote_host_ip_addr,--key=/path/to/key.pem"

   .. group-tab:: Windows

      .. note::

         Not supported on Windows OS

.. note::

  For serial PTY, the "--generate-hardware-map" option cannot scan it out
  and generate a correct hardware map automatically. You have to edit it
  manually according to above example. This is because the serial port
  of the PTY is not fixed and being allocated in the system at runtime.

If west is not available or does not know how to flash your system, a custom
flash command can be specified using the ``flash-command`` flag. The script is
called with a ``--build-dir`` with the path of the current build, as well as a
``--board-id`` flag to identify the specific device when multiple are available
in a hardware map.

.. tabs::

   .. group-tab:: Linux

      .. code-block:: bash

         west twister -p npcx9m6f_evb --device-testing --device-serial /dev/ttyACM0
         --flash-command './custom_flash_script.py,--flag,"complex, argument"'

   .. group-tab:: Windows

      .. note::

         west twister -p npcx9m6f_evb --device-testing
         --device-serial COM1
         --flash-command 'custom_flash_script.py,--flag,"complex, argument"'

Would result in calling ``./custom_flash_script.py
--build-dir <build directory> --board-id <board identification>
--flag "complex, argument"``.

.. _twister_fixtures:

Fixtures
--------

Some tests require additional setup or special wiring specific to the test.
Running the tests without this setup or test fixture may fail. A test scenario can
specify the fixture it needs which can then be matched with hardware capability
of a board and the fixtures it supports via the command line or using the hardware
map file.

Fixtures are defined in the hardware map file as a list:

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        id: "0240000026334e450015400f5e0e000b4eb1000097969900"
        platform: frdm_k64f
        product: DAPLink CMSIS-DAP
        runner: pyocd
        serial: /dev/ttyACM9

When running ``twister`` with ``--device-testing``, the configured fixture
in the hardware map file will be matched to test scenarios requesting the same fixtures
and these tests will be executed on the boards that provide this fixture.

To reserve a board for fixture-dependent tests, set ``run_with_fixture_only`` to
``true``. Twister will select that board only for test scenarios that request
matching fixtures; it will not select the board for scenarios without fixture
requirements.

.. code-block:: yaml

      - connected: true
        fixtures:
          - gpio_loopback
        run_with_fixture_only: true
        id: 0240000026334e450015400f5e0e000b4eb1000097969900
        platform: frdm_k64f

.. figure:: figures/fixtures.svg
   :figclass: align-center

Fixtures can also be provided via twister command option ``--fixture``, this option
can be used multiple times and all given fixtures will be appended as a list. And the
given fixtures will be assigned to all boards, this means that all boards set by
current twister command can run those test scenarios which request the same fixtures.

Some fixtures allow for configuration strings to be appended, separated from the
fixture name by a ``:``. Only the fixture name is matched against the fixtures
requested by test scenarios.

Notes
-----

It may be useful to annotate board descriptions in the hardware map file
with additional information.  Use the ``notes`` keyword to do this.  For
example:

.. code-block:: yaml

    - connected: false
      fixtures:
        - gpio_loopback
      id: "000683290670"
      notes: An nrf5340dk/nrf5340 is detected as an nrf52840dk/nrf52840 with no serial
        port, and three serial ports with an unknown platform.  The board id of the serial
        ports is not the same as the board id of the development kit.  If you regenerate
        this file you will need to update serial to reference the third port, and platform
        to nrf5340dk/nrf5340/cpuapp or another supported board target.
      platform: nrf52840dk/nrf52840
      product: J-Link
      runner: jlink
      serial: null

Overriding Board Identifier
---------------------------

When (re-)generated the hardware map file will contain an ``id`` keyword
that serves as the argument to ``--board-id`` when flashing.  In some
cases the detected ID is not the correct one to use, for example when
using an external J-Link probe.  The ``probe_id`` keyword overrides the
``id`` keyword for this purpose.   For example:

.. code-block:: yaml

    - connected: false
      id: "0229000005d9ebc600000000000000000000000097969905"
      platform: mimxrt1060_evk
      probe_id: "000609301751"
      product: DAPLink CMSIS-DAP
      runner: jlink
      serial: null

Using Single Board For Multiple Variants
----------------------------------------

  The ``platform`` attribute can be a list of names or a string
  with names separated by spaces. This allows to run tests for
  different platform variants on the same physical board, without
  re-configuring the hardware map file for each variant. For example:

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      platform:
      - nrf5340dk/nrf5340/cpuapp
      - nrf5340dk/nrf5340/cpuapp/ns
      product: J-Link
      runner: nrfjprog
      serial: /dev/ttyACM1

.. _twister_multi_core_testing:

Multi-Core testing support
--------------------------

Twister supports testing multi-core applications where different cores use
separate UART interfaces. This feature works only with the pytest harness
(``harness: pytest``). Generated hardware map should contain multiple entries
for the same physical device, each representing a different core connection.
For example:

.. code-block:: yaml

    - connected: true
      id: "001234567890"
      serial: /dev/ttyACM0
    - connected: true
      id: "001234567890"
      platform:
      - nrf54l15dk/nrf54l15/cpuapp
      product: J-Link
      runner: nrfutil
      serial: /dev/ttyACM1

Both instances share the same device ID but have different serial ports, allowing
tests to interact with multiple cores simultaneously. Each connection
is handled independently with separate log files.

.. _twister_multi_duts_testing:

Multi-DUTs testing support
--------------------------

Twister supports test scenarios that require more than one device.
This feature works only with the pytest harness (``harness: pytest``).
Hardware and ``native_sim`` execution environments are supported.

To declare that a test needs an additional device, add
``required_devices`` under ``harness_config`` in the test's YAML file.
Each entry in the list describes one extra DUT. An empty entry ``{}``
reserves a second device with the same platform and application as the
main DUT. See :ref:`required_devices <required_devices>` for all available options.

Example test configuration:

.. code-block:: yaml

    tests:
      multidut.basic:
        harness: pytest
        harness_config:
          required_devices:
            - {}

The hardware map must contain at least one entry per required device.
Each entry needs a matching platform and a serial connection:

.. code-block:: yaml

    - connected: true
      id: "01"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM0
    - connected: true
      id: "02"
      platform: nrf52840dk/nrf52840
      serial: /dev/ttyACM1

Run the test on hardware with:

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut \
      --device-testing --hardware-map map.yaml

Run the test on ``native_sim`` (no hardware map required):

.. code-block:: console

    $ west twister -vv -ll debug -T tests/subsys/testsuite/multidut -p native_sim

Twister reserves all required devices (or creates placeholder entries if ``native_sim`` is used),
then passes them to pytest with all necessary information
(platform, serial connection, build artifacts to flash, etc.) so the
test can interact with all devices.

An example multi-DUT test can be found at
:zephyr_file:`tests/subsys/testsuite/multidut`.

Quarantine
----------

Twister allows user to provide configuration files defining a list of tests or
platforms to be put under quarantine. Such tests will be skipped and marked
accordingly in the output reports. This feature is especially useful when
running larger test suits, where a failure of one test can affect the execution
of other tests (e.g. putting the physical board in a corrupted state).

To use the quarantine feature one has to add the argument
``--quarantine-list <PATH_TO_QUARANTINE_YAML>`` to a twister call.
Multiple quarantine files can be used.
The current status of tests on the quarantine list can also be verified by adding
``--quarantine-verify`` to the above argument. This will make twister skip all tests
which are not on the given list.

A quarantine yaml is a sequence of dictionaries. Each dictionary must have
at least one of the following keys: ``scenarios``, ``platforms``, ``architectures``
or ``simulations``. A combination of these entries is allowed.
An optional ``comment`` entry can be used to provide more details
(e.g., a link to a reported issue). These comments will also
be added to the output reports.

When quarantining a class of tests or many scenarios in a single testsuite or
when dealing with multiple issues within a subsystem, it is possible to use
regular expressions, for example, **kernel.*** would quarantine
all kernel tests.

An example of entries in a quarantine yaml:

.. code-block:: yaml

    - scenarios:
        - sample.basic.helloworld
      comment: "Link to the issue: https://github.com/zephyrproject-rtos/zephyr/pull/33287"

    - scenarios:
        - kernel.common
        - kernel.common.(misra|tls)
        - kernel.common.nano64
      platforms:
        - .*_cortex_.*
        - native_sim

    - platforms:
        - qemu_x86
      comment: "filter out qemu_x86"

    - architectures:
        - riscv

    - simulations:
        - armfvp

.. _twister_output:

Test Output and Reports
***********************

By default, Twister writes all of its output to a :file:`twister-out` directory
created in the current working directory. Use ``-O``/``--outdir`` to choose a
different location. On each run this directory is cleaned, unless ``--no-clean``
is given; ``--clobber-output`` controls what cleaning does.

Top-level reports
=================

The following files are written at the root of the output directory:

:file:`twister.json`
    The primary machine-readable report. It contains an entry for every selected
    test suite and test case with its :ref:`status <twister_statuses>`, target
    platform, execution time, memory footprint, any
    :ref:`recorded data <twister_console_harness>`, and the environment and
    options used for the run.

:file:`testplan.json`
    The resolved test plan: every test instance (test scenario times platform)
    that Twister considered, including those that were filtered out together
    with the reason. This is the file to inspect to understand why a given
    scenario did or did not run. It can be reused with ``--load-tests`` to
    replay the same selection.

:file:`twister.xml`
    JUnit XML summary suitable for CI systems.

:file:`twister_report.xml`
    JUnit XML report including all test cases (not just the summary).

:file:`twister_suite_report.xml`
    JUnit XML report grouped by test suite.

:file:`twister.log`
    Human-readable log of the whole run.

:file:`twister_footprint.json`
    ROM/RAM footprint report. Only generated when ``--footprint-report`` is used.

The report base name (``twister``) can be changed with ``--report-name``, and
``--report-suffix`` appends a suffix (for example a version or commit ID) to all
generated file names. Use ``-o``/``--report-dir`` to write the reports to a
directory other than the output directory, and ``--platform-reports`` to
additionally emit a per-platform :file:`<platform>.json` and
:file:`<platform>.xml`. ``--report-summary`` prints a summary of the failures
from the latest run without rebuilding.

Per-test artifacts
==================

Each test instance has its own build directory under the output directory,
named after the platform and the test:
:file:`twister-out/<platform>/<test path>/<scenario>/`. In addition to the
normal Zephyr build artifacts (for example :file:`zephyr/zephyr.elf`), it may
contain:

:file:`build.log`
    Output of the build for this instance.

:file:`handler.log`
    Console output captured from the device or emulator while running the test.

:file:`twister_harness.log`
    Log produced by pytest-based harnesses (for example ``pytest`` and
    ``shell``).

:file:`recording.csv`
    Data fields captured by the ``record`` option of the
    :ref:`console harness <twister_console_harness>`, when configured.

.. _twister_console_monitor:

Live Run Monitoring
*******************

For long runs it can be hard to tell from the scrolling console output what
twister is actually doing: what is queued, what each job is building or
running right now, and which tests have already failed and why. The
``--console-monitor`` option replaces the normal output with a live
full-screen dashboard in the terminal for the duration of the run:

.. code-block:: console

   $ west twister -T tests/kernel --console-monitor

The dashboard shows overall progress with pass/fail/error/filtered
breakdowns and an estimated time to completion, the set of test instances
currently *in flight* with the pipeline stage each one is in (``cmake``,
``build``, ``run``, ...), and a scrollable table of every test instance in
the plan, including statically filtered ones. Normal log output goes to
:file:`twister.log` in the meantime.

Navigation: :kbd:`Tab` cycles the table filter
(all/active/failures/passed/queued/filtered), :kbd:`f` jumps straight to
the failures view, and :kbd:`/` starts an incremental text search over
instance names and failure reasons (:kbd:`Esc` clears it). Move the
selection with the arrow keys or :kbd:`j`/:kbd:`k` and press :kbd:`Enter`
to open the detail view for an instance: its pipeline stage timeline, the
list of failing test cases with their reasons, and the tail of its log
files (:kbd:`l` switches between the available logs, :kbd:`j`/:kbd:`k` or
the arrow keys scroll, :kbd:`g`/:kbd:`G` jump to the top/end, and the view
follows new output while pinned to the end) -- particularly useful for
inspecting failures while the rest of the run continues.

When the run finishes the dashboard stays up so failures can be inspected;
pressing :kbd:`q` leaves it, after which reports are written and twister
exits as usual. Pressing :kbd:`q` while the run is still going leaves the
dashboard early and resumes the normal console output. The option requires
an interactive terminal and is ignored otherwise (e.g. in CI).

The monitor observes the run without influencing it: monitoring events are
delivered on a best-effort basis and are dropped rather than ever delaying
the build/run pipeline.

.. _twister_test_config:

Twister Configuration File
**************************

The Twister configuration file (``test_config.yaml``, passed with
``--test-config``) can be used to customize various aspects of twister
and the default enabled options and features. This allows tweaking the filtering
capabilities depending on the environment and makes it possible to adapt and
improve coverage when targeting different sets of platforms.

.. note::

   This file (selected with ``--test-config``) configures a whole Twister run.
   It is distinct from the per-application test configuration in ``tests.yaml``,
   which describes individual :ref:`test scenarios <twister_tests_long_version>`.

The Twister configuration file also adds support for test levels and the ability
to assign a specific test to one or more levels. Using command line options of
twister it is then possible to select a level and just execute the tests
included in this level.

Additionally, the configuration file allows defining level
dependencies and additional inclusion of tests into a specific level if
the test itself does not have this information already.

In the configuration file you can include complete components using
regular expressions and you can specify which test level to import from
the same file, making management of levels easier.

To help with testing outside of upstream CI infrastructure, additional
options are available in the configuration file, which can be hosted
locally. As of now, those options are available:

- Ability to ignore default platforms as defined in board definitions
  (Those are mostly emulation platforms used to run tests in upstream
  CI)
- Option to specify your own list of default platforms overriding what
  upstream defines.
- Ability to override ``build_on_all`` options used in some test scenarios.
  This will treat tests or sample as any other just build for default
  platforms you specify in the configuration file or on the command line.
- Ignore some logic in twister to expand platform coverage in cases where
  default platforms are not in scope.


Platform Configuration
======================

The following options control platform filtering in twister:

- ``override_default_platforms``: override default key a platform sets in board
  configuration and instead use the list of platforms provided in the
  configuration file as the list of default platforms. This option is set to
  False by default.
- ``increased_platform_scope``: This option is set to True by default, when
  disabled, twister will not increase platform coverage automatically and will
  only build and run tests on the specified platforms.
- ``default_platforms``: A list of additional default platforms to add. This list
  can either be used to replace the existing default platforms or can extend it
  depending on the value of ``override_default_platforms``.
- ``build_toolchains``: A mapping of platform names to the list of toolchains
  every test assigned to that platform should be built with. Twister creates one
  test instance per toolchain, each in its own build directory. This sets, or
  overrides, the ``build_toolchains`` option of the board definition; an empty
  list disables multi-toolchain builds for a platform that requests them. Since
  this multiplies build time, it is typically enabled only in the configuration
  file used by CI (``tests/test_config_ci.yaml``) so that local runs keep
  building each test once. See :ref:`twister_toolchain_selection`.

And example platforms configuration:

.. code-block:: yaml

	platforms:
	  override_default_platforms: true
	  increased_platform_scope: false
	  default_platforms:
	    - qemu_x86
	  build_toolchains:
	    native_sim:
	      - host/gnu
	      - host/llvm


Test Level Configuration
========================

The test configuration allows defining test levels, level dependencies and
additional inclusion of tests into a specific test level if the test itself
does not have this information already.

In the configuration file you can include complete components using
regular expressions and you can specify which test level to import from
the same file, making management of levels simple.

And example test level configuration:

.. code-block:: yaml

	levels:
	  - name: my-test-level
	    description: >
	      my custom test level
	    adds:
	      - kernel.threads.*
	      - kernel.timer.behavior
	      - arch.interrupt
	      - boards.*


Combined configuration
======================

To mix the Platform and level configuration, you can take an example as below:

An example platforms plus level configuration:

.. code-block:: yaml

	platforms:
	  override_default_platforms: true
	  default_platforms:
	    - frdm_k64f
	levels:
	  - name: smoke
	    description: >
	        A plan to be used verifying basic zephyr features.
	  - name: unit
	    description: >
	        A plan to be used verifying unit test.
	  - name: integration
	    description: >
	        A plan to be used verifying integration.
	  - name: acceptance
	    description: >
	        A plan to be used verifying acceptance.
	  - name: system
	    description: >
	        A plan to be used verifying system.
	  - name: regression
	    description: >
	        A plan to be used verifying regression.


To run with above test_config.yaml file, only default_platforms with given test level
test scenarios will run.

.. code-block:: console

   $ west twister --test-config=<path to>/test_config.yaml -T tests --level="smoke"
