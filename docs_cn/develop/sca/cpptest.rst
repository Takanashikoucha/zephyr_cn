.. _cpptest:

Parasoft C/C++test 支持
##########################

Parasoft `C/C++test <https://www.parasoft.com/products/parasoft-c-ctest/>`__ 是一个用于 C 和 C++ 的软件测试和静态分析工具。它是一个商业软件，你必须获取商业许可证才能使用它。

C/C++test 的文档可以在 https://docs.parasoft.com/ 找到。请参考文档了解如何使用它。

生成构建数据文件
***************************

要使用 C/C++test，``cpptestscan`` 必须在你的 :envvar:`PATH` 环境变量中找到。并且 :ref:`west build <west-building>` 应该用 ``-DZEPHYR_SCA_VARIANT=cpptest`` 参数调用，例如

.. code-block:: shell

    west build -b qemu_cortex_m3 zephyr/samples/hello_world -- -DZEPHYR_SCA_VARIANT=cpptest

一个 ``.bdf`` 文件将生成为 :file:`build/sca/cpptest/cpptestscan.bdf`（构建数据文件）。

生成报告文件
************************

请参考 Parasoft C/C++test 文档获取更多细节。

要导入并生成报告文件，类似以下内容应该可以工作。

.. code-block:: shell

    cpptestcli -data out -localsettings local.conf -bdf build/sca/cpptest/cpptestscan.bdf -config "builtin://Recommended Rules" -report out/report

你可能需要将 ``bdf.import.c.compiler.exec``、``bdf.import.cpp.compiler.exec`` 和 ``bdf.import.linker.exec`` 设置为 :ref:`west build <west-building>` 所使用的工具链。
