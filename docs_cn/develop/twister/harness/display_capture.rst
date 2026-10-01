.. _twister_display_capture_harness:

显示捕获
###########

``display_capture`` 测试框架用于通过摄像头捕获并分析显示输出，以验证显示驱动程序的功能。它与 pytest 集成，使用视频指纹执行自动化视觉测试。

.. figure:: figures/twister_display_capture_success.webp
   :align: center
   :alt: 显示设备显示屏摄像头预览的窗口，四角有彩色方块，文字叠加层指示测试匹配成功。

    "compare"（比较）运行中显示的窗口，指纹与参考指纹匹配度为 90%。

硬件配置
==============

显示捕获测试框架需要：

- 至少 200 万像素的 UVC 兼容摄像头（例如 1080p 分辨率）
- 遮光外壳或黑色窗帘，以确保光照一致
- 连接摄像头的 PC 主机，用于捕获显示输出
- 连接到同一 PC 的被测设备（DUT），用于烧录和串口控制台访问

配置
============

该测试框架使用 YAML 配置文件，定义摄像头设置、测试参数和视频签名分析选项。典型配置如下：

.. code-block:: yaml
   :caption: display_config.yaml

    case_config:
      device_id: 0
      res_x: 1280
      res_y: 720
      fps: 30
      run_time: 20
    test:
      timeout: 30
      prompt: "screen starts"
      expect: ["tests.drivers.display.check.shield"]
    plugins:
      - name: signature
        module: plugins.signature_plugin
        class: VideoSignaturePlugin
        status: enable
        config:
          operations: "compare"  # 或 "generate"
          metadata:
            name: "tests.drivers.display.check.shield"
            platform: "frdm_mcxn947"
          directory: "./fingerprints"
          duration: 100
          method: "combined"
          threshold: 0.65
          phash_weight: 0.35
          dhash_weight: 0.25
          histogram_weight: 0.2
          edge_ratio_weight: 0.1
          gradient_hist_weight: 0.1

- ``case_config`` - 本节定义通用的摄像头设置和测试时长。

  - ``device_id`` - 摄像头设备 ID（默认为 0）。任何有效的 OpenCV 摄像头标识符均可，可以是：

    - 本地摄像头的整数（第一台摄像头用 0，第二台用 1，依此类推）。
    - Linux 上的设备路径字符串，例如 ``/dev/video0``。
    - 网络摄像头的 IP 视频流 URL，例如 ``rtsp://192.168.1.100:8554/stream``。

  - ``res_x`` - 摄像头的水平分辨率（整数，默认为 1280）。
  - ``res_y`` - 摄像头的垂直分辨率（整数，默认为 720）。
  - ``fps`` - 摄像头的每秒帧数（整数，默认为 30）。
  - ``run_time`` - 测试时长（秒）（整数，默认为 20）。

- ``test`` - 本节包含与设备交互相关的测试配置。

  - ``timeout`` - 等待提示符出现在设备 UART 输出上的最大时间（秒）（整数，默认为 30）。
  - ``prompt`` - 开始显示捕获前在设备 UART 输出中等待的字符串模式。可以是正则表达式（字符串，默认为 ``uart:~$``）。
  - ``expect`` - 必须与应用返回的测试结果匹配的期望字符串列表。如果捕获的结果与该列表匹配，则测试通过（字符串列表，默认为 ``['PASS']``）。

- ``plugins`` - 本节包含处理摄像头帧的插件配置。目前仅支持 ``VideoSignaturePlugin`` 插件，其接受以下配置选项：

  - ``operations`` - 运行测试时执行的操作（字符串）。必须设为 ``generate``（生成指纹）或 ``compare``（将捕获的指纹与参考指纹比较）。
  - ``metadata`` - 用于指纹识别的元数据信息（可选）。

    - ``name`` - 测试用例名称标识符（字符串）。
    - ``platform`` - 目标平台标识符（字符串）。

  - ``directory`` - 存储指纹的目录（字符串，默认为 ``./fingerprints``）。
  - ``duration`` - 分析的帧数（整数）。帧数越多耗时越长，但生成的指纹更准确。
  - ``method`` - 生成显示指纹的方法（字符串，默认为 ``combined``）。必须设为以下值之一：``phash``、``dhash``、``histogram`` 或 ``combined``。

    ``phash``（感知哈希）
      捕获整体视觉结构和布局。最适合检测主要渲染问题，例如 UI 元素位置不正确。
    ``dhash``（差异哈希）
      检测亮度模式和渐变。对对比度变化敏感，例如亮度或对比度问题。
    ``histogram``（颜色直方图）
      分析颜色分布。能快速检测明显的颜色问题，例如颜色交换缺陷。
    ``combined``（推荐方法）
      对所有方法进行加权（参见下方 :samp:`{method}_weight` 选项），以进行稳健比较。能平衡检测主要和细微的视觉问题。

  - ``threshold`` - 相似度分数阈值，高于该值即认为参考指纹与捕获的指纹之间存在匹配（可选浮点数，默认为 0.65）。
  - ``phash_weight`` - phash 方法的权重（可选浮点数，默认为 0.35）。
  - ``dhash_weight`` - dhash 方法的权重（可选浮点数，默认为 0.25）。
  - ``histogram_weight`` - histogram 方法的权重（可选浮点数，默认为 0.2）。
  - ``gradient_hist_weight`` - 梯度直方图方法的权重（可选浮点数，默认为 0.1）。
  - ``edge_ratio_weight`` - 边缘比率方法的权重（可选浮点数，默认为 0.1）。

配置文件路径在测试的 ``testcase.yaml`` 中通过 :envvar:`DISPLAY_TEST_DIR` 环境变量使用 ``display_capture_config`` 测试框架配置选项指定：

.. code-block:: yaml

    harness: display_capture
    harness_config:
      pytest_dut_scope: session
      fixture: fixture_display
      display_capture_config: "${DISPLAY_TEST_DIR}/display_config.yaml"

工作流程
========

首先，为已知良好的显示输出生成**参考指纹**：

.. code-block:: bash

    # 构建并烧录显示测试
    west build -b <board> tests/drivers/display/display_check
    west flash

    # 通过将配置文件中的 'operations' 字段设为 'generate' 来配置指纹生成模式

    # 生成指纹
    export DISPLAY_TEST_DIR=<path-to-config-directory>
    west twister --device-testing --hardware-map map.yml \
        -T tests/drivers/display/display_check/

指纹存储在配置文件的 ``directory`` 字段指定的目录中，并按配置文件 ``metadata`` 字段定义的测试名称和平台进行组织。

生成指纹后，可以再次运行测试，这次以**比较模式**运行：

.. code-block:: bash

    # 将配置文件中的 'operations' 字段设为 'compare'

    export DISPLAY_TEST_DIR=<path-to-fingerprints-parent-directory>
    west twister --device-testing --hardware-map map.yml \
        -T tests/drivers/display/display_check/

该测试框架使用配置的签名方法和阈值，将捕获的视频与参考指纹进行比较。如果参考指纹与捕获指纹之间的相似度分数超过配置的 ``threshold``，则测试通过。

.. note::

   - 被测设备（DUT）的 ``testcase.yaml`` 中的测试名称必须与指纹元数据配置中的 ``name`` 字段匹配。
   - 一个目录中可以存储多个指纹以进行综合验证，尽管这会增加比较时间。
   - 指纹对测试场景和平台均具有特定性。
