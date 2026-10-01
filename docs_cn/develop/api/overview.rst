.. _api_overview:

API 概览
############

该表格列出了 Zephyr 的 API 及其相关信息，
包括它们当前的 :ref:`stability level <api_lifecycle>`。
关于主要发布版本之间 API 变更的更多细节，
可在 :ref:`zephyr_release_notes` 中查阅。

版本列使用 `semantic version <https://semver.org/>`_，
并有以下约定：

 * 主版本为零（0.y.z）用于初始开发阶段。
   任何内容都可能随时发生变更。
   公共 API 不应被视为稳定。

    * 如果次版本号不超过 1（0.1.z），
      该 API 被视为 :ref:`experimental <api_lifecycle_experimental>`。
    * 如果次版本号大于 1（0.y.z | y > 1），
      该 API 被视为 :ref:`unstable <api_lifecycle_unstable>`。

 * 版本 1.0.0 定义了公共 API。
   在此发布之后版本号递增的方式
   取决于该公共 API 及其变更情况。

    * 主版本号大于或等于 1（x.y.z | x >= 1）的 API
      被视为 :ref:`stable <api_lifecycle_stable>`。
    * Zephyr 中所有现有的稳定 API 都将从版本 1.0.0 开始。

 * 补丁版本 Z（x.y.Z | x > 0）
   如果仅引入向后兼容的缺陷修复，则必须递增。
   缺陷修复被定义为修复错误行为的内部变更。

 * 次版本 Y（x.Y.z | x > 0）
   如果向公共 API 引入新的向后兼容功能，则必须递增。
   如果任何公共 API 功能被标记为已弃用，则必须递增。
   如果在内部代码中引入了大量新功能或改进，则可以递增。
   它也可以包含补丁级别的变更。
   当次版本递增时，补丁版本必须重置为 0。

 * 主版本 X（x.Y.z | x > 0）
   如果对 API 进行了破坏兼容性的变更，则必须递增。

.. note::
   现有 API 的版本初始值基于 API 的当前状态设定：

     - 0.1.0 表示 :ref:`experimental <api_lifecycle_experimental>` API
     - 0.8.0 表示 :ref:`unstable <api_lifecycle_unstable>` API，
     - 最后 1.0.0 表示 :ref:`stable <api_lifecycle_stable>` API。

   未来对 API 的变更将需要按照上述指南调整版本号。


.. api-overview-table::