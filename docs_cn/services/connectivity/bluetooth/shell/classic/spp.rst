Bluetooth:
Classic:
SPP
Shell
#############################

这
document
describe
如何
运行
Bluetooth
Classic
SPP
functionality。
:code:`spp`
command
expose
Bluetooth
Classic
SPP
Shell
commands。

Commands
********

:code:`spp`
commands：

.. code-block::
   console

   uart:~$
   spp
   spp
   -
   Bluetooth
   SPP
   sh
   commands
   Subcommands:
     register_with_channel
  :
      <channel>
      [limited
      credit
      value]
      [hold_credit]
     register_with_uuid
     :
      <bt-uuid16(e.g.
      1101)|bt-uuid32|bt-uuid128(e.g.
                          00001101-0000-1000-8000-00805F9B34FB)>
      [limited
                          credit
      value]
      [hold_credit]
     connect_by_channel
     :
      <channel>
      [limited
      credit
      value]
      [hold_credit]
     connect_by_uuid
        :
      <bt-uuid16(e.g.
      1101)|bt-uuid32|bt-uuid128(e.g.
                          00001101-0000-1000-8000-00805F9B34FB)>
      [limited
                          credit
      value]
      [hold_credit]
     send
                   :
      send
      [length
      of
      packet(s)]
     rls
                    :
      [overrun|parity|framing]
     disconnect
             :
      [none]
     recv_complete
          :
      [none]

Server
Register
***************

.. tabs::

   .. group-tab::
      Register
      with
      channel

      .. code-block::
         console

         uart:~$
         spp
         register_with_channel
         9
         SPP:
         server
         registered
         (channel=9)
