.. _requirements_catalog:

需求目录
####################

Zephyr 的需求维护在专用的 ``reqmgmt`` 仓库中，
使用 `StrictDoc <https://github.com/strictdoc-project/strictdoc>`__ 管理。当该
仓库存在于工作区中（作为 west 项目被拉取进来）时，其
需求会被导出并直接渲染到本文档下方。

.. only:: reqmgmt

   .. toctree::
      :maxdepth: 2

      /build/requirements/index

.. only:: not reqmgmt

   由于工作区中不存在 ``reqmgmt``
   模块，本次构建未包含这些需求。请参见
   `Zephyr Project Requirements <https://zephyrproject-rtos.github.io/reqmgmt/>`__
   查看已发布的版本。
