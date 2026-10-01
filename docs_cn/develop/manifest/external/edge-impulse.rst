.. _external_module_edge_impulse:

Zephyr 的 Edge Impulse SDK
############################

概述
****

Edge Impulse 是一个领先的边缘 AI 设计与开发平台，用于将机器学习部署到边缘设备。Zephyr 的 Edge Impulse SDK 将 Edge Impulse 推理 SDK 打包为 Zephyr 模块，便于与 Zephyr 构建系统集成。`在此 <https://www.edgeimpulse.com/signup>`_ 注册免费账户。

该模块将 Edge Impulse 推理 SDK 打包为 Zephyr 模块，便于与 Zephyr 构建系统集成。它还可以提供 west 扩展命令，用于在 Edge Impulse 平台上构建并下载模型部署产物到工作区，以便集成到 Zephyr 应用中。

Edge Impulse SDK 采用 `BSD-3-Clause-Clear 许可
<https://github.com/edgeimpulse/edge-impulse-sdk-zephyr?tab=BSD-3-Clause-Clear-1-ov-file>`_。
请注意，Edge Impulse 云服务至少需要一个免费层级账户或公开项目的 api-key；定价和服务条款请参见 `Edge Impulse 网站 <https://edgeimpulse.com>`_。

将模块添加到项目
****************

要使用该模块，在 Zephyr 子 manifest 中添加以下条目（将 ``v1.82.3`` 替换为所需版本），然后运行 ``west update``，或者将其添加到项目的 ``west.yml`` manifest：

.. code-block:: yaml

   manifest:
     projects:
       - name: edge-impulse-sdk-zephyr
         url: https://github.com/edgeimpulse/edge-impulse-sdk-zephyr
         revision: v1.82.3
         path: modules/edge-impulse-sdk-zephyr
         west-commands: west/west-commands.yml

在 Zephyr 中使用
****************

构建和部署 Edge Impulse 模型可使用提供的 west 扩展命令，也可手动操作。
详细步骤请参见 `Edge Impulse Zephyr 模块部署`_。

**West 扩展命令：**

- ``west ei-build``：触发 Studio 构建，支持可选参数（``-e tflite-eon``、``-t int8``、``-i 1``）
- ``west ei-deploy``：下载预构建的部署产物
- 两者都需要 ``-k``（API key）和 ``-p``（项目 ID）选项

有关将 Edge Impulse 与 Zephyr 集成的分步教程和指南，请参见 `Edge Impulse Zephyr 模块部署`_。

参考资料
********

.. target-notes::

.. _Edge Impulse Zephyr 模块部署:
   https://docs.edgeimpulse.com/hardware/deployments/run-zephyr-module
