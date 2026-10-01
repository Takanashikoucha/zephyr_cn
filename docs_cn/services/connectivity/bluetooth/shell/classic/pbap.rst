Bluetooth:
Classic:
PBAP
Shell
###############################

本文
档
描述
如何
运行
Bluetooth
Classic
PBAP
（Phonebook
Access
Profile，
电话簿
访问
配置文件）
功能。
:code:`pbap`
命令
暴露
Bluetooth
Classic
PBAP
Shell
命令。

有
两
个
子
命令
:code:`pbap
pce`
和
:code:`pbap
pse`。

:code:`pbap
pce`
用于
Phonebook
Client
Equipment
（PCE，
电话簿
客户端
设备）
功能
，
:code:`pbap
pse`
用于
Phonebook
Server
Equipment
（PSE，
电话簿
服务器
设备）
功能。

Commands
********

所有
命令
只
能
在
ACL
连接
建立
之后
使用
，
除了
:code:`pbap
pce
sdp_reg`
和
:code:`pbap
pse
rfcomm_register`
和
:code:`pbap
pse
l2cap_register`。

:code:`pbap`
命令：

.. code-block::
   console

   uart:~$
   pbap
   pbap
   -
   Bluetooth
   pbap
   shell
   commands
   Subcommands:
     alloc_buf
                        :
      Alloc
      tx
      buffer
     release_buf
                       :
      Free
      allocated
      tx
      buffer
     pce
                               :
      Client
      sets
     pse
                               :
      Server
      sets
     add_header_auth_challenge
         :
      <password>
     add_header_auth_response
          :
      <password>
     add_ap
                            :
      add
      application
      param

:code:`pbap
pce`
命令：

.. code-block::
   console

   uart:~$
   pbap
   pce
   pce
   -
   Client
   sets
   Subcommands:
     sdp_reg
                          :
      [none]
     sdp_discover
                       :
      [none]
     connect_rfcomm
                     :
      <channel>
     disconnect_rfcomm
                      :
      [none]
     connect_l2cap
                    :
      <channel>
     disconnect_l2cap
                     :
      [none]
     connect
                    :
      <mopl>
     disconnect
                       :
      [none]
     pull_pb
                      :
      <name>
      [srmp]
     pull_vcard_listing
                       :
      <name>
      [srmp]
     pull_vcard_entry
                     :
      <name>
      [srmp]
     set_phone_book
                     :
      <Flags>
      [name]
     abort
                      :
      [none]

:code:`pbap
pse`
命令：

.. code-block::
   console

   uart:~$
   pbap
   pse
   pse
   -
   Server
   sets
   Subcommands:
     rfcomm_register
                      :
      [none]
     l2cap_register
                     :
      [none]
     register
                       :
      [none]
     connect_rsp
                    :
      <mopl>
      <rsp:
      unauth,
      success,
      error>
      [rsp_code]
     disconnect_rsp
                     :
      <rsp:
      success,
      error>
      [rsp_code]
     pull_phone_book_rsp
                        :
      <rsp:
      noerror,
      error>
      [rsp_code]
      [srmp]
     pull_vcard_listing_rsp
                           :
      <rsp:
      noerror,
      error>
      [rsp_code]
      [srmp]
     pull_vcard_entry_rsp
                         :
      <rsp:
      noerror,
      error>
      [rsp_code]
      [srmp]
     set_phone_book_rsp
                       :
      <rsp:
      success,
      error>
      [rsp_code]
     abort_rsp
                      :
      <rsp:
      success,
      error>
      [rsp_code]

:code:`pbap
add_ap`
（应用
参数）
命令：

.. code-block::
   console

   uart:~$
   pbap
   add_ap
   add_ap
   -
   add
   application
   param
   Subcommands:
     Order
                            :
      <indexed/alphanumeric/phonetic>
     SearchValue
                      :
      <text>
     SearchAttribute
                    :
      <name/number/sound>
     MaxListCount
                     :
      <0x0000-0xffff>
     ListStartOffset
                    :
      <0x0000-0xffff>
     PropertySelector
                     :
      <64
      bits
      mask
      :
      bt_pbap_appl_param_property_mask>
     Format
                           :
      <v2.1/v3.0>
     PhonebookSize
                    :
      <0x0000-0xffff>
     NewMissedCalls
                     :
      <0x00-0xff>
     PrimaryFolderVersion
                         :
      <16bytes>
     SecondaryFolderVersion
                           :
      <16bytes>
     vCardSelector
                    :
      <64
      bits
      mask
      :
      bt_pbap_appl_param_property_mask>

Usage
Examples
**************

Register
PSE
=================

1.
注册
PSE
RFCOMM
服务器：

.. code-block::
   console

   uart:~$
   pbap
   pse
   rfcomm_register
   RFCOMM
   server
   (channel
   01)
   is
   registered

2.
注册
PSE
L2CAP
服务器：

.. code-block::
   console

   uart:~$
   pbap
   pse
   l2cap_register
   L2cap
   server
   (psm
   01)
   is
   registered

3.
注册
PSE：

.. code-block::
   console

   uart:~$
   pbap
   pse
   register

4.
接受
PCE
连接
并
响应：

.. code-block::
   console

   uart:~$
   pbap
   alloc_buf
   uart:~$
   pbap
   pse
   connect_rsp
   300
   success
   pbap
   connect
   version
   1,
   mopl
   256
   Connection
   established
   with
   authentication

5.
与
PCE
断开
连接：

.. code-block::
   console

   uart:~$
   pbap
   alloc_buf
   uart:~$
   pbap
   pse
   disconnect_rsp
   success
   pbap
   disconnect
   requested
   by
   pce

Pull
Phonebook
**************

从
PSE
拉取
完整
电话簿：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pce
         pull_pb
         "telecom/pb"
         pbap
         pull
         phonebook
         result
         Continue
         Application
         Parameters
         (length:
         2):
           PhonebookSize:
           0x0002
           (2)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN;CHARSET=UTF-8:descvs
         N;CHARSET=UTF-8:descvs
         END:VCARD
         =========body=========

         please
         send
         pull
         cmd
         again
         uart:~$
         pbap
         pce
         pull_pb
         "telecom/pb"
         pbap
         pull
         phonebook
         result
         Success
         Application
         Parameters
         (length:
         2):
           PhonebookSize:
           0x0002
           (2)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN;CHARSET=UTF-8:descvs
         N;CHARSET=UTF-8:descvs
         END:VCARD
         =========body=========

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         pull_phone_book
         request
         name
         =
         telecom/pb
         Application
         Parameters
         (length:
         0):

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_phone_book_rsp
         noerror
         Suspend
         after
         sending
         a
         single
         response
         and
         await
         the
         PCE
         request

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_phone_book_rsp
         noerror
         Keep
         sending
         responses
         continuously
         until
         rsp_code
         is
         success

Pull
vCard
Listing
******************

拉取
vCard
列表
以
发现
联系人：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         add_ap
         MaxListCount
         0x0005
         uart:~$
         pbap
         add_ap
         ListStartOffset
         0x0000
         uart:~$
         pbap
         pce
         pull_vcard_listing
         "telecom/pb"
         pbap
         pull
         vcard_listing
         result
         Continue
         Application
         Parameters
         (length:
         6):
           MaxListCount:
           0x0005
           (5)
           ListStartOffset:
           0x0000
           (0)

         =========body=========
         <?xml
         version="1.0"?>
         <!DOCTYPE
         vcard-listing
         SYSTEM
         "vcard-listing.dtd">
         <vCard-listing
         version="1.0">
         <card
         handle="1.vcf"
         name="qwe"/>
         <card
         handle="2.vcf"
         name="qwe"/>
         =========body=========

         please
         send
         pull
         cmd
         again
         uart:~$
         pbap
         pce
         pull_vcard_listing
         "telecom/pb"
         pbap
         pull
         vcard_listing
         result
         Success
         =========body=========
         <card
         handle="1.vcf"
         name="qwe"/>
         <card
         handle="2.vcf"
         name="qwe"/>
         /<vCard-listing>
         =========body=========

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         pull_vcard_listing
         request
         name
         =
         telecom/pb
         Application
         Parameters
         (length:
         6):
           MaxListCount:
           0x0005
           (5)
           ListStartOffset:
           0x0000
           (0)

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_vcard_listing_rsp
         noerror
         Suspend
         after
         sending
         a
         single
         response
         and
         await
         the
         PCE
         request

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_vcard_listing_rsp
         noerror

Pull
vCard
Entry
****************

拉取
特定
vCard
条目：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         add_ap
         Format
         v2.1
         uart:~$
         pbap
         pce
         pull_vcard_entry
         "telecom/pb/1.vcf"
         pbap
         pull
         vcard_entry
         result
         Continue
         Application
         Parameters
         (length:
         1):
           Format:
           0x00
           (vCard
           2.1)

         =========body=========
         BEGIN:VCARD
         VERSION:2.1
         FN:
         N:
         TEL;X-0:1155
         =========body=========

         uart:~$
         pbap
         pce
         pull_vcard_entry
         "telecom/pb/1.vcf"
         pbap
         pull
         vcard_entry
         result
         Success

         =========body=========
         X-IRMC-CALL-DATETIME;DIALED:20220913T110607
         END:VCARD
         =========body=========

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         pull_vcard_entry
         request
         name
         =
         telecom/pb/1.vcf
         Application
         Parameters
         (length:
         1):
           Format:
           0x00
           (vCard
           2.1)

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_vcard_entry_rsp
         noerror
         Suspend
         after
         sending
         a
         single
         response
         and
         await
         the
         PCE
         request

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         pull_vcard_entry_rsp
         noerror

Set
Phone
Book
**************

更改
当前
电话簿
目录：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pce
         set_phone_book
         0x02
         "telecom"
         PBAP
         set
         phonebook
         result
         OK

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pce
         set_phone_book
         0x02
         "pb"
         PBAP
         set
         phonebook
         result
         OK

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pce
         set_phone_book
         0x02
         PBAP
         set
         phonebook
         result
         OK

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         set_phone_book
         request
         set
         phonebook
         to
         children
         telecom
         folder

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         set_phone_book_rsp
         success

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         set_phone_book
         request
         set
         phonebook
         to
         children
         pb
         folder

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         set_phone_book_rsp
         success

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         set_phone_book
         request
         set
         phonebook
         to
         parent
         folder

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         set_phone_book_rsp
         success

Abort
Operation
***************

中止
进行
中
的
操作：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         pce
         abort
         abort
         success.

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         pbap_pse
         get
         receive
         abort
         req

         uart:~$
         pbap
         pse
         abort_rsp
         success

Authentication
**************

PBAP
可以
使用
OBEX
认证
建立
安全
连接。
认证
过程
涉及
质询
-
响应
机制。

带
认证
质询
的
PCE：

.. tabs::

   .. group-tab::
      PCE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         add_header_auth_challenge
         "password123"
         uart:~$
         pbap
         pce
         connect
         255
         pbap
         connect
         result
         Unauthorized,
         mopl
         255
         PSE
         requires
         authentication
         Action
         required:
           1.
           Allocate
           new
           tx_buf
           (pbap
           alloc_buf)
           2.
           Add
           auth_response
           header
           (pbap
           add_header_auth_response
           <password>)
           3.
           Add
           original
           auth_challenge
           header
           (pbap
           add_header_auth_challenge
           <password>)
           4.
           Re-send
           connect
           request
           (pbap
           pce
           connect
           <mopl>)

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         add_header_auth_response
         "password123"
         uart:~$
         pbap
         add_header_auth_challenge
         "password123"
         uart:~$
         pbap
         pce
         connect
         255
         pbap
         connect
         result
         Success,
         mopl
         255
         Connection
         ID:
         0x00000001
         Authentication
         verified
         successfully
         Connection
         established
         with
         authentication

   .. group-tab::
      PSE
      side

      .. code-block::
         console

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         register

         uart:~$
         pbap
         alloc_buf
         pbap
         connect
         version
         1,
         mopl
         255
         PCE
         authentication
         required
         -
         add
         auth_response
         to
         connect_rsp
         tx_buf

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         add_header_auth_challenge
         "password123"
         uart:~$
         pbap
         pse
         connect_rsp
         255
         unauth

         uart:~$
         pbap
         alloc_buf
         pbap
         connect
         version
         1,
         mopl
         255
         auth
         success
         Connection
         established
         with
         authentication

         uart:~$
         pbap
         alloc_buf
         uart:~$
         pbap
         pse
         connect_rsp
         255
         success