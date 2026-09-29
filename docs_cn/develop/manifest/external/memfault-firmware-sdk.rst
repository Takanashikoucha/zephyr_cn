.. _external_module_memfault_firmware_sdk:

memfault-firmware-sdk
#####################

简介
****

`memfault-firmware-sdk`_ 为嵌入式开发者提供内置的远程调试、性能监控
和 OTA 更新能力，面向基于 MCU 的设备。它自动从现场设备捕获崩溃报告、
日志和堆栈跟踪，便于在无需物理接触的情况下诊断问题。该 SDK 还收集
轻量级性能指标，如内存使用、电池续航、连接性和固件稳定性，以长期跟踪
车队可靠性。

该 SDK 与 `Memfault`_ 平台通信，平台聚合这些数据，帮助团队更快
地优先处理和解决问题。此外，该 SDK 支持空中固件更新，可实现受控
发布和新版本远程部署。

该 SDK 受自定义 BSD 风格许可保护，附带服务特定的使用限制。更多细节
请参见 `Memfault Firmware SDK 许可`_。

在 Zephyr 中使用
****************

要将 ``memfault-firmware-sdk`` 作为 Zephyr :ref:`module <modules>`
引入，将其作为 West 项目添加到 :file:`west.yaml` 文件，内容如下，
然后运行 :command:`west update`：

.. code-block:: yaml

   manifest:
     remotes:
       # Add the Memfault GitHub repo
       - name: memfault
         url-base: https://github.com/memfault
     projects:
       # Add the Memfault SDK
       - name: memfault-firmware-sdk
         path: modules/lib/memfault-firmware-sdk
         revision: 1.33.0
         remote: memfault

.. note::

   上面显示的 revision 仅为示例。请查看 `memfault-firmware-sdk`_
   的 releases 页面获取最新的 release tag，确保使用所需版本。

更详细的步骤和 API 文档请参阅 `memfault-firmware-sdk 文档`_ 以及
提供的 `memfault-firmware-sdk 示例`_。

参考资料
********

.. _memfault-firmware-sdk:
   https://github.com/memfault/memfault-firmware-sdk

.. _Memfault Firmware SDK 许可:
   https://github.com/memfault/memfault-firmware-sdk/blob/master/LICENSE

.. _memfault-firmware-sdk 文档:
    https://docs.memfault.com/docs/mcu/introduction

.. _memfault-firmware-sdk Zephyr 指南:
   https://docs.memfault.com/docs/mcu/zephyr-guide

.. _memfault-firmware-sdk 示例:
   https://github.com/memfault/memfault-firmware-sdk/tree/master/examples

.. _Memfault:
   https://memfault.com/
