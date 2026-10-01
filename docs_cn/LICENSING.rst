:orphan:

.. _zephyr_licensing:

Zephyr 项目组件的许可
######################################

Zephyr 整体采用 `Apache 2.0 License`_ 许可。但它确实导入或复用了少量受其他许可证覆盖的包、脚本和其他文件。在某些情况下，无法为这些文件添加许可证头，因此它们的许可信息以机器可读的形式集中声明在仓库根目录的 :zephyr_file:`REUSE.toml` 文件中（遵循 `REUSE specification`_）。

下面的章节由该元数据**自动生成**，因此始终反映代码树的实际状态。要添加、更新或删除条目，请编辑 :zephyr_file:`REUSE.toml` 中对应的 ``[[annotations]]`` 块，而不是本页（参见 :ref:`external-contributions`）。

.. note::

   本页仅列出许可*例外*。它**不**定义 Zephyr 项目本身的许可证，该许可证是 Apache 2.0，如仓库根目录的 :zephyr_file:`LICENSE` 文件所规定。

.. contents:: 已记录的组件
   :local:
   :depth: 1

.. zephyr-licensing-exceptions::

.. _Apache 2.0 License:
   https://github.com/zephyrproject-rtos/zephyr/blob/main/LICENSE

.. _REUSE specification:
   https://reuse.software/spec/
