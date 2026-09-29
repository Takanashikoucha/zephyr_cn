.. _toolchain_gnuarmemb:

GNU
Arm
Embedded
################

#. 下载
   并
   安装
   `GNU
   Arm
   Embedded`_
   构建
   用于
   你
   的
   操作
   系统
   并
   解压
   到
   你
   的
   文件
   系统。

   .. note::

      在
      Windows
      上，
      本
      指南
      假设
      你
      安装
      到
      目录
      :file:`C:\\gnu_arm_embedded`。
      你
      也
      可以
      选择
      ARM
      GCC
      安装器
      使用
      的
      默认
      安装
      路径，
      在
      那
      种
      情况
      下
      你
      需要
      相应
      调整
      下面
      指南
      中
      的
      路径。

   .. warning::

      在
      macOS
      Catalina
      或
      之后
      你
      可能
      需要
      :ref:`change
      a
      security
      policy
      <mac-gatekeeper>`
      为
      工具链
      能
      从
      终端
      运行。

#. :ref:`Set
   these
   environment
   variables
   <env_vars>`：

   - 设置
     :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
     为
     ``gnuarmemb``。
   - 设置
     :envvar:`GNUARMEMB_TOOLCHAIN_PATH`
     为
     工具链
     安装
     目录。

#. 要
   检查
   你
   在
   当前
   环境
   中
   正确
   设置
   了
   这些
   变量，
   遵循
   这些
   示例
   shell
   会话
   （:envvar:`GNUARMEMB_TOOLCHAIN_PATH`
   值
   在
   你
   的
   系统
   上
   可能
   不同）：

   .. code-block:: console

      #
      Linux,
      macOS:
      $
      echo
      $ZEPHYR_TOOLCHAIN_VARIANT
      gnuarmemb
      $
      echo
      $GNUARMEMB_TOOLCHAIN_PATH
      /home/you/Downloads/gnu_arm_embedded

      #
      Windows:
      >
      echo
      %ZEPHYR_TOOLCHAIN_VARIANT%
      gnuarmemb
      >
      echo
      %GNUARMEMB_TOOLCHAIN_PATH%
      C:\gnu_arm_embedded

   .. warning::

      在
      macOS
      上，
      如果
      你
      在
      建议
      的
      过程
      中
      遇到
      问题，
      brew
      上
      有
      一
      个
      非
      官方
      包
      可能
      帮助
      你。
      运行
      ``brew
      install
      gcc-arm-embedded``
      并
      配置
      变量
