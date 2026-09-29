.. _toolchain_intel_oneapi_toolkit:

Intel
oneAPI
Toolkit
####################

#. 下载
   `Intel
   oneAPI
   Base
   Toolkit
   <https://software.intel.com/content/www/us/en/develop/tools/oneapi/all-toolkits.html>`_

#. 假设
   工具
   套件
   安装
   在
   ``/opt/intel/oneApi``，
   用
   以下
   设置
   环境
   using::

      #
      Linux,
      macOS:
      export
      ONEAPI_TOOLCHAIN_PATH=/opt/intel/oneapi
      source
      $ONEAPI_TOOLCHAIN_PATH/compiler/latest/env/vars.sh

      #
      Windows:
      >
      set
      ONEAPI_TOOLCHAIN_PATH=C:\Users\Intel\oneapi

   要
   设置
   完整
   的
   oneApi
   环境，
   用::

      source
      /opt/intel/oneapi/setvars.sh

   上面
   也
   会
   更改
   python
   环境
   为
   工具链
   使用
   的
   那
   个
   并
   可能
   与
   Zephyr
   使用
   的
   冲突。

#. 设置
   :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
   为
   ``oneApi``。
