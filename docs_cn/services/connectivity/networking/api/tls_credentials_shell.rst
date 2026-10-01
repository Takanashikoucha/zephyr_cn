.. _tls_credentials_shell:

TLS Credentials Shell
#####################

TLS Credentials shell 为管理已安装的 TLS credentials 提供 command-line interface。

Commands
********

.. _tls_credentials_shell_buf_cred:

Buffer Credential (``buf``)
===========================

增量 buffer data 到 credential buffer 中（使其可用 :ref:`tls_credentials_shell_add_cred` command 添加。

替代方案：

   - 清除 credential buffer。

   - 直接将 credential 加载到 credential buffer（以 ``Ctrl + c`` 结束。

Usage
-----

要将 ``<DATA>`` 追加到 credential buffer（用：

.. code-block:: shell

   cred buf <DATA>

根据需要多次使用以将完整 credential 加载到 credential buffer（然后用 :ref:`tls_credentials_shell_add_cred` command 存储。

要将 ``<DATA>`` 直接加载到 credential buffer（用：

.. code-block:: shell

   cred buf load
   <DATA>
   Ctrl + c

要清除 credential buffer（用：

.. code-block:: shell

   cred buf clear

Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<DATA>``", "要追加到 credential buffer 的 text data。可为 text（或 base64-encoded binary。细节参见 :ref:`tls_credentials_shell_add_cred` 和 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_add_cred:

Add Credential (``add``)
=========================

向 TLS Credential store 添加 TLS credential。

Credential contents 可随 ``cred add`` 调用内联提供（否则从 credential buffer 获取。

Usage
-----

要用 credential buffer 中的数据添加 TLS credential（用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT>

要用同一 command 提供的数据添加 TLS credential（用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT> <DATA>


Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "新 credential 使用的 sectag。可为任何 non-negative integer。"
   "``<TYPE>``", "要添加的 credential type。有效值参见 :ref:`tls_credentials_shell_cred_types`。"
   "``<BACKEND>``", "Reserved。须始终为 ``DEFAULT``（case-insensitive）。"
   "``<FORMAT>``", "指定提供的 credential 的 storage format。有效值参见 :ref:`tls_credentials_shell_data_formats`。"
   "``<DATA>``", "若提供（此 argument 用作 credential data（而非 credential buffer 中的任何 data。可为 text（或 base64-encoded binary。"

.. _tls_credentials_shell_del_cred:

Delete Credential (``del``)
===========================

从 credential store 删除指定 credential。

Usage
-----

要删除匹配指定 sectag 和 credential type 的 credential（若存在）（用：

.. code-block:: shell

   cred del <SECTAG> <TYPE>

Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "要删除的 credential 的 sectag。可为任何 non-negative integer。"
   "``<TYPE>``", "要删除的 credential type。有效值参见 :ref:`tls_credentials_shell_cred_types`。"

.. _tls_credentials_shell_get_cred:

Get Credential Contents (``get``)
=================================

获取并打印指定 credential 的内容。

Usage
-----

要获取并打印匹配指定 sectag 和 credential type 的 credential（若存在）（用：

.. code-block:: shell

   cred get <SECTAG> <TYPE> <FORMAT>

Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "要获取的 credential 的 sectag。可为任何 non-negative integer。"
   "``<TYPE>``", "要获取的 credential type。有效值参见 :ref:`tls_credentials_shell_cred_types`。"
   "``<FORMAT>``", "指定提供的 credential 的 retrieval format。有效值参见 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_list_cred:

List Credentials (``list``)
===========================

列出 credential store 中的 TLS credentials。

Usage
-----

要列出所有可用 credentials（用：

.. code-block:: shell

   cred list

要列出所有带指定 sectag 的 credentials（用：

.. code-block:: shell

   cred list <SECTAG>

要列出所有带指定 credential type 的 credentials（用：

.. code-block:: shell

   cred list any <TYPE>

要列出所有带指定 credential type 和 sectag 的 credentials（用：

.. code-block:: shell

   cred list <SECTAG> <TYPE>


Arguments
---------

.. csv-table::
   :header: "Argument", "Description"
   :widths: 15 85

   "``<SECTAG>``", "Optional。若提供（仅列出带此 sectag 的 credentials。传 ``any`` 或省略以允许任何 sectag。否则（可为任何 non-negative integer。"
   "``<TYPE>``", "Optional。若提供（仅列出带此 credential type 的 credentials。传 ``any`` 或省略以允许任何 credential type。否则（有效值参见 :ref:`tls_credentials_shell_cred_types`。"


Output
------

Command 以以下（CSV-compliant）格式输出所有匹配的 credentials：

.. code-block:: shell

   <SECTAG>,<TYPE>,<DIGEST>,<STATUS>

其中：

.. csv-table::
   :header: "Symbol", "Value"
   :widths: 15 85

   "``<SECTAG>``", "列出的 credential 的 sectag。Non-negative integer。"
   "``<TYPE>``", "列出的 credential 的 credential type short-code（细节参见 :ref:`tls_credentials_shell_cred_types`）。"
   "``<DIGEST>``", "表示 credential contents 的 string digest。此 digest 的确切性质可能因 credentials storage backend 而异（但当前对所有 backends 均为 raw credential contents 的 base64 encoded SHA256 hash（故本质上相同 credentials 的不同 storage formats 将有不同 digests）。"
   "``<STATUS>``", "指示生成列出的 credential digest 成功或失败的 status code。成功为 0（否则为特定于 storage backend 的负 error code。Status 非零的行将以 error 格式打印。"

列表打印后（将打印找到的 credentials 的最终 summary（形式为：

.. code-block:: shell

   <N> credentials found.

其中 ``<N>`` 为找到的 credentials 数量（若未找到则为 zero。

.. _tls_credentials_shell_cred_types:

Credential Types
****************

以下 keywords（case-insensitive）可用于指定 credential type：

.. csv-table::
   :header: "Keyword(s)", "Meaning"
   :widths: 15 85

   "``CA_CERT``, ``CA``", "受信任的 CA certificate。"
   "``SERVER_CERT``, ``SELF_CERT``, ``CLIENT_CERT``, ``CLIENT``, ``SELF``, ``SERV``", "Self 或 server certificate。"
   "``PRIVATE_KEY``, ``PK``", "Private key。"
   "``PRE_SHARED_KEY``, ``PSK``", "Pre-shared key。"
   "``PRE_SHARED_KEY_ID``, ``PSK_ID``", "Pre-shared key 的 ID。"

.. _tls_credentials_shell_data_formats:

Storage/Retrieval Formats
*************************

:ref:`tls_credentials <sockets_tls_credentials_subsys>` module 将存储的 credentials 视为任意 binary buffers。

为便利（TLS credentials shell 提供四种格式以通过 shell 提供并随后检索这些 buffers。

这些格式及其（case-insensitive）keywords 如下：

.. csv-table::
   :header: "Keyword", "Meaning", "Behavior during storage (``cred add``)", "Behavior during retrieval (``cred get``)"
   :widths: 3, 32, 34, 34

   "``BIN``", "Credential 由 shell 作为 base64 处理（存储时无 NULL termination。", "输入 shell 的 data 将在存储前从 base64 解码为 raw binary。不追加 terminator。", "存储的 data 将在打印前编码为 base64。"
   "``BINT``", "Credential 由 shell 作为 base64 处理（存储时带 NULL termination。", "输入 shell 的 data 将在存储前从 base64 解码为 raw binary（并追加 NULL terminator。", "NULL terminator 将从存储的 data 截断（然后该 data 编码为 base64 并打印。"
   "``STR``", "Credential 由 shell 作为 literal string 处理（存储时无 NULL termination。", "输入 shell 的 text data 将按原样传入存储（无 NULL terminator。", "存储的 data 作为 text 打印。Non-printable characters 打印为 ``?``"
   "``STRT``", "Credential 由 shell 作为 literal string 处理（存储时带 NULL-termination。", "输入 shell 的 text data 将按原样传入存储（带 NULL terminator。", "NULL terminator 将在作为 text 打印前从存储的 data 截断。Non-printable characters 打印为 ``?``"

``BIN`` format 可用于安装任何类型的 credentials（因为 base64 可用于编码任何可想象的 binary buffer。
其余三种格式为特殊 use-cases 的便利提供。

例如：

- 要安装 printable pre-shared-keys（用 ``STR`` 输入 PSK（无需先编码。确保其存储时无 NULL terminator。
- 要安装 DER 格式的 X.509 certificates（或其他 raw-binary credentials（如 non-printable PSKs）（base64-encode 该 binary（并用 ``BIN`` format。
- 要安装 PEM 格式的 X.509 certificates 或 certificate chains（base64 encode 完整 PEM string（含 new-lines 和 ``----BEGIN X ----`` / ``----END X----`` markers）（然后用 ``BINT`` format 确保存储的 string 为 NULL-terminated。这是必需的（因为 Zephyr 不支持 shell 中的 multi-line strings。否则（可用 ``STRT`` format 实现此目的而无需 base64 编码。若手动将 NULL terminator 编码到 base64 中（也可用 ``BIN`` 替代。
