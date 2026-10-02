.. _fota_http:

Firmware Over-the-Air over HTTP
###############################

概述
********

FOTA HTTP 库从 HTTP 服务器下载固件映像，
并将其直接写入当前未运行的 MCUboot 槽。
然后允许应用程序请求交换、确认新映像或
擦除该槽。与 :ref:`hawkBit 或 UpdateHub <ota>` 不同，没有设备
管理协议参与：任何能够分发文件的 web 服务器
都可以作为更新源，这使其非常适合简单的部署
和台架测试。

映像到达时通过 :ref:`flash_img_api` 流式写入 flash，
因此其大小不受 RAM 限制。槽在
写入期间被渐进擦除，且槽的 MCUboot trailer 在
第一个字节落地前被清除，因此前一个映像的
残留永远不会被误认为待处理的交换。

下载后，库从 flash 读回 MCUboot 头，
当数据不是映像时以 ``-ENOEXEC`` 失败。它不
验证签名：MCUboot 在映像启动前会做此事，
且该检查决定映像是否运行。可选的 SHA-256
与调用者提供的摘要比较可用
:kconfig:option:`CONFIG_FOTA_HTTP_SHA256_CHECK`，以在
重启前捕获损坏的
传输。被该比较拒绝的映像，或
被下面的降级检查拒绝的映像，会从槽中擦除。
部分失败的下载后，:c:func:`fota_http_apply` 拒绝该槽，直到另一
次写入它的下载成功，而部分数据留在原处用于
续传。

更新周期
************

典型序列为：

#. :c:func:`fota_http_download` 或 :c:func:`fota_http_download_async`
   将映像获取到次要槽。可选的
   :c:struct:`fota_http_download_params` 成员 ``sha256``、``resume``
   和 TLS 相关的仅在其 Kconfig 选项启用时存在。
#. :c:func:`fota_http_apply` 将映像标记为测试启动，或
   永久。
#. 设备重启，MCUboot 将映像交换进来。
#. 测试启动时，应用程序验证自身并调用
   :c:func:`fota_http_confirm`。没有该调用，下次重启会使
   MCUboot 回退到前一个映像。

回退步骤需要带回退支持的 MCUboot 模式，例如
swap-using-move 或 swap-using-offset。在 overwrite-only 模式中，
交换发生即前一个映像消失，且确认无效果，
因此检查板卡的 sysbuild 配置选择哪种模式。

测试映像运行期间，次要槽持有 MCUboot 将
回退到的映像，因此 :c:func:`fota_http_download` 以 ``-EPERM`` 拒绝，直到
调用了 :c:func:`fota_http_confirm`。

线程和栈
*****************

:c:func:`fota_http_download` 阻塞调用线程整个
传输期间，且需要足够的栈供 HTTP 客户端使用，https 时供
TLS 握手。使用 :kconfig:option:`CONFIG_FOTA_HTTP_ASYNC` 时，
:c:func:`fota_http_download_async` 在
库拥有的线程上运行相同的传输，其大小由
:kconfig:option:`CONFIG_FOTA_HTTP_THREAD_STACK_SIZE` 决定，并通过
完成回调报告
结果。shell 命令选择
异步变体，因此 shell 栈大小无关紧要。
仅调用 :c:func:`fota_http_download` 的应用程序保持其
禁用，且不付出线程栈的代价。

一次仅运行一个下载。:c:func:`fota_http_cancel` 在下一
片段到达或请求超时
时中止进行中的传输。

重定向和续传
********************

状态为 301、302、303、307 或 308 的响应会被跟随
最多 :kconfig:option:`CONFIG_FOTA_HTTP_MAX_REDIRECTS` 次。绝对
和仅路径的 ``Location`` 头均被接受。

使用 :kconfig:option:`CONFIG_FOTA_HTTP_RESUME` 时，传输运行期间和
失败时下载偏移存储在 settings 中。稍后
设置 ``resume`` 参数的下载从该偏移用 HTTP
``Range`` 请求继续。仅当 URL 和映像索引
与中断的下载匹配时重用该偏移，且当
服务器发送了 ``ETag`` 或
``Last-Modified`` 头时，请求会携带 ``If-Range``，因此
服务器上变更的文件会从头重新获取。忽略 ``Range`` 头并以完整文件应答的
服务器会从零重启传输，``416 Range Not Satisfiable`` 应答
同样如此——这是文件变得比存储
偏移短时服务器发送的。过长无法存储的验证器也会丢弃
存储的进度，因此
下次下载从头开始，而非对可能已变更的文件续传。
映像完成时清除偏移。

多个映像
***************

在多于一个可更新映像的布局中，``image_index``
参数选择下载去往哪个次要槽。
:c:func:`fota_http_apply` 和 :c:func:`fota_http_confirm` 均接受
相同的索引，因此携带第二台设备固件的布局
仅确认本设备验证的内容。当若干映像必须一起运行时，
重启前下载并应用所有映像：MCUboot 验证
整个集合并一次交换进来，且之后确认每个映像，因为
未确认的映像是单独回退的。
:c:func:`fota_http_confirm_pending` 仅报告映像 0，因此
更新多个映像的应用程序需自行跟踪其余映像。
使用 :kconfig:option:`CONFIG_FOTA_HTTP_REJECT_DOWNGRADE` 的降级检查仅覆盖映像 0。

使用 direct-XIP 引导加载程序时，映像运行的槽在
链接时固定，因此设备必须获取为空闲槽构建的映像变体。
:c:func:`fota_http_get_download_slot` 报告其为哪个槽。这仅
覆盖单映像布局：第一个映像之后的每个映像，库
总是上传到该对的奇数槽，这对
swap 和 overwrite 模式是正确的，但对 direct-XIP 不正确。

降级保护
********************

:kconfig:option:`CONFIG_FOTA_HTTP_REJECT_DOWNGRADE` 将
下载头中的版本与运行映像比较，
当版本较旧时使下载失败，并擦除被拒绝的映像以防误
应用。这是为应用程序提供的便利检查。强制
策略应属于引导加载程序，参见 MCUboot 的降级防止和
硬件回滚保护选项。

TLS
***

启用 :kconfig:option:`CONFIG_FOTA_HTTP_TLS` 时接受
``https`` URL。服务器的 CA 证书在
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_SEC_TAG` 下查找，或在
下载参数传入的标签下查找，且可用
:c:func:`fota_http_tls_add_ca` 或直接用
:c:func:`tls_credential_add` 注册。对于双向 TLS，用 :c:func:`fota_http_tls_add_client_cert` 注册
客户端
证书和密钥。

对端验证默认是必需的，且
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_PEER_VERIFY` 在生产环境应保持
默认值。URL 中的主机名会
与证书进行验证。当 URL 携带 IP 地址且
证书没有匹配条目时，在 ``tls_hostname`` 参数传入期望的名称。

证书有效期仅在
:kconfig:option:`CONFIG_MBEDTLS_HAVE_TIME_DATE` 启用时才被强制，这要求
在第一次下载前设备上具有正确的挂钟。TLS 1.3 可用
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_VERSION_1_3` 选择。

shell 命令
**************

启用 :kconfig:option:`CONFIG_FOTA_HTTP_SHELL` 时，``fota`` 命令
从控制台暴露该库：

.. code-block:: console

   fota download <url> [resume] [image=<n>]   下载映像
   fota cancel                                中止进行中的下载
   fota apply [permanent] [image=<n>]         下次复位时启动下载的映像
   fota confirm [image]                       确认运行中的映像
   fota status                                显示映像和确认状态
   fota erase [image]                         擦除次要槽

完整的使用说明参见 :zephyr:code-sample:`fota-http` 示例。

API 参考
*************

.. doxygengroup:: fota_http
