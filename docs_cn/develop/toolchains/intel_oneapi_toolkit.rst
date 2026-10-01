.. _toolchain_intel_oneapi_toolkit:

Intel oneAPI 工具包
####################

#. 下载 `Intel oneAPI Base Toolkit
   <https://software.intel.com/content/www/us/en/develop/tools/oneapi/all-toolkits.html>`_

#. 假设工具包安装在 ``/opt/intel/oneApi``，使用以下命令设置环境::

        # Linux, macOS:
        export ONEAPI_TOOLCHAIN_PATH=/opt/intel/oneapi
        source $ONEAPI_TOOLCHAIN_PATH/compiler/latest/env/vars.sh

        # Windows:
        > set ONEAPI_TOOLCHAIN_PATH=C:\Users\Intel\oneapi

   要设置完整的 oneApi 环境，请使用::

        source  /opt/intel/oneapi/setvars.sh

   上述命令还会将 Python 环境更改为工具链所使用的那个，
   可能会与 Zephyr 所使用的环境产生冲突。

#. 将 :envvar:`ZEPHYR_TOOLCHAIN_VARIANT` 设置为 ``oneApi``。
