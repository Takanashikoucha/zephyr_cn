.. _external_module_executorch:

ExecuTorch
##########

简介
****

`ExecuTorch <https://github.com/pytorch/executorch>`_ 是 PyTorch 的设备上推理运行时。在 Zephyr 中，可作为外部模块集成，在 CPU 和 Arm Ethos-U NPU 上运行模型。

如果您刚接触 ExecuTorch，以下资源是很好的学习起点：

- `ExecuTorch 工作原理 <https://docs.pytorch.org/executorch/stable/intro-how-it-works.html>`_
- `入门 架构概述
  <https://docs.pytorch.org/executorch/stable/getting-started-architecture.html>`_

ExecuTorch 采用 `BSD 3-Clause 许可
<https://github.com/pytorch/executorch/blob/main/LICENSE>`_。

在 Zephyr 中使用
****************

本节介绍 ExecuTorch 模块注册、模型准备，以及 CPU 和 Arm Ethos-U NPU 两种目标的构建/运行步骤。

.. note::

   **前置条件**

   - **Python 3.12–3.13** — ExecuTorch 工具链所需。请使用单独的虚拟环境，或使用兼容 Python 版本创建的 Zephyr 虚拟环境。
   - **Arm FVP** — 仅当以 Corstone FVP（例如 ``mps3/corstone300/fvp``）为目标时才需要，用于在无物理硬件的情况下仿真 Cortex-M 和 Ethos-U NPU。安装步骤参见 :ref:`安装 Arm FVP <fvp-install>`。
   - **Docker（仅限 macOS）** — 仅当通过 `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ 走 Arm Ethos-U NPU 推理流程时才需要。

安装 ExecuTorch
================

**步骤 1：** 在 west manifest 中添加以下项目条目，将 ExecuTorch 注册为外部模块。可以创建专门的子 manifest 文件 ``zephyrproject/zephyr/submanifests/executorch.yaml``，或直接添加到应用现有的 ``west.yml``：

.. code-block:: yaml

   manifest:
     projects:
       - name: executorch
         url: https://github.com/pytorch/executorch
         revision: v1.2.0
         path: modules/lib/executorch
         submodules: true

**步骤 2：** 运行 west update：

.. code-block:: console

   west update

**步骤 3：** 安装 ExecuTorch 及依赖：

.. note::

   请在 Python 版本兼容（3.12–3.13）的 Zephyr 虚拟环境中运行这些命令。

.. code-block:: console

   pip install executorch==1.2.0
   pip install tosa-tools==2026.2.1
   pip install ethos-u-vela==5.0.0

构建并运行
==========

在嵌入式设备上运行 AI 模型时，目标硬件可能包含专用 AI 加速器——通常称为 NPU（神经网络处理单元）。Arm 提供 `Ethos-U NPU 家族 <https://www.arm.com/products/silicon-ip-cpu?families=ethos%20npus>`_ 用于高效的设备上 AI 推理。下面的标签页涵盖两条路径：以 Ethos-U NPU 为目标的加速推理，以及无 NPU 设备的纯 CPU 推理。

.. _fvp-install:

.. tabs::

   .. group-tab:: Arm Ethos-U NPU 推理

      .. note::

         **安装 Arm FVP**

         固定虚拟平台（FVP）是 Arm 提供的仿真器，可在无物理硬件的情况下运行 Zephyr。此处需要通过 Corstone-300 参考平台仿真 Ethos-U55/U65/U85 加速器，因此必须安装。

         .. tabs::

            .. group-tab:: Ubuntu

               **步骤 1：** 从 Arm FVP 页面下载 Corstone-300 的 FVP 安装程序。FVP 可安装在机器上的任意位置——不需要放在 Zephyr 项目目录内。

               `Arm Corstone FVP
               <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_

               .. note::

                  FVP 版本号随每次发布变化。请从 Arm 下载页面将文件名和 URL 设置为您想要的版本。

                  .. code-block:: console

                     FVP_TGZ="FVP_Corstone_SSE-300_11.27_42_Linux64_armv8l.tgz"
                     FVP_URL="https://developer.arm.com/-/cdn-downloads/permalink/FVPs-Corstone-IoT/Corstone-300/${FVP_TGZ}"
                     curl -L -o "${FVP_TGZ}" "${FVP_URL}"

               **步骤 2：** 解压下载的归档：

               .. code-block:: console

                  tar -xf "${FVP_TGZ}"

               **步骤 3：** 运行安装脚本：

               .. code-block:: console

                  ./FVP_Corstone_SSE-300.sh --i-agree-to-the-contained-eula --no-interactive -q

               **步骤 4：** 将 FVP 添加到 ``PATH``。``FVP_Corstone_SSE-300_Ethos-U55`` 和 ``FVP_Corstone_SSE-300_Ethos-U65`` 位于同一目录：

               .. code-block:: console

                  export PATH=$HOME/FVP_Corstone_SSE-300/models/Linux64_armv8l_GCC-9.3:$PATH

               **步骤 5：** 通过 source 提供的脚本安装所需的运行时依赖（``libpython3.9.so.1.0``）。不同 shell 的方法略有差异：

               *bash：*

               .. code-block:: console

                  source $HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  unset PYTHONHOME

               *zsh：* source 之前必须手动设置 ``BASH_SOURCE``，因为 zsh 不会自动填充它：

               .. code-block:: console

                  BASH_SOURCE=$HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  source $HOME/FVP_Corstone_SSE-300/scripts/runtime.sh
                  unset PYTHONHOME

               **步骤 6：** 验证安装：

               .. code-block:: console

                  FVP_Corstone_SSE-300_Ethos-U55 --version
                  FVP_Corstone_SSE-300_Ethos-U65 --version

            .. group-tab:: macOS

               在 macOS 上，FVP 通过 `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ 项目提供的 Docker 包装器运行。

               **步骤 1：** 克隆仓库并检出所需 commit。仓库可克隆到机器上的任意位置——不需要放在 Zephyr 项目目录内。

               .. code-block:: console

                  git clone https://github.com/Arm-Examples/FVPs-on-Mac.git

               .. code-block:: console

                  cd FVPs-on-Mac
                  git switch --detach 1458860

               **步骤 2：** 构建 Docker 包装器：

               .. code-block:: console

                  ./build.sh

               .. note::

                  在 macOS 上执行包装器构建和 FVP 命令之前，必须已安装并运行 Docker。

               **步骤 3：** 对构建做健全性检查：

               .. code-block:: console

                  ./bin/FVP_Corstone_SSE-300 --version

               **步骤 4：** 将 FVP 二进制文件暴露给环境：

               .. code-block:: console

                  export PATH=$PATH:$(pwd)/bin

            .. group-tab:: Windows

               **步骤 1：** 从 Arm FVP 页面下载 Corstone-300 的 FVP 安装程序。FVP 可安装在机器上的任意位置——不需要放在 Zephyr 项目目录内。

               `Arm FVP
               <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_

               选择 Windows 安装程序并运行。按照安装向导操作。FVP 二进制文件通常安装到类似 ``C:\Program Files\ARM\FVP_Corstone_SSE-300\models\Win64_VC2019`` 的路径。

               .. note::

                  如果没有 ``python39.dll``，可能还需要安装它

               **步骤 2：** 打开新的 PowerShell 窗口并验证安装：

               .. code-block:: console

                  .\FVP_Corstone_SSE-300.exe --version

            .. group-tab:: Zephyr Docker CI

               `Zephyr Docker CI 镜像 <https://github.com/zephyrproject-rtos/docker-image>`_ 是手动安装 FVP 的替代方案。它是 Zephyr 官方 CI 容器，已包含 Corstone-300 和 Corstone-320 FVP 以及所有其他 Zephyr 构建依赖——无需单独安装 FVP。

               **步骤 1：** 拉取镜像：

               .. code-block:: console

                  docker pull ghcr.io/zephyrproject-rtos/zephyr-build:main

               **步骤 2：** 挂载 Zephyr 工作区和 Zephyr SDK 启动容器：

               .. code-block:: console

                  docker run -it --rm \
                    -v $HOME/zephyrproject:$HOME/zephyrproject \
                    -v $HOME/zephyr-sdk-0.17.4:$HOME/zephyr-sdk-0.17.4 \
                    -w $HOME/zephyrproject \
                    -e HOME=$HOME \
                    -e ZEPHYR_SDK_INSTALL_DIR=$HOME/zephyr-sdk-0.17.4 \
                    --user root \
                    --entrypoint /bin/bash \
                    ghcr.io/zephyrproject-rtos/zephyr-build:main

               .. note::

                  SDK 版本（``0.17.4``）可能变化。请替换为您安装的版本，或使用通用形式：

                  .. code-block:: console

                     docker run -it --rm \
                       -v $HOME/zephyrproject:$HOME/zephyrproject \
                       -v $HOME/zephyr-sdk-<version>:$HOME/zephyr-sdk-<version> \
                       -w $HOME/zephyrproject \
                       -e HOME=$HOME \
                       -e ZEPHYR_SDK_INSTALL_DIR=$HOME/zephyr-sdk-<version> \
                       --user root \
                       --entrypoint /bin/bash \
                       ghcr.io/zephyrproject-rtos/zephyr-build:main

               **步骤 3：** 在容器内激活 Zephyr 虚拟环境：

               .. code-block:: console

                  source $HOME/zephyrproject/.venv/bin/activate

               **步骤 4：** 验证 FVP 可用：

               .. code-block:: console

                  FVP_Corstone_SSE-300 --version
                  FVP_Corstone_SSE-320 --version

               之后即可在容器内运行任意 ``west build`` 命令，与下文构建步骤中的描述完全一致。

      .. rubric:: 准备 Ethos-U55 PTE 模型

      在 ExecuTorch 中，``.pte`` 文件是序列化程序文件，是部署 PyTorch 模型到边缘和移动设备的最终二进制格式。有关使用 Arm Ethos-U 后端导出和降低（lowering）自己的 PyTorch 模型的指导，请参见 `使用 ExecuTorch Export <https://docs.pytorch.org/executorch/stable/using-executorch-export.html>`_。

      此处使用的模型是一个最小的 ``add`` 模型，接收两个张量并逐元素相加。它的存在纯粹是为了验证完整的 ExecuTorch 工作流运行正确——从模型编译到通过 Ethos-U NPU 进行设备上推理。预期输出是每个元素等于 ``2 + 2 = 4``。

      从 Zephyr 根目录（例如 ``~/zephyrproject``）运行：

      .. tabs::

         .. group-tab:: Ubuntu/macOS

            .. code-block:: console

               cd ~/zephyrproject
               python -m modules.lib.executorch.examples.arm.aot_arm_compiler \
                 --model_name=modules/lib/executorch/examples/arm/example_modules/add.py \
                 --quantize --delegate -t ethos-u55-128 --output=add_u55_128.pte

         .. group-tab:: Windows

            .. code-block:: console

               cd ~/zephyrproject
               python -m modules.lib.executorch.examples.arm.aot_arm_compiler `
                 --model_name=modules/lib/executorch/examples/arm/example_modules/add.py `
                 --quantize --delegate -t ethos-u55-128 --output=add_u55_128.pte

      ``--delegate`` 告诉 ``aot_arm_compiler`` 使用 Ethos-U 后端，``-t ethos-u55-128`` 选择 Ethos-U 变体和 MAC 数量。这些必须与您的硬件或 FVP 配置匹配。

      .. rubric:: 构建并运行

      从 Zephyr 根目录（``~/zephyrproject``）运行：

      .. tabs::

         .. group-tab:: Ubuntu/macOS

            .. code-block:: console

               cd ~/zephyrproject
               west build -p auto -b mps3/corstone300/fvp \
                 modules/lib/executorch/zephyr/samples/hello-executorch \
                 -t run -- -DET_PTE_FILE_PATH=add_u55_128.pte

         .. group-tab:: Windows

            .. code-block:: console

               cd $env:USERPROFILE\zephyrproject
               west build -p auto -b mps3/corstone300/fvp `
                 modules/lib/executorch/zephyr/samples/hello-executorch -t run -- `
                 "-DET_PTE_FILE_PATH=$PWD\add_u55_128.pte"

   .. group-tab:: 纯 CPU 推理

      .. rubric:: 准备模型

      此处使用的模型是为 Cortex-M55 导出的最小 ``add`` 模型。本示例使用 ExecuTorch Arm AOT 编译器当前可用的纯 CPU 目标。支持的目标可能随时间变化。其他一些 Cortex-M 板也可能运行生成的 ``.pte``，前提是所需算子被运行时支持，但兼容性应按板逐一验证。从 Zephyr 根目录（例如 ``~/zephyrproject``）运行：

      .. code-block:: console

         python -m modules.lib.executorch.examples.arm.aot_arm_compiler \
           --model_name=modules/lib/executorch/examples/arm/example_modules/add.py \
           --quantize --target=cortex-m55+int8 --output=add_m55.pte

      .. rubric:: 构建并运行

      将 ``<board>`` 替换为目标板。对于下文未验证的板，应在目标上验证兼容性。

      .. code-block:: console

         west build -b <board> modules/lib/executorch/zephyr/samples/hello-executorch \
           -t run -- -DET_PTE_FILE_PATH=add_m55.pte

      .. note::

         该示例已在以下板上使用同一 ``add_m55.pte`` 产物测试通过：

         - **STM Nucleo-N657X0-Q**（``nucleo_n657x0_q``）：

           .. code-block:: console

              west build -b nucleo_n657x0_q \
                modules/lib/executorch/zephyr/samples/hello-executorch \
                -- -DET_PTE_FILE_PATH=add_m55.pte

         - **nRF5340 DK**（``nrf5340dk/nrf5340/cpuapp``）：

           .. code-block:: console

              west build -b nrf5340dk/nrf5340/cpuapp \
                modules/lib/executorch/zephyr/samples/hello-executorch \
                -- -DET_PTE_FILE_PATH=add_m55.pte

      构建后向硬件烧录：

      .. code-block:: console

         west flash

预期运行输出
============

.. code-block:: console

   I [executorch:arm_executor_runner.cpp:450 main()] Model executed successfully.
   I [executorch:arm_executor_runner.cpp:457 main()] Model outputs:
   I [executorch:arm_executor_runner.cpp:464 main()]   output[0]: tensor scalar_type=Float numel=5
   I [executorch:arm_executor_runner.cpp:481 main()]     [0] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [1] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [2] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [3] = 4.000000
   I [executorch:arm_executor_runner.cpp:481 main()]     [4] = 4.000000
   I [executorch:arm_executor_runner.cpp:499 main()] SUCCESS: Program complete, exiting.

``output`` 值 ``4.000000`` 确认模型已在设备上成功运行，每个元素都是 ``2 + 2`` 的结果，由 Ethos-U NPU 或 CPU 后端通过 ExecuTorch 计算得出。

Zephyr 上的 ExecuTorch 正在积极开发中，更复杂、更有意思的示例应用即将到来。您可以在这里跟踪进度并找到新示例：`ExecuTorch Zephyr 示例 <https://github.com/pytorch/executorch/tree/main/zephyr/samples>`_。

参考资料
********

- `ExecuTorch <https://github.com/pytorch/executorch>`_ — PyTorch 的设备上推理运行时。
- `ExecuTorch 工作原理 <https://docs.pytorch.org/executorch/stable/intro-how-it-works.html>`_ — ExecuTorch 工作流入门。
- `入门 架构 <https://docs.pytorch.org/executorch/stable/getting-started-architecture.html>`_ — ExecuTorch 高层架构概述。
- `Arm FVP <https://developer.arm.com/Tools%20and%20Software/Fixed%20Virtual%20Platforms/IoT%20FVPs>`_ — 用于 Cortex-M 和 Ethos-U 仿真的固定虚拟平台。
- `FVPs-on-Mac <https://github.com/Arm-Examples/FVPs-on-Mac.git>`_ — 使 Arm FVP 能在 macOS 上运行的 Docker 包装器。
- `Arm Ethos-U NPU 家族 <https://www.arm.com/products/silicon-ip-cpu?families=ethos%20npus>`_ — Arm 用于高效设备上 AI 推理的 NPU IP。
- `使用 ExecuTorch Export
  <https://docs.pytorch.org/executorch/stable/using-executorch-export.html>`_ — ExecuTorch 模型导出和后端 lowering 指南。
- `Zephyr Docker CI 镜像 <https://github.com/zephyrproject-rtos/docker-image>`_ — Zephyr 官方 CI 容器，包含预装 FVP 和构建依赖。
- `hello-executorch 示例
  <https://github.com/pytorch/executorch/tree/main/zephyr/samples/hello-executorch>`_ — 本指南使用的 Zephyr 最小 ExecuTorch 示例。
