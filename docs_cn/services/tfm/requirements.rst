TF-M Requirements
#################

以下是可用于 TF-M 的部分板级：

.. list-table::
   :header-rows: 1

   * - Board
     - NSPE board name
   * - :ref:`mps2_an521_board`
     - ``mps2/an521/cpu0/ns`` (qemu supported)
   * - :zephyr:board:`mps3`
     -
       - ``mps3/corstone300/fvp/ns`` (armfvp supported)
       - ``mps3/corstone310/fvp/ns`` (armfvp supported)
   * - :zephyr:board:`mps4`
     -
       - ``mps4/corstone315/fvp/ns`` (armfvp supported)
       - ``mps4/corstone320/fvp/ns`` (armfvp supported)
   * - :zephyr:board:`bl5340_dvk`
     - ``bl5340_dvk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`lpcxpresso55s69`
     - ``lpcxpresso55s69_ns``
   * - :zephyr:board:`nrf9160dk_nrf9160 <nrf9160dk>`
     - ``nrf9160dk/nrf9160/ns``
   * - :zephyr:board:`nrf5340dk`
     - ``nrf5340dk/nrf5340/cpuapp/ns``
   * - :zephyr:board:`b_u585i_iot02a`
     - ``b_u585i_iot02a/stm32u585xx/ns``
   * - :zephyr:board:`nucleo_l552ze_q`
     - ``nucleo_l552ze_q/stm32l552xx/ns``
   * - :zephyr:board:`stm32l562e_dk`
     - ``stm32l562e_dk/stm32l562xx/ns``
   * - :zephyr:board:`v2m_musca_b1`
     - ``v2m_musca_b1/musca_b1/ns``

要确认某板级支持 TF-M，请检查该板级默认配置中 :kconfig:option:`CONFIG_TRUSTED_EXECUTION_NONSECURE` 是否设置为 ``y``。

Software Requirements
*********************

构建 TF-M 二进制文件所需的 Python 模块列在 TF-M 仓库的 ``tools/requirements.txt`` 中。

可以通过以下方式安装它们：

   .. code-block:: bash

      $ pip3 install -r "$(west list trusted-firmware-m -f '{abspath}')/tools/requirements.txt"

TF-M 的签名工具会使用这些模块，为固件镜像做好准备，以便引导加载器进行验证。

为 QEMU 生成二进制文件以及在某些平台上合并签名后的安全与非安全二进制文件的过程，还需要使用 ``srec_cat`` 工具。

在 Linux 上可以通过以下方式安装：

   .. code-block:: bash

      $ sudo apt-get install srecord

在 OS X 上：

   .. code-block:: bash

      $ brew install srecord

对于 Windows 系统，请确保系统路径上有一份该工具可用。例如参见：
`SRecord for Windows <https://sourceforge.net/projects/srecord/files/srecord-win32>`_
