.. _snippets:

片段
########

片段是一种将构建系统设置保存在一处、然后在构建任何
Zephyr 应用时使用这些设置的方式。当通用配置适用于
多个不同应用时，这让你可以单独保存这些配置。

片段的一些示例使用场景是：

- 将开发板的控制台后端从"真实"UART 更改为 USB CDC-ACM UART
- 启用经常使用的调试选项
- 将相互关联的配置设置应用到 AMP SoC 上的"主"CPU 和协处理器核心

以下页面记录这个功能。

.. toctree::
   :maxdepth: 1

   using.rst
   /snippets/index.rst
   writing.rst
   design.rst
