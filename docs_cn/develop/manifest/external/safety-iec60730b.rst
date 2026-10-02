.. _external_module_safety_iec60730b:

IEC 60730 B 类安全测试子系统
#############################

简介
****

`safety_iec60730b`_ 是一个 Zephyr :ref:`module <modules>`，提供可从 Zephyr 应用运行 IEC 60730 B 类安全自检的测试子系统。

`IEC 60730-1`_ 是一项国际标准，定义了家用电器及类似设备中使用的自动电气控制的安全要求。附录 H B 类描述了控制器必须实现的软件故障/错误检测措施，用于检测可能导致危险误动作的随机硬件故障。

该子系统通过单一、厂商中立的 API 暴露这些"持续执行"的自检，通过 Kconfig 和设备驱动模型与 Zephyr 集成，并将实际测试执行委托给可选择的后端。NXP SoC 上的默认后端是 `NXP IEC 60730 B 类安全库`_。

以下 B 类测试例程被暴露，每个都可通过 Kconfig 单独选择：

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 测试
     - Kconfig 符号
     - 检测的故障
   * - CPU 寄存器
     - ``CONFIG_IEC60730B_TEST_CPU``
     - 核心寄存器中的固定型（stuck-at）故障
   * - FPU 寄存器
     - ``CONFIG_IEC60730B_TEST_FPU``
     - 浮点寄存器中的固定型（stuck-at）故障
   * - 程序计数器
     - ``CONFIG_IEC60730B_TEST_PC``
     - 程序计数器损坏、非法执行流
   * - RAM
     - ``CONFIG_IEC60730B_TEST_RAM``
     - RAM 单元故障，使用 March C / March X 算法
   * - Flash / ROM
     - ``CONFIG_IEC60730B_TEST_FLASH``
     - 不可变存储器损坏，使用 CRC16 / CRC32
   * - 栈
     - ``CONFIG_IEC60730B_TEST_STACK``
     - 栈溢出和栈下溢
   * - 时钟
     - ``CONFIG_IEC60730B_TEST_CLOCK``
     - 系统时钟漂移，对照独立计数器测量
   * - 模拟 I/O
     - ``CONFIG_IEC60730B_TEST_AIO``
     - ADC 信号通路故障，对照已知内部参考验证
   * - 数字 I/O
     - ``CONFIG_IEC60730B_TEST_DIO``
     - GPIO 固定型（stuck-at）故障和短路
   * - 看门狗
     - ``CONFIG_IEC60730B_TEST_WDOG``
     - 看门狗超时和复位生成

在该 API 背后，测试例程来自三个可互换的硬件抽象层（HAL）后端之一：

* **NXP HAL**（``CONFIG_IEC60730B_HAL_NXP``）调用同一仓库中随附的经预认证的 NXP IEC 60730 B 类裸机安全库。它在 NXP SoC 上默认被选中，由经认证的实现支撑。
* **Zephyr HAL**（``CONFIG_IEC60730B_HAL_ZEPHYR``）在标准 Zephyr 驱动 API 之上实现相同的测试，使该子系统可在任何 Zephyr 支持的平台上使用。它在非 NXP SoC 上是默认选择。
* **无 HAL**（``CONFIG_IEC60730B_HAL_NONE``）仅构建弱桩（weak stubs），因此每个测试都返回 ``IEC60730B_TEST_NOT_SUPPORTED``。可将其作为自定义后端的起点：实现公共头文件中声明的函数，它们在链接时会覆盖弱函数。

.. warning::

   Zephyr HAL 为实验性。它不使用任何厂商认证库，其代码均未通过 IEC 60730 B 类认证。用户有责任在其特定应用和目标平台上使用前，自行评估、验证和认证所有代码，方可用于任何安全关键产品。

测试子系统、其 HAL 后端、示例和模块元数据（``zephyr/`` 下的所有内容）采用 Apache-2.0 许可。作为后端使用的 NXP 安全库（``source/`` 下的所有内容）采用 *LA_OPT_Online Code Hosting NXP_Software_License* 分发；完整文本请参见仓库中的 ``IEC60730-LICENSE.txt``。

在 Zephyr 中使用
****************

将模块添加到现有工作区
========================

将模块作为 West 项目添加到 ``west.yml`` manifest，或通过子 manifest（例如 :file:`zephyr/submanifests/iec60730b.yaml`）引入，内容如下：

.. code-block:: yaml

   manifest:
     projects:
       - name: safety_iec60730b
         url: https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b
         revision: main_github
         path: modules/safety/iec60730b # adjust the path as needed

然后拉取：

.. code-block:: console

   west update safety_iec60730b

创建独立工作区
==============

该仓库还自带自己的 manifest，会拉入 Zephyr 本身以及该模块所需的 HAL：

.. code-block:: console

   west init -m https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b <workspace>
   cd <workspace>
   west update

配置
====

在应用 :file:`prj.conf` 中启用测试子系统：

.. code-block:: cfg

   CONFIG_IEC60730B=y

所有测试例程默认启用。禁用不需要的项，必要时覆盖自动 HAL 选择。

应用接口
========

公共 API 声明在 ``iec60730b_test.h`` 中，该模块会将其添加到应用 include 路径。包含该头文件并直接调用测试函数，通常分为启动前执行一次的启动测试，和从专用安全线程或中断中周期性执行的运行时测试。每个函数成功时返回 ``0``，检测到故障时返回负错误码，测试被禁用或在目标上不可用时返回 ``IEC60730B_TEST_NOT_SUPPORTED``。

示例应用
========

``zephyr/samples/safety/`` 下的 ``safety`` 示例是参考集成。它运行完整的启动和运行时测试集，在控制台报告每个结果，喂给 Zephyr 任务看门狗通道，并在安全线程存活期间闪烁 LED。

从工作区根目录为受支持的板之一构建并烧录：

.. code-block:: console

   west build -p -b frdm_mcxa266 modules/safety/iec60730b/zephyr/samples/safety
   west flash

该示例在看门狗测试中故意让看门狗超时，因此板会复位一次，启动横幅和启动测试结果会出现两次。

参考资料
********

.. target-notes::

.. _safety_iec60730b:
   https://github.com/nxp-mcuxpresso/mcux-safety-iec60730b

.. _IEC 60730-1:
   https://webstore.iec.ch/publication/66089

.. _NXP IEC 60730 B 类安全库:
   https://www.nxp.com/applications/technologies/functional-safety/iec-60730-safety-standard-for-household-appliances:APIEC60730
