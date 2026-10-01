.. _kapa_ai:

Kapa.ai 文档助手
###############################

Zephyr 文档网站增加了一个由 Kapa.ai 驱动的 AI 助手。该助手基于 Zephyr 自身的文档、源代码和
GitHub 活动进行训练（参见下文`数据来源`_），可以用自然语言回答自由形式的问题，
并引用其构建每个答案所使用的文档页面和资源。

同一知识库还通过 `Model Context Protocol <https://modelcontextprotocol.io/>`_（MCP）服务器
对外提供，使外部 AI 助手和 IDE 可以直接查询 Zephyr 知识（参见`使用 MCP 服务器`_）。

.. note::

   答案是 AI 生成的，可能包含不准确之处。请始终对照官方文档验证重要信息，
   并将助手视为起点而非权威来源。

使用聊天机器人
*****************

聊天机器人在文档的每个页面都可以使用：

* 点击页面底部显示的聊天机器人按钮，或
* 按 :kbd:`Ctrl+K`（macOS 上为 :kbd:`Cmd+K`）从任意位置打开它。

助手会在侧边栏中打开，你可以用日常语言提问，例如*"如何在设备树（devicetree）中配置一个 UART 设备？"*
或*"工作队列（workqueue）和线程（thread）有什么区别？"*。答案中会包含指向相关文档页面、
GitHub 议题（issue）或源文件的链接，方便你进一步深入了解。

第一次使用助手时，会显示一个一次性同意界面，说明该功能如何工作以及会收集哪些数据。
参见下文`隐私`_部分。

.. tip::

   你不必用英语提问。助手会检测你使用的语言，并以相同语言回复，
   因此你可以用偏好的语言（英语、中文、西班牙语、日语、法语、德语以及许多其他语言）与它交互。

AI 驱动搜索
*****************

除了聊天机器人，Kapa.ai 还可以驱动文档搜索框：

#. 点击搜索框旁边的齿轮（:guilabel:`Search settings`）图标。
#. 从菜单中选择 :guilabel:`Kapa AI search`。
#. 输入查询并按 :kbd:`Enter`。

此时不再使用内置的关键字搜索，你的查询将由 AI 助手回答。你的选择会被记住，
因此后续搜索会一直使用你选择的引擎，直到你手动改回去。

使用 MCP 服务器
*********************

Kapa.ai 还将 Zephyr 知识库作为 :abbr:`MCP (Model Context Protocol)` 服务器对外提供。
MCP 是一个开放标准，让 AI 助手和具备 AI 能力的 IDE 能够连接外部工具和知识源。
将 Zephyr MCP 服务器添加到你的助手中，就能让它代表你查询最新的 Zephyr 文档、源代码和 GitHub 活动。

该服务器在以下端点可用，使用可流式（streamable）HTTP 传输：

.. code-block:: none

   https://zephyrproject.mcp.kapa.ai

具体的配置步骤取决于你使用的 MCP 客户端。大多数客户端读取带有 ``mcpServers`` 节的
JSON 配置文件，类似于以下示例：

.. code-block:: json

   {
     "mcpServers": {
       "zephyr-docs": {
         "url": "https://zephyrproject.mcp.kapa.ai"
       }
     }
   }

有些客户端则期望服务器通过本地 stdio 桥（如 `mcp-remote <https://www.npmjs.com/package/mcp-remote>`_）启动：

.. code-block:: json

   {
     "mcpServers": {
       "zephyr-docs": {
         "command": "npx", "args": ["-y", "mcp-remote", "https://zephyrproject.mcp.kapa.ai"]
       }
     }
   }

请查阅你所使用的具体 MCP 客户端（AI 编码助手、IDE 扩展等）的文档，
了解其配置的精确位置和语法。

.. tip::

   将 MCP 服务器连接到 AI 编码助手后，它就能回答 Zephyr 相关问题，
   并基于项目实际的文档和源代码给出代码建议，而不是仅仅依赖其训练数据。

数据来源
************

Kapa.ai 的答案完全基于以下 Zephyr 项目来源构建，这些来源按所示频率同步：

.. list-table::
   :header-rows: 1
   :widths: 25 50 25

   * - 来源
     - 详情
     - 刷新频率
   * - 源代码
     - ``zephyrproject-rtos/zephyr`` 仓库（不含 ``boards/`` 和 ``doc/`` 文件夹）；
       C、Markdown、Python 和文本文件
     - 每小时
   * - API 参考
     - https://docs.zephyrproject.org/latest/doxygen/html/index.html
     - 每天
   * - 设备树绑定（bindings）
     - https://docs.zephyrproject.org/latest/build/dts/api/bindings.html
     - 每天
   * - 主文档
     - https://docs.zephyrproject.org/latest/（不含 API 参考和设备树绑定章节）
     - 每天
   * - 项目 wiki
     - https://github.com/zephyrproject-rtos/zephyr/wiki
     - 每天
   * - GitHub 议题
     - ``zephyrproject-rtos/zephyr`` 最近 6 个月的议题（issues）
     - 每 5 分钟
   * - GitHub 拉取请求
     - ``zephyrproject-rtos/zephyr`` 最近 6 个月的拉取请求（pull requests）
       （不含未合并即关闭的）
     - 每 10 分钟

如需获取权威且最新的配置，请参见 Zephyr 项目基础设施 wiki 上的
`Kapa.ai 页面 <https://github.com/zephyrproject-rtos/infrastructure/wiki/Kapa.ai>`_。

隐私
*******

助手会利用你的问题，基于 Zephyr 文档、源代码以及 GitHub 议题和拉取请求来提供答案。
问题和交互可能被匿名收集并分析，以识别需要澄清的领域，从而帮助改进文档。
不会收集任何个人身份信息。
