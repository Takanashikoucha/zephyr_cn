.. _fota_http:

Firmware Over-the-Air over HTTP
###############################

Overview
********

FOTA HTTP library 从 HTTP server 下载 firmware image（并
直接写入当前未运行的 MCUboot slot。
然后允许 application 请求 swap、confirm 新 image 或
erase slot。与 :ref:`hawkBit or UpdateHub <ota>` 不同（无 device
management protocol 参与：任何能 serve file 的 web server 可
作为 update source（这使其适合简单 deployments
和 bench testing。

Image 到达时通过 :ref:`flash_img_api` 流式写入 flash（
故其 size 不受 RAM 限制。Slot 在
写入期间渐进 erase（且 slot 的 MCUboot trailer 在
第一 byte 落地前清除（故前一个 image 的
残留永不会被误认为 pending swap。

下载后（library 从 flash 读回 MCUboot header（
data 非 image 时以 ``-ENOEXEC`` 失败。其不
验证 signature：MCUboot 在 image 启动前做此事（且
该 check 决定 image 是否运行。可选的 SHA-256
与 caller 提供的 digest 比较可用
:kconfig:option:`CONFIG_FOTA_HTTP_SHA256_CHECK`（以在
reboot 前捕获损坏
transfer。被该比较拒绝的 image（或
被下面 downgrade check 拒绝的 image）从 slot 中 erase。
部分失败的下载后（:c:func:`fota_http_apply` 拒绝 slot（直到另一
写入它的下载成功（而 partial data 留在原处用于
resume。

Update cycle
************

典型 sequence 为：

#. :c:func:`fota_http_download` 或 :c:func:`fota_http_download_async`
   将 image 获取到 secondary slot。可选
   :c:struct:`fota_http_download_params` members ``sha256``、``resume``
   和 TLS 相关的仅在其 Kconfig option 启用时存在。
#. :c:func:`fota_http_apply` 将 image 标记为 test boot（或
   permanent。
#. Device reboot（且 MCUboot swap 入 image。
#. Test boot 时（application 验证自身并调用
   :c:func:`fota_http_confirm`。无该调用（下次 reboot 使
   MCUboot 回退到前一个 image。

Revert 步骤需带 revert 支持的 MCUboot mode（如
swap-using-move 或 swap-using-offset。overwrite-only mode 中（
swap 发生即前一个 image 消失（且 confirmation 无效果（
故检查 board 的 sysbuild configuration 选择哪种 mode。

test image 运行期间（secondary slot 持有 MCUboot 将
回退的 image（故 :c:func:`fota_http_download` 以 ``-EPERM`` 拒绝（直到
调用 :c:func:`fota_http_confirm`。

Threads and stack
*****************

:c:func:`fota_http_download` 阻塞调用 thread 整个
transfer 期间（且需足够 stack 供 HTTP client（https 时供
TLS handshake。用 :kconfig:option:`CONFIG_FOTA_HTTP_ASYNC`（
:c:func:`fota_http_download_async` 在
library 拥有的 thread 上运行相同 transfer（size 由
:kconfig:option:`CONFIG_FOTA_HTTP_THREAD_STACK_SIZE` 决定（且通过
completion callback 报告
result。Shell command 选择
asynchronous variant（故 shell stack size 无关紧要。
仅调用 :c:func:`fota_http_download` 的 Applications 保持其
禁用（且不付出 thread stack 代价。

一次仅运行一个 download。:c:func:`fota_http_cancel` 在下一
fragment 到达或 request 超时
时中止进行中的 transfer。

Redirects and resume
********************

Status 为 301、302、303、307 或 308 的 Responses 跟随
最多 :kconfig:option:`CONFIG_FOTA_HTTP_MAX_REDIRECTS` 次。绝对和
仅 path 的 ``Location`` headers 均接受。

用 :kconfig:option:`CONFIG_FOTA_HTTP_RESUME`（transfer 运行期间和
失败时 download offset 存储在 settings 中。稍后
设置 ``resume`` parameter 的 download 从该 offset 用 HTTP
``Range`` request 继续。仅当 URL 和 image index
与中断的 download 匹配时重用 offset（且当
server 发送 ``ETag`` 或
``Last-Modified`` header 时（request 带 ``If-Range``（故
server 上变更的 file 从头重新获取。忽略 ``Range`` header 并以完整 file 应答的
server 从零重启 transfer（``416 Range Not Satisfiable`` 应答
同样如此（这是 file 变得比存储
offset 短时 server 发送的。过长无法存储的 validator 也丢弃
存储的 progress（故
下次 download 从头开始（而非对可能已变更的 file resume。
image 完成时清除 offset。

Multiple images
***************

多于一个 updateable image 的 layout 中（``image_index``
parameter 选择 download 去往哪个 secondary slot。
:c:func:`fota_http_apply` 和 :c:func:`fota_http_confirm` 均接受
相同 index（故携带第二 device firmware 的 layout
仅 confirm 此 device 验证的。须一起运行若干 images 时（
reboot 前下载并应用所有：MCUboot 验证
整个集合并一次 swap 入（且之后 confirm 每个（因为
未 confirm 的 image 单独回退。
:c:func:`fota_http_confirm_pending` 仅报告 image 0（故
更新若干 images 的 application 自行跟踪其余。
用 :kconfig:option:`CONFIG_FOTA_HTTP_REJECT_DOWNGRADE` 的 downgrade check 仅覆盖 image 0。

用 direct-XIP bootloaders（image 运行的 slot 在
link 时固定（故 device 须获取为空闲 slot 构建的 image 变体。
:c:func:`fota_http_get_download_slot` 报告其为哪个 slot。这仅
覆盖单 image layouts：第一个之后每个 image（library
总上传到 pair 的奇数 slot（这对
swap 和 overwrite modes 正确（但对 direct-XIP 不正确。

Downgrade protection
********************

:kconfig:option:`CONFIG_FOTA_HTTP_REJECT_DOWNGRADE` 将
下载的 header 中的 version 与运行 image 比较（
其较旧时使 download 失败（并 erase 被拒绝 image 以防误
apply。此为 application 的便利 check。强制
policy 应属于 bootloader（参见 MCUboot downgrade prevention 和
hardware rollback protection options。

TLS
***

启用 :kconfig:option:`CONFIG_FOTA_HTTP_TLS` 时接受
``https`` URLs。Server 的 CA certificate 在
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_SEC_TAG` 下查找（或在
download parameters 传入的 tags 下（且可用
:c:func:`fota_http_tls_add_ca` 或直接用
:c:func:`tls_credential_add` 注册。对 mutual TLS（用 :c:func:`fota_http_tls_add_client_cert` 注册
client
certificate 和 key。

Peer verification 默认必需（且
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_PEER_VERIFY` 生产环境应保持
默认。URL 中的 host name 与
certificate 验证。URL 携带 IP address 且
certificate 无匹配 entry 时（在 ``tls_hostname`` parameter 传入期望 name。

Certificate validity dates 仅在
:kconfig:option:`CONFIG_MBEDTLS_HAVE_TIME_DATE` 启用时强制（其需
第一次下载前 device 上正确 wall clock。TLS 1.3 可用
:kconfig:option:`CONFIG_FOTA_HTTP_TLS_VERSION_1_3` 选择。

Shell commands
**************

启用 :kconfig:option:`CONFIG_FOTA_HTTP_SHELL` 时（``fota`` command
从 console 暴露 library：

.. code-block:: console

   fota download <url> [resume] [image=<n>]   download an image
   fota cancel                                abort the download in progress
   fota apply [permanent] [image=<n>]         boot the downloaded image on the next reset
   fota confirm [image]                       confirm the running image
   fota status                                show images and confirmation state
   fota erase [image]                         erase the secondary slot

完整 walkthrough 参见 :zephyr:code-sample:`fota-http` sample。

API Reference
*************

.. doxygengroup:: fota_http
