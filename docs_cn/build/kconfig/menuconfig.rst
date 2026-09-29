.. _menuconfig:

交互式 Kconfig 接口
##############################

有两个
交互式
配置
接口
可用
于
探索
可用
的
Kconfig 选项
并
进行
临时
更改：
``menuconfig`` 和
``guiconfig``。
``menuconfig`` 是
基于
curses 的
接口，
在
终端
中
运行，
而
``guiconfig`` 是
图形
配置
接口。

.. note::

   配置
   也
   可以
   通过
   手动
   编辑
   应用
   构建
   目录
   中
   的
   :file:`zephyr/.config`
   来
   更改。
   使用
   配置
   接口
   之一
   通常
   更
   方便，
   因为
   它们
   正确
   处理
   配置
   符号
   之间
   的
   依赖
   关系。

   如果
   你
   尝试
   在
   :file:`zephyr/.config` 中
   启用
   一个
   依赖
   未
   满足
   的
   符号，
   赋值
   将
   被
   忽略
   并
   在
   重新
   配置
   时
   被
   覆盖。

要
使
设置
永久
化，
你
应该
在
:file:`*.conf` 文件
中
设置
它，
如
:ref:`setting_configuration_values` 中
所述。

.. tip::

   保存
   最小
   配置
   文件
   （在
   menuconfig 中
   例如
   使用
   :kbd:`D`）
   并
   检查
   它
   在
   使
   设置
   永久
   化
   时
   可能
   很有
   用。
   最小
   配置
   文件
   只
   列出
   与其
   默认
   值
   不同
   的
   符号。

要
运行
配置
接口
之一，
做
以下
事情：

#. 使用
   ``west`` 或
   ``cmake`` 按
   通常
   方式
   构建
   你的
   应用：

   .. zephyr-app-commands::
      :tool: all
      :cd-into:
      :board: <board>
      :goals: build
      :compact:

#. 要
   运行
   基于
   终端
   的
   ``menuconfig`` 接口，
   使用
   以下
   命令
   之一：

   .. code-block:: bash

      west build -t menuconfig

   .. code-block:: bash

      ninja menuconfig

   要
   运行
   图形
   ``guiconfig``，
   使用
   以下
   命令
   之一：

   .. code-block:: bash

      west build -t guiconfig

   .. code-block:: bash

      ninja guiconfig

   .. note::

      如果
      你
      尝试
      运行
      ``guiconfig`` 时
      得到
      ``tkinter`` 的
      导入
      错误，
      你
      缺少
      必需
      的
      包。
      见
      :ref:`installation_linux`。
      你
      需要
      的
      包
      通常
      叫
      类似
      ``python3-tk``/``python3-tkinter`` 的
      名字。

      尽管
      ``tkinter`` 是
      标准
      库
      的
      一部分，
      许多
      Python 安装
      默认
      不
      包含
      它。

   两个
   接口
   显示
   如下：

   .. figure:: menuconfig.png
      :alt: menuconfig 接口

   .. figure:: guiconfig.png
      :alt: guiconfig 接口

   ``guiconfig``
   始终
   在
   底部
   窗口
   窗格
   中
   显示
   帮助
   文本
   和
   与
   当前
   选中
   项
   相关
   的
   其他
   信息。
   在
   终端
   接口
   中，
   按
   :kbd:`?` 查看
   相同
   信息。

   .. note::

      如果
      你
      偏好
      在
      ``guiconfig`` 接口
      中
      工作，
      那么
      在
      *单
      菜单
      模式*
      中
      检查
      你
      对
      Kconfig 文件
      做的
      任何
      更改
      是
      一个
      好
      主意，
      这
      通过
      顶部
      的
      复选框
      切换。
      与
      完整
      树
      模式
      不同，
      单
      菜单
      模式
      会
      区分
      使用
      ``config`` 定义
      的
      符号
      和
      使用
      ``menuconfig`` 定义
      的
      符号，
      显示
      在
      ``menuconfig`` 接口
      中
      看起来
      是
      什么
      样子。

#. 在
   ``menuconfig`` 接口
   中
   按
   如下
   方式
   更改
   配置
   值：

   * 使用
     箭头
     键
     导航
     菜单。
     也
     支持
     常用
     `Vim
     <https://www.vim.org>`__
     键
     绑定。

   * 使用
     :kbd:`Space` 和
     :kbd:`Enter` 进入
     菜单
     并
     切换
     值。
     菜单
     旁边
     显示
     ``--->``。
     按
     :kbd:`ESC` 返回
     父
     菜单。

     布尔
     配置
     选项
     用
     :guilabel:`[ ]` 括号
     显示，
     而
     数值
     和
     字符串
     值
     的
     配置
     符号
     用
     :guilabel:`( )` 括号
     显示。
     不能
     更改
     的
     符号
     值
     显示
     为
     :guilabel:`- -` 或
     :guilabel:`*-*`。

     .. note::

        你
        也
        可以
        按
        :kbd:`Y` 或
        :kbd:`N` 将
        布尔
        配置
        符号
        设置
        为
        对应
        值。

   * 按
     :kbd:`?` 显示
     当前
     选中
     符号
     的
     信息，
     包括
     其
     帮助
     文本。
     按
     :kbd:`ESC` 或
     :kbd:`Q` 从
     信息
     显示
     返回
     菜单。

   在
   ``guiconfig`` 接口
   中，
   要么
   点击
   符号
   旁边
   的
   图像
   来
   更改
   其
   值，
   要么
   双击
   带
   符号
   的
   行
   （这
   只有
   在
   符号
   没有
   子
   项
   时
   才
   有效，
   因为
   双击
   带
   子
   项
   的
   符号
   打开/关闭
   其
   菜单
   而不是
   更改
   值）。

   ``guiconfig``
   也
   支持
   键盘
   控制，
   与
   ``menuconfig``
   类似。

#. 在
   ``menuconfig`` 接口
   中
   按
   :kbd:`Q` 会
   带出
   保存
   并
   退出
   对话框
   （如果
   有
   更改
   要
   保存）：

   .. figure:: menuconfig-quit.png
      :alt: 保存
      并
      退出
      对话框

   按
   :kbd:`Y` 将
   内核
   配置
   选项
   保存
   到
   默认
   文件名
   （:file:`zephyr/.config`）。
   除非
   你
   在
   实验
   不同
   配置，
   你
   通常
   会
   保存
   到
   默认
   文件名。

   ``guiconfig`` 接口
   在
   退出
   时
   如果
   已
   修改
   也
   会
   提示
   保存
   配置。

   .. note::

      构建
      期间
      使用
      的
      配置
      文件
      始终
      是
      :file:`zephyr/.config`。
      如果
      你
      有
      另一个
      保存
      的
      配置
      想
      用
      它
      构建，
      复制
      它
      到
      :file:`zephyr/.config`。
      确保
      备份
      你的
      原始
      配置
      文件。

      也
      注意
      在
      Linux 和
      macOS 上，
      以
      ``.`` 开头
      的
      文件名
      默认
      不
      被
      ``ls`` 列出。
      使用
      ``-a`` 标志
      查看
      它们。

在
菜单
树
中
查找
符号
并
导航
到
它
可能
很
麻烦。
要
直接
跳转
到
符号，
按
:kbd:`/` 键
（这在
``guiconfig`` 中
也
有效）。
这
会
带出
以下
对话框，
你
可以
按
名称
搜索
符号
并
跳转
到
它们。
在
``guiconfig`` 中，
你
也
可以
直接
在
对话框
中
更改
符号
值。

.. figure:: menuconfig-jump-to.png
   :alt: menuconfig
   跳转
   对话框

.. figure:: guiconfig-jump-to.png
   :alt: guiconfig
   跳转
   对话框

如果
你
跳转
到
一个
当前
不可见
的
符号
（例如，
由于
依赖
未
满足），
那么
*显示
全部
模式*
将
被
启用。
在
显示
全部
模式
中，
所有
符号
都
被
显示，
包括
当前
不可见
的
符号。
要
关闭
显示
全部
模式，
在
``menuconfig`` 中
按
:kbd:`A` 或
在
``guiconfig`` 中
按
:kbd:`Ctrl-A`。

.. note::

   如果
   当前
   菜单
   中
   没有
   可见
   项，
   显示
   全部
   模式
   不
   能
   被
   关闭。

要
弄清楚
你
跳转
到
的
符号
为什么
不可见，
检查
其
依赖，
要么
在
``menuconfig`` 中
按
:kbd:`?`，
要么
在
``guiconfig`` 底部
的
信息
窗格
中。
如果
你
发现
符号
依赖
另一个
未
启用
的
符号，
你可以
依次
跳转
到
那个
符号
查看
它
是否
可以
被
启用。

.. note::

   在
   ``menuconfig`` 中，
   你
   可以
   按
   :kbd:`Ctrl-F` 在
   跳转
   对话框
   中
   查看
   当前
   选中
   项
   的
   帮助
   而
   不
   离开
   对话框。

关于
``menuconfig`` 和
``guiconfig`` 的
更多
信息，
见
:zephyr_file:`menuconfig.py
<scripts/kconfig/menuconfig.py>` 和
:zephyr_file:`guiconfig.py
<scripts/kconfig/guiconfig.py>` 顶部
的
Python
docstring。
