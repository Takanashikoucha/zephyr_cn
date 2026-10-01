.. _external_module_mender_mcu:

mender-mcu
##########

简介
****

`mender-mcu`_ 通过集成 Zephyr，为资源受限设备提供健壮的固件更新。它实现了 Update Module 接口，允许模块定义如何处理更新的具体细节。mender-mcu 提供一个默认 Update Module，与 MCUboot 集成以提供 A/B 更新。这使得微控制器（MCU）能够执行原子、防失败的 OTA 更新，失败时自动回滚，类似于 Mender 对 Linux 设备的更新。

客户端与 Mender 服务器通信，报告设备清单和身份，检查可用更新，下载新固件，并与 Update Module 协作安全地安装更新。Mender 服务器提供采用 Apache-2.0 许可的开源版本，以及采用商业许可的企业版本，可通过商业计划获取，支持本地托管和 Mender 托管（全托管服务）。

mender-mcu 采用 Apache-2.0 许可。

要求
****

* 用于 JSON 解析的 cJSON

在 Zephyr 中使用
****************

要将 mender-mcu 作为 Zephyr :ref:`module <modules>` 引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/mender-mcu.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: mender-mcu
         url: https://github.com/mendersoftware/mender-mcu
         revision: main
         path: modules/mender-mcu # 根据需要调整路径

更详细的步骤和 API 文档请参阅 `mender-mcu 文档`_。`Zephyr 参考项目`_ 提供了一个示例参考集成。

参考资料
********

.. target-notes::

.. _mender-mcu:
   https://github.com/mendersoftware/mender-mcu

.. _mender-mcu 文档:
   https://docs.mender.io/operating-system-updates-zephyr

.. _Zephyr 参考项目:
   https://github.com/mendersoftware/mender-mcu-integration
