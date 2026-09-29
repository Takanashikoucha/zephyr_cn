.. _toolchain_cadence_xcc:

Cadence
Tensilica
Xtensa
C/C++
Compiler
（XCC）
#############################################

#. 获取
   目标
   特定
   SoC
   的
   Tensilica
   Software
   Development
   Toolkit。
   这
   通常
   包含
   两
   个
   部分：

   * Xtensa
     Xplorer
     包含
     必需
     的
     可执行
     文件
     和
     库。

   * 一
     个
     SoC
     特定
     的
     add-on
     要
     安装
     在
     Xtensa
     Xplorer
     之上。

     * 这
       个
       add-on
       允许
       编译器
       为
       手头
       的
       SoC
       生成
       代码。

#. 安装
   Xtensa
   Xplorer
   然后
   SoC
   add-on。

   * 遵循
     Cadence
     的
     说明
     如何
     安装
     SDK。

   * 取决于
     SDK，
     有
     两
     套
     编译器：

     * 基于
       GCC
       的
       编译器：
       ``xt-xcc``
       和
       其
       朋友。

     * 基于
       Clang
       的
       编译器：
       ``xt-clang``
       和
       其
       朋友。

#. 确保
   你
   已
   获取
   使用
   SDK
   的
   许可，
   或
   有
   访问
   远程
   许可
   服务器
   的
   权限。

#. :ref:`Set
   these
   environment
   variables
   <env_vars>`：

   * 设置
     :envvar:`ZEPHYR_TOOLCHAIN_VARIANT`
     为
     ``xcc``
     或
     ``xt-clang``。
   * 设置
     :envvar:`XTENSA_TOOLCHAIN_PATH`
     为
     工具链
     安装
     目录。

   * 有
     两
     种
     方式
     指定
     要
     使用
     的
     SoC
     ID
     和
     SDK
     版本。
     它们
     互
     斥，
     不能
     一起
     使用。

     #. 当
        为
        单一
        SoC
        构建
        时：

        * 设置
          :envvar:`XTENSA_CORE`
          为
          应用
          目标
          的
          SoC
          ID。
        * 设置
          :envvar:`TOOLCHAIN_VER`
          为
          Xtensa
          SDK
          版本。

     #. 当
        为
        多
        个
        SoCs
        构建
        时，
        对
        每个
        SoC
        和
        board
        组合：

        * 设置
          :envvar:`XTENSA_CORE_{normalized_board_target}`
          为
          应用
          目标
          的
          SoC
          ID。
        * 设置
          :envvar:`TOOLCHAIN_VAR_{normalized_board_target}`
          为
          Xtensa
          SDK
          版本。
