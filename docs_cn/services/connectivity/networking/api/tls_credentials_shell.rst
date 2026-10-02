.. _tls_credentials_shell:

TLS 凭据 Shell
#####################

TLS 凭据 Shell 提供了一个命令行界面，用于管理已安装的 TLS 凭据。

命令
********

.. _tls_credentials_shell_buf_cred:

缓冲凭据（``buf``）
===========================

将数据增量地写入凭据缓冲区，以便之后使用 :ref:`tls_credentials_shell_add_cred` 命令添加。

或者：

   - 清空凭据缓冲区。

   - 将凭据直接加载到凭据缓冲区，以 ``Ctrl + c`` 结束。

用法
-----

要将 ``<DATA>`` 追加到凭据缓冲区，使用：

.. code-block:: shell

   cred buf <DATA>

按需多次使用此命令，将完整凭据加载到凭据缓冲区，然后使用 :ref:`tls_credentials_shell_add_cred` 命令将其存储。

要将 ``<DATA>`` 直接加载到凭据缓冲区，使用：

.. code-block:: shell

   cred buf load
   <DATA>
   Ctrl + c

要清空凭据缓冲区，使用：

.. code-block:: shell

   cred buf clear

参数
---------

.. csv-table::
   :header: "参数", "说明"
   :widths: 15 85

   "``<DATA>``", "要追加到凭据缓冲区的文本数据。可以是文本，也可以是 base64 编码的二进制。详细信息参见 :ref:`tls_credentials_shell_add_cred` 和 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_add_cred:

添加凭据（``add``）
=========================

向 TLS 凭据存储（TLS Credential store）添加一个 TLS 凭据。

凭据内容可以随 ``cred add`` 调用以内联方式提供，否则将从凭据缓冲区获取。

用法
-----

要使用凭据缓冲区中的数据添加一个 TLS 凭据，使用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT>

要使用同一命令中提供的数据添加一个 TLS 凭据，使用：

.. code-block:: shell

   cred add <SECTAG> <TYPE> <BACKEND> <FORMAT> <DATA>


参数
---------

.. csv-table::
   :header: "参数", "说明"
   :widths: 15 85

   "``<SECTAG>``", "新凭据使用的 sectag。可以是任意非负整数。"
   "``<TYPE>``", "要添加的凭据类型。有效值参见 :ref:`tls_credentials_shell_cred_types`。"
   "``<BACKEND>``", "保留。必须始终为 ``DEFAULT``（不区分大小写）。"
   "``<FORMAT>``", "指定所提供凭据的存储格式。有效值参见 :ref:`tls_credentials_shell_data_formats`。"
   "``<DATA>``", "如果提供，此参数将作为凭据数据使用，而不是凭据缓冲区中的任何数据。可以是文本，也可以是 base64 编码的二进制。"

.. _tls_credentials_shell_del_cred:

删除凭据（``del``）
===========================

从凭据存储中删除指定的凭据。

用法
-----

要删除与指定 sectag 和凭据类型匹配的凭据（如果存在），使用：

.. code-block:: shell

   cred del <SECTAG> <TYPE>

参数
---------

.. csv-table::
   :header: "参数", "说明"
   :widths: 15 85

   "``<SECTAG>``", "要删除的凭据的 sectag。可以是任意非负整数。"
   "``<TYPE>``", "要删除的凭据类型。有效值参见 :ref:`tls_credentials_shell_cred_types`。"

.. _tls_credentials_shell_get_cred:

获取凭据内容（``get``）
=================================

检索并打印指定凭据的内容。

用法
-----

要检索并打印与指定 sectag 和凭据类型匹配的凭据（如果存在），使用：

.. code-block:: shell

   cred get <SECTAG> <TYPE> <FORMAT>

参数
---------

.. csv-table::
   :header: "参数", "说明"
   :widths: 15 85

   "``<SECTAG>``", "要获取的凭据的 sectag。可以是任意非负整数。"
   "``<TYPE>``", "要获取的凭据类型。有效值参见 :ref:`tls_credentials_shell_cred_types`。"
   "``<FORMAT>``", "指定所提供凭据的检索格式。有效值参见 :ref:`tls_credentials_shell_data_formats`。"

.. _tls_credentials_shell_list_cred:

列出凭据（``list``）
===========================

列出凭据存储中的 TLS 凭据。

用法
-----

要列出所有可用凭据，使用：

.. code-block:: shell

   cred list

要列出具有指定 sectag 的所有凭据，使用：

.. code-block:: shell

   cred list <SECTAG>

要列出具有指定凭据类型的所有凭据，使用：

.. code-block:: shell

   cred list any <TYPE>

要列出具有指定凭据类型和 sectag 的所有凭据，使用：

.. code-block:: shell

   cred list <SECTAG> <TYPE>


参数
---------

.. csv-table::
   :header: "参数", "说明"
   :widths: 15 85

   "``<SECTAG>``", "可选。如果提供，则仅列出具有此 sectag 的凭据。传入 ``any`` 或省略以允许任意 sectag。否则可以是任意非负整数。"
   "``<TYPE>``", "可选。如果提供，则仅列出具有此凭据类型的凭据。传入 ``any`` 或省略以允许任意凭据类型。否则有效值参见 :ref:`tls_credentials_shell_cred_types`。"


输出
------

该命令以如下（符合 CSV 规范的）格式输出所有匹配的凭据：

.. code-block:: shell

   <SECTAG>,<TYPE>,<DIGEST>,<STATUS>

其中：

.. csv-table::
   :header: "符号", "值"
   :widths: 15 85

   "``<SECTAG>``", "所列凭据的 sectag。一个非负整数。"
   "``<TYPE>``", "所列凭据的凭据类型简码（详细信息参见 :ref:`tls_credentials_shell_cred_types`）。"
   "``<DIGEST>``", "表示凭据内容的字符串摘要。该摘要的具体形式可能因凭据存储后端而异，但目前对于所有后端，它都是原始凭据内容的 base64 编码 SHA256 哈希值（因此对于本质上相同的凭据，不同的存储格式将具有不同的摘要）。"
   "``<STATUS>``", "表示生成所列凭据摘要成功或失败的狀態代码。成功时为 0，否则为存储后端特有的负错误码。状态不为零的行将以错误格式打印。"

打印列表后，将按以下形式打印所找到凭据的最终汇总：

.. code-block:: shell

   <N> credentials found.

其中 ``<N>`` 是找到的凭据数量，未找到时为零。

.. _tls_credentials_shell_cred_types:

凭据类型
****************

可以使用以下关键字（不区分大小写）指定凭据类型：

.. csv-table::
   :header: "关键字", "含义"
   :widths: 15 85

   "``CA_CERT``, ``CA``", "受信任的 CA 证书。"
   "``SERVER_CERT``, ``SELF_CERT``, ``CLIENT_CERT``, ``CLIENT``, ``SELF``, ``SERV``", "自签名或服务器证书。"
   "``PRIVATE_KEY``, ``PK``", "私钥。"
   "``PRE_SHARED_KEY``, ``PSK``", "预共享密钥。"
   "``PRE_SHARED_KEY_ID``, ``PSK_ID``", "预共享密钥的 ID。"

.. _tls_credentials_shell_data_formats:

存储/检索格式
*************************

:ref:`tls_credentials <sockets_tls_credentials_subsys>` 模块将存储的凭据视为任意二进制缓冲区。

为方便起见，TLS 凭据 Shell 提供了四种格式，用于通过 Shell 提供这些缓冲区并稍后检索它们。

这些格式及其（不区分大小写的）关键字如下：

.. csv-table::
   :header: "关键字", "含义", "存储时（``cred add``）的行为", "检索时（``cred get``）的行为"
   :widths: 3, 32, 34, 34

   "``BIN``", "凭据由 Shell 作为 base64 处理，存储时不带 NULL 终止符。", "在存储之前，在 Shell 中输入的数据将从 base64 解码为原始二进制。不会追加终止符。", "存储的数据在打印之前将编码为 base64。"
   "``BINT``", "凭据由 Shell 作为 base64 处理，存储时带 NULL 终止符。", "在存储之前，在 Shell 中输入的数据将从 base64 解码为原始二进制，并追加一个 NULL 终止符。", "在打印之前，NULL 终止符将从存储数据中截断，然后该数据被编码为 base64 并打印。"
   "``STR``", "凭据由 Shell 作为字面字符串处理，存储时不带 NULL 终止符。", "在 Shell 中输入的文本数据将按原样传入存储，不带 NULL 终止符。", "存储的数据将以文本形式打印。不可打印字符将打印为 ``?``"
   "``STRT``", "凭据由 Shell 作为字面字符串处理，存储时带 NULL 终止符。", "在 Shell 中输入的文本数据将按原样传入存储，带 NULL 终止符。", "在打印之前，NULL 终止符将从存储数据中截断，然后该数据以文本形式打印。不可打印字符将打印为 ``?``"

``BIN`` 格式可用于安装任何类型的凭据，因为 base64 可用于编码任何可想象的二进制缓冲区。
其余三种格式为特殊用例提供的便利。

例如：

- 要安装可打印的预共享密钥，使用 ``STR`` 直接输入 PSK 而无需先进行编码。
  这确保它以不带 NULL 终止符的方式存储。
- 要安装 DER 格式的 X.509 证书（或其他原始二进制凭据，例如不可打印的 PSK），将二进制进行 base64 编码并使用 ``BIN`` 格式。
- 要安装 PEM 格式的 X.509 证书或证书链，将整个 PEM 字符串（包括换行符和 ``----BEGIN X ----`` / ``----END X----`` 标记）进行 base64 编码，然后使用 ``BINT`` 格式以确保存储的字符串以 NULL 结尾。
  这是必需的，因为 Zephyr 不支持 Shell 中的多行字符串。
  否则，可以使用 ``STRT`` 格式实现此目的而无需 base64 编码。
  如果你手动将 NULL 终止符编码进 base64 中，也可以使用 ``BIN`` 代替。
