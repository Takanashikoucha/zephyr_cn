.. _twister_bsim_harness:

Bsim
####

``bsim`` 测试框架（harness）扩展了 :ref:`脚本测试框架 <twister_script_harness>` 以支持
BabbleSim 测试。
在构建阶段，它将最终可执行文件（``zephyr.exe``）从构建目录复制到 BabbleSim 的 ``bin`` 目录
（``${BSIM_OUT_PATH}/bin``）。在运行阶段，它执行 ``tests_scripts`` 中列出的测试脚本。

默认情况下，可执行文件名为（将点号和斜杠替换为下划线）：
``bs_<platform_name>_<test_path>_<test_scenario_name>``。
此名称可通过 ``harness_config`` 部分中的 ``bsim_exe_name`` 选项覆盖。

扩展 :ref:`脚本测试框架 <twister_script_harness>` 的额外 ``bsim`` 测试框架键：

bsim_exe_name: <string>
    如果提供，复制到 BabbleSim 的 bin 目录时的可执行文件名将为
    ``bs_<platform_name>_<bsim_exe_name>``，而非基于测试路径和场景名称的默认值。

多镜像 BabbleSim 测试的示例配置，其中广播端（advertiser）仅构建，
扫描端（scanner）通过 :ref:`required_applications <required_applications>` 引用它：

.. code-block:: yaml

    common:
      platform_allow:
        - nrf52_bsim/native
      harness: bsim
    tests:
      bluetooth.host.adv.extended.advertiser:
        build_only: true
        harness_config:
          bsim_exe_name: tests_bsim_bluetooth_host_adv_extended_prj_advertiser_conf
        extra_args:
          CONF_FILE=prj_advertiser.conf
      bluetooth.host.adv.extended.scanner:
        harness_config:
          bsim_exe_name: tests_bsim_bluetooth_host_adv_extended_prj_scanner_conf
          tests_scripts:
            - tests_scripts/run_adv_extended.sh
        extra_args:
          CONF_FILE=prj_scanner.conf
        required_applications:
          - application: bluetooth.host.adv.extended.advertiser
