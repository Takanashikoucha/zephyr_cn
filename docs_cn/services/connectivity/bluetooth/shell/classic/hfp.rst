Bluetooth:
Classic:
HFP
Shell
###############################

这
document
describe
如何
运行
Bluetooth
Classic
HFP
functionality。
:code:`hfp`
command
expose
Bluetooth
Classic
HFP
Shell
commands。

有
两
个
sub
commands
:code:`hfp
hf`
和
:code:`hfp
ag`。

:code:`hfp
hf`
用于
Hands
Free
Profile
（HF）
functionality
:code:`hfp
ag`
用于
Audio
Gateway
（AG）
functionality。

Commands
********

所有
commands
只
能
在
ACL
connection
被
established
之后
使用
除了
:code:`hfp
hf
reg`
和
:code:`hfp
ag
reg`。

:code:`hfp`
commands：

.. code-block::
   console

   uart:~$
   hfp
   hfp
   -
   Bluetooth
   HFP
   shell
   commands
   Subcommands:
     hf
  :
      HFP
      HF
      shell
      commands
     ag
  :
      HFP
      AG
      shell
      commands

:code:`hfp
hf`
commands：

.. code-block::
   console

   uart:~$
   hfp
   hf
   hf
   -
   HFP
   HF
   shell
   commands
   Subcommands:
     reg
                          :
      [none]
     connect
                      :
      <channel>
     disconnect
                   :
      [none]
     sco_disconnect
               :
      [none]
     cli
                          :
      <enable/disable>
     vgm
                          :
      <gain>
