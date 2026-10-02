.. _flashing-soc-board-config:

烧录配置
######################

Zephyr 支持为烧录器（flash runner，从 :ref:`west flash<west-flashing>` 调用）
设置配置，允许自定义烧录开发板时命令的使用方式。此配置用于 :ref:`sysbuild` 项目，
允许为开发板目标组配置何时运行命令。例如：多核 SoC 可能希望只允许对所有核心
使用一次 ``--erase`` 参数，这会防止在单次 ``west flash`` 调用中运行多个擦除任务，
这可能错误地清除其他正在烧录的镜像使用的内存。

优先级
********

烧录配置是单一的，它只会从单个位置读取。此配置可以位于以下文件中，按最高优先级
开始：

 * ``soc.yml``（在 soc 文件夹中）
 * ``board.yml``（在 board 文件夹中）

配置
*************

配置通过在 yml 文件中使用带有单个 ``run_once`` 子项的 ``runners`` 映射来应用，
这然后包含一个命令映射，如提供给烧录器的那样，例如 ``--reset`` 后跟一个指定
每个这些命令设置的列表（这些按烧录器分组，并按限定符/开发板分组）。命令使用
``runners`` 列表值有关联的烧录器它们应用于，这可以包含 ``all`` 如果它应用于所有
烧录器，否则必须包含每个它应用于的烧录器使用烧录器特定名称。开发板目标组可以使用
``groups`` 键指定，它有一个开发板目标集合的列表。开发板目标是正则表达式匹配，对于
``soc.yml`` 文件每个开发板目标集合必须在 ``qualifiers`` 键中（只允许开发板限定符的
正则表达式匹配，开发板名称必须从这些条目中省略）。对于 ``board.yml`` 文件每个开发板
目标集合必须在 ``boards`` 键中，这些是包含形成单一组的匹配的列表。最后一个参数
``run`` 可以设置为 ``first``，意味着命令将在每个开发板目标集合的第一个镜像烧录过程中
运行一次，或设置为 ``last``，将在每个开发板目标集合的最终镜像烧录中运行一次。

``soc.yml`` 的示例烧录配置显示如下，其中 ``--recover`` 命令只会对使用 nRF5340 SoC
应用或网络 CPU 核心的任何开发板目标使用一次，并只会在所有相应核心的镜像烧录后重置
网络或应用核心。

.. code-block:: yaml

  runners:
    run_once:
      '--recover':
        - run: first
          runners:
            - nrfjprog
          groups:
            - qualifiers:
                - nrf5340/cpunet
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns
      '--reset':
        - run: last
          runners:
            - nrfjprog
            - jlink
          groups:
            - qualifiers:
                - nrf5340/cpunet
            - qualifiers:
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns
        # Made up non-real world example to show how to specify different options for different
        # flash runners
        - run: first
          runners:
            - some_other_runner
          groups:
            - qualifiers:
                - nrf5340/cpunet
            - qualifiers:
                - nrf5340/cpuapp
                - nrf5340/cpuapp/ns

使用
*****

烧录器支持的命令在烧录非 sysbuild 应用时可以正常使用，run once 配置不会被使用。
烧录带多个镜像的 sysbuild 项目时，将应用烧录器 run once 配置。

例如，为 nrf5340dk 构建 :zephyr:code-sample:`smp-svr` 示例将包含 MCUboot 作为
次要镜像：

.. code-block:: console

   cmake -GNinja -Sshare/sysbuild/ -Bbuild -DBOARD=nrf5340dk/nrf5340/cpuapp -DAPP_DIR=samples/subsys/mgmt/mcumgr/smp_svr
   cmake --build build

用 nrf5340dk 连接构建后，以下命令可以用于烧录开发板的两个应用，并只会在烧录
第一个镜像时执行单次设备恢复操作：

.. code-block:: console

   west flash --recover

如果上面在没有烧录配置的情况下运行，恢复过程将运行两次，设备将无法启动。
