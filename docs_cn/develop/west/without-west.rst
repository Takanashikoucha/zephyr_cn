.. _no-west:

用
Zephyr
而
不
用
west
#########################

本
页
提供
用
Zephyr
而
不
用
west
的
信息。
这
对
初学者
不
推荐
因为
涉及
额外
的
工作。
特别
是，
你
将
必须
"手动"
做
工作
来
替换
这些
功能：

- clone
  Zephyr
  使用
  的
  额外
  源
  代码
  仓库
  除
  主
  zephyr
  仓库
  外
  并
  保持
  它们
  更新
- 向
  Zephyr
  构建
  系统
  指定
  这些
  仓库
  的
  位置
- 烧录
  和
  调试
  而
  不
  理解
  相关
  主机
  工具
  的
  详细
  用法

.. note::

   如果
   你
   之前
   安装
   了
   west
   并
   想
   停止
   使用
   它，
   先
   卸载
   它：

   .. code-block:: console

      pip3
      uninstall
      west

   否则，
   Zephyr
   的
   构建
   系统
   会
   找到
   它
   并
   可能
   尝试
   使用
   它。

获取
源
------------------

除
了
下载
zephyr
源
代码
仓库
本身，
你
将
需要
手动
clone
:term:`west
manifest`
文件
内部
列出
的
额外
projects。

.. code-block:: console

   mkdir
   zephyrproject
   cd
   zephyrproject
