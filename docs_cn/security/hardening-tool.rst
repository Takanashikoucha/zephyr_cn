.. _hardening:

加固工具
##############

在发布产品之前，确保软件尽可能安全至关重要。
这一过程称为"加固"，涉及增强系统安全以保护其免受潜在威胁和漏洞的影响。

从高层来看，加固 Zephyr 应用可视为一个双重过程：

#. 禁用可能导致安全漏洞的功能和编译标志（例如，确保不使用任何"实验性"功能，
   禁用通常用于调试目的的功能，如断言、shell 等）。
#. 启用可提升安全的可选功能（例如，栈哨兵、硬件栈保护等）。
   其中一些功能可能依赖硬件。

为简化此过程，Zephyr 提供了一款**加固工具**，用于根据**加固数据库**分析应用配置。
加固数据库是由 Zephyr **安全工作组**整理的一组建议。
该工具查看构建目标中的 Kconfig 选项，并提供量身定制的建议和推荐，
用于调整安全相关选项，并附上每条建议背后的理由。

使用
*****

.. zephyr-app-commands::
    :tool: all
    :zephyr-app: samples/hello_world
    :board: reel_board
    :goals: hardenconfig

输出应与下表类似。对于每个设置为可能导致安全漏洞值的配置选项，
表格将提出一个应替代使用的推荐值，连同该选项重要性的原因。

.. code-block:: console

   Hardening report for profile: strict
   +------------------------------+-----------+---------------+----------------+--------------------------------------------------+
   | Name                         | Current   | Recommended   | Check result   | Rationale                                        |
   +==============================+===========+===============+================+==================================================+
   | CONFIG_BUILD_OUTPUT_STRIPPED | n         | y             | FAIL           | Produces a stripped copy of the ELF next to the  |
   |                              |           |               |                | unstripped one, so a product that distributes or |
   |                              |           |               |                | flashes the ELF itself ships no symbol names or  |
   |                              |           |               |                | debug information for an attacker to work from.  |
   |                              |           |               |                | Both files are built; deploying the stripped one |
   |                              |           |               |                | remains the user's responsibility.               |
   +------------------------------+-----------+---------------+----------------+--------------------------------------------------+
   | CONFIG_STACK_SENTINEL        | n         | y             | FAIL           | Places a software sentinel value at the end of   |
   |                              |           |               |                | each thread stack and checks it at context       |
   |                              |           |               |                | switches, catching overflows on hardware without |
   |                              |           |               |                | MPU/MMU stack protection.                        |
   +------------------------------+-----------+---------------+----------------+--------------------------------------------------+

不适用于当前目标的选项（例如，无 MPU 硬件上的基于 MPU 的保护，
或当前配置中无可见提示的选项）不会被报告。

除数据库驱动的检查外，该工具还会标记任何在 Kconfig 本身中被标记为
实验性、已弃用或不安全的已启用选项（即选择
:kconfig:option:`CONFIG_EXPERIMENTAL`、:kconfig:option:`CONFIG_DEPRECATED` 或
:kconfig:option:`CONFIG_NOT_SECURE` 的选项）。

配置档
********

建议被分组为**配置档**。树内提供两个配置档：

``base``
   每个生产构建都应满足的基线加固：启用可用的内存保护和漏洞缓解功能，
   并禁用本质上不安全的选项。

``strict``（默认）
   包含 ``base`` 的全部内容，外加移除调试、跟踪和可观测性功能（日志、
   shell、断言等）——这些功能会扩大攻击面或泄露内部状态。
   某些产品合理地保留其中一部分启用——如果你的情况如此，
   请改为对照 ``base`` 配置档检查：

.. code-block:: shell

   west build -t hardenconfig -- -DHARDENCONFIG_PROFILE=base

配置选项
*********************

该工具通过 CMake 缓存变量（在 ``west build`` 命令行上 ``--`` 之后传递，如上所示）
或同名环境变量控制：

.. list-table::
   :header-rows: 1

   * - 选项
     - 效果
   * - ``HARDENCONFIG_PROFILE``
     - 用于对照检查的加固配置档。默认：``strict``。
   * - ``HARDENCONFIG_SHOW_ALL``
     - 设置时，除失败项外还列出通过和不适用的选项。
   * - ``HARDENCONFIG_STRICT``
     - 设置时，若任何检查失败则以非零代码退出。
       适用于以干净的加固报告门控 CI 流水线或发布流程。
   * - ``HARDENCONFIG_JSON``
     - 结果额外以 JSON 写入的文件路径，供脚本和仪表盘消费。
   * - ``HARDENCONFIG_EXTRA_SOURCES``
     - 额外加固数据库文件（见下文）的分号分隔列表。

加固数据库
**********************

数据库被分发，使得每条规则与其所加固的代码放在一起，
并由该代码的维护者审查：

* :zephyr_file:`scripts/kconfig/hardening.yaml` — 中心文件，
  由安全工作组所有。它定义加固**配置档**，
  以及针对顶层 Kconfig 文件中定义符号的规则。
* 与其相关 Kconfig 文件相邻的 ``hardening.yaml`` **片段**（例如
  :zephyr_file:`subsys/bluetooth/hardening.yaml` 或
  :zephyr_file:`arch/x86/hardening.yaml`），仅包含规则。
  片段在 ``arch/``、``boards/``、``drivers/``、``kernel/``、``lib/``、
  ``modules/``、``share/``、``soc/`` 和 ``subsys/`` 下自动发现。
  在两个文件中定义同一符号是错误，在片段中定义配置档也是错误。

所有文件使用相同的 JSON schema，:zephyr_file:`scripts/schemas/hardening-schema.yaml`。
每条规则以其适用的 Kconfig 符号为键，推荐一个精确值或整数约束：

.. code-block:: yaml

   rules:
     BOOT_BANNER:
       value: n
       rationale: |
         The boot banner prints the exact Zephyr version to the console,
         letting anyone with console access fingerprint the firmware and
         match it against known vulnerabilities for that release.
       references: [CWE-200]

     STACK_POINTER_RANDOM:
       min: 100
       rationale: |
         Randomizing each thread's initial stack pointer makes stack
         addresses unpredictable. The offset is taken out of the thread's
         own stack, which keeps the recommended value small.
       references: [CWE-121]

贡献新规则意味着将其添加到相关 Kconfig 文件旁的 ``hardening.yaml`` 片段
（如果子系统尚没有片段则创建片段），并需要一个 ``rationale``——
该要求由 schema 强制执行。持续集成额外验证每个文件都能解析并匹配 schema、
每条规则都引用一个与符号类型值相一致的现有 Kconfig 符号、
没有规则被定义两次，且没有文件看起来像命名错误的片段——
因此条目不会悄悄过期或悄悄加载失败。

``rationale`` 是报告向读者展示的内容，包裹在窄列中，
通常也是读者仅有的依据。用一两句现在时态、以功能为主语的话
说明该选项的安全后果：

``value: n``
   启用它所造成的暴露，以及在重要时谁能触达它："冗长的调制解调器日志
   转储与调制解调器交换的所有数据，可能包括 APN 设置、PIN 和服务器地址
   等凭据。"

``value: y``
   它阻止的攻击，或关闭它允许的行为，以更易读者为准。

``value: 0``、``min`` 和 ``max``
   其他值输出什么或未能阻止什么，以及边界值本身的作用。

不要：

* 说明选项属于哪里。配置档决定产品是否应接受该后果；
  写"……泄露内部传输状态和地址"，而非"……且仅属于开发构建"。
* 声称一个不进一步行动就不完整的效果。例如，某选项可能启用
   剥离二进制的生成，但确保部署的是该二进制是用户的责任。
* 复述报告已展示的列。在"0 完全禁用随机化；建议至少 100 字节的随机偏移"中，
   后半部分是"推荐"列。
* 重复另一规则的措辞。可能在同一报告中失败的两条规则
   应读起来足够不同，以便读者区分。

不要为某个选项添加 ``n`` 规则，如果该选项只能在另一个覆盖
至少相同配置档的 ``n`` 规则已被违反时才能启用；
例如，一旦 :kconfig:option:`CONFIG_SHELL` 本身被标记，
shell 命令模块的规则就是冗余的，CI 会拒绝它。
仅 ``select``\ 一个被标记选项的规则不冗余：
它指明了用户实际必须更改的内容。

规则不携带适用条件：某推荐是否适用于给定目标
已编码在 Kconfig 本身中（依赖、硬件支持），
该工具将不适用于当前目标的选项报告为不适用而非失败。

在树外扩展数据库
**********************************

产品团队可用 ``HARDENCONFIG_EXTRA_SOURCES`` 在树内数据库之上
叠加自己的推荐。每个额外文件使用相同 schema，
可定义新配置档（可选地扩展树内配置档）和新规则，
以及覆盖树内规则。重新定义现有配置档会被拒绝，
因此无论产品在其上叠加什么，树内配置档都保留此处文档化的含义：

.. code-block:: yaml

   profiles:
     acme-production:
       extends: strict
       description: ACME product security policy.

   rules:
     MY_VENDOR_DEBUG_INTERFACE:
       value: n
       profiles: [acme-production]
       rationale: |
         The vendor debug interface bypasses the product's authentication.

.. code-block:: shell

   west build -t hardenconfig -- \
     -DHARDENCONFIG_EXTRA_SOURCES=/path/to/acme-hardening.yaml \
     -DHARDENCONFIG_PROFILE=acme-production
