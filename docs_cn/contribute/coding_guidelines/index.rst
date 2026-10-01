.. _coding_guidelines:

编码指南
#################


主要规则
**********

编码指南规则基于 MISRA-C 2012，是 MISRA-C 的一个**子集**。该子集列在下表中，包含规则摘要、其 MISRA-C 严重级别，以及供参考的其他标准中的对应规则。

下表中的严重级别和其他引用仅供参考。所列规则对 Zephyr 均为必需，所有新代码都应遵循下列规则。


.. note::

    对于现有的 Zephyr 维护者和协作者，如果你无法通过你的雇主获得一份 MISRA-C 2012 副本，项目将提供有限数量的副本。如果你需要一份 MISRA-C 2012 副本，请发邮件至 safety@lists.zephyrproject.org，并说明你无法通过其他途径获得副本的原因，以及获得副本后预期做出的贡献。安全委员会将审查所有申请。


.. list-table:: 主要规则
    :header-rows: 1
    :widths: 12 50 15 15

    * -  Zephyr 规则
      -  描述
      -  MISRA-C 2012 引用
      -  CERT C 引用

         .. _MisraC_Dir_1_1:
    * -  1
      -  程序输出所依赖的任何实现定义行为都应被记录并理解
      -  `指令 1.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_01_01.c>`_
      -  | `FLP30-C <https://wiki.sei.cmu.edu/confluence/display/c/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters>`_
         | `MSC09-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC09-C.+Character+encoding%3A+Use+subset+of+ASCII+for+safety>`_
         | `EXP11-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP11-C.+Do+not+make+assumptions+regarding+the+layout+of+structures+with+bit-fields>`_

         .. _MisraC_Dir_2_1:
    * -  2
      -  所有源文件都应能编译且无任何编译错误
      -  `指令 2.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_02_01.c>`_
      -  N/A

         .. _MisraC_Dir_3_1:
    * -  3
      -  所有代码都应可追溯到已记录的需求
      -  `指令 3.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_03_01.c>`_
      -  N/A

         .. _MisraC_Dir_4_1:
    * -  4
      -  应最小化运行期失败
      -  `指令 4.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_01.c>`_
      -  N/A

         .. _MisraC_Dir_4_2:
    * -  5
      -  所有汇编语言的使用都应被记录
      -  `指令 4.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_02.c>`_
      -  N/A

         .. _MisraC_Dir_4_4:
    * -  6
      -  不应将代码段“注释掉”
      -  `指令 4.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_04.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Dir_4_5:
    * -  7
      -  同一命名空间中可见性重叠的标识符在排版上应无歧义
      -  `指令 4.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_05.c>`_
      -  `DCL02-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL02-C.+Use+visually+distinct+identifiers>`_

         .. _MisraC_Dir_4_6:
    * -  8
      -  应使用表示大小与符号性的 typedef 替代基本数值类型
      -  `指令 4.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_06.c>`_
      -  N/A

         .. _MisraC_Dir_4_7:
    * -  9
      -  如果函数返回错误信息，则应测试该错误信息
      -  `指令 4.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_07.c>`_
      -  N/A

         .. _MisraC_Dir_4_8:
    * -  10
      -  如果指向结构体或联合体（union）的指针在翻译单元内从未被解引用，则应隐藏该对象的实现
      -  | `指令 4.8 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_08_1.c>`_
         | `指令 4.8 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_08_2.c>`_
      -  `DCL12-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL12-C.+Implement+abstract+data+types+using+opaque+types>`_

         .. _MisraC_Dir_4_9:
    * -  11
      -  在函数与函数式宏可以互换的地方，应优先使用函数
      -  `指令 4.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_09.c>`_
      -  `PRE00-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE00-C.+Prefer+inline+or+static+functions+to+function-like+macros>`_

         .. _MisraC_Dir_4_10:
    * -  12
      -  应采取预防措施，防止头文件内容被包含多次
      -  `指令 4.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_10.c>`_
      -  `PRE06-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE06-C.+Enclose+header+files+in+an+include+guard>`_

         .. _MisraC_Dir_4_11:
    * -  13
      -  应检查传递给库函数的值的有效性
      -  `指令 4.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_11.c>`_
      -  N/A

         .. _MisraC_Dir_4_12:
    * - 14
      -  不应使用动态内存分配
      -  `指令 4.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_12.c>`_
      -  | `API03-C <https://wiki.sei.cmu.edu/confluence/display/c/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions>`_
         | `API04-C <https://wiki.sei.cmu.edu/confluence/display/c/API04-C.+Provide+a+consistent+and+usable+error-checking+mechanism>`_
         | `STR01-C <https://wiki.sei.cmu.edu/confluence/display/c/STR01-C.+Adopt+and+implement+a+consistent+plan+for+managing+strings>`_

         .. _MisraC_Dir_4_13:
    * -  15
      -  设计用于对资源执行操作的函数应按适当的顺序调用
      -  `指令 4.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_13.c>`_
      -  N/A

         .. _MisraC_Dir_4_14:
    * -  16
      -  应检查从外部来源接收的值的有效性
      -  `指令 4.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/D_04_14.c>`_
      -  N/A

         .. _MisraC_Rule_1_2:
    * -  17
      -  不应使用语言扩展
      -  `规则 1.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_01_02.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Rule_1_3:
    * -  18
      -  不应出现未定义行为或关键的未指定行为
      -  `规则 1.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_01_03.c>`_
      -  N/A

         .. _MisraC_Rule_2_1:
    * -  19
      -  项目中不应包含不可达代码
      -  | `规则 2.1 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_01_1.c>`_
         | `规则 2.1 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_01_2.c>`_
      -  `MSC12-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>`_

         .. _MisraC_Rule_2_2:
    * -  20
      -  不应存在死代码
      -  `规则 2.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_02.c>`_
      -  | `DCL22-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL22-C.+Use+volatile+for+data+that+cannot+be+cached>`_
         | `MSC12-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed>`_

         .. _MisraC_Rule_2_3:
    * -  21
      -  项目中不应包含未使用的类型声明
      -  `规则 2.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_03.c>`_
      -  N/A

         .. _MisraC_Rule_2_6:
    * -  22
      -  函数中不应包含未使用的标签声明
      -  `规则 2.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_06.c>`_
      -  N/A

         .. _MisraC_Rule_2_7:
    * -  23
      -  函数中不应存在未使用的参数
      -  `规则 2.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_02_07.c>`_
      -  N/A

         .. _MisraC_Rule_3_1:
    * -  24
      -  注释中不应使用 /* 或 // 字符序列
      -  `规则 3.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_03_01.c>`_
      -  `MSC04-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion>`_

         .. _MisraC_Rule_3_2:
    * -  25
      -  // 注释中不应使用行拼接
      -  `规则 3.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_03_02.c>`_
      -  N/A

         .. _MisraC_Rule_4_1:
    * -  26
      -  八进制和十六进制转义序列应被终止
      -  `规则 4.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_04_01.c>`_
      -  `MSC09-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC09-C.+Character+encoding%3A+Use+subset+of+ASCII+for+safety>`_

         .. _MisraC_Rule_4_2:
    * -  27
      -  不应使用三字符组（trigraph）
      -  `规则 4.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_04_02.c>`_
      -  `PRE07-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE07-C.+Avoid+using+repeated+question+marks>`_

         .. _MisraC_Rule_5_1:
    * -  28
      -  外部标识符应各不相同
      -  | `规则 5.1 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_01_1.c>`_
         | `规则 5.1 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_01_2.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_2:
    * -  29
      -  同一作用域和命名空间中声明的标识符应各不相同
      -  `规则 5.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_02.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_3:
    * -  30
      -  内层作用域中声明的标识符不应遮蔽外层作用域中声明的标识符
      -  `规则 5.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_03.c>`_
      -  | `DCL01-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL01-C.+Do+not+reuse+variable+names+in+subscopes>`_
         | `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_4:
    * -  31
      -  宏标识符应各不相同
      -  `规则 5.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_04.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_5:
    * -  32
      -  标识符应与宏名不同
      -  `规则 5.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_05.c>`_
      -  `DCL23-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique>`_

         .. _MisraC_Rule_5_6:
    * -  33
      -  typedef 名应是唯一的标识符
      -  `规则 5.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_06.c>`_
      -  N/A

         .. _MisraC_Rule_5_7:
    * -  34
      -  标签名（tag name）应是唯一的标识符
      -  `规则 5.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_07.c>`_
      -  N/A

         .. _MisraC_Rule_5_8:
    * -  35
      -  定义具有外部链接的对象或函数的标识符应是唯一的
      -  | `规则 5.8 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_08_1.c>`_
         | `规则 5.8 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_08_2.c>`_
      -  N/A

         .. _MisraC_Rule_5_9:
    * -  36
      -  定义具有内部链接的对象或函数的标识符应是唯一的
      -  | `规则 5.9 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_09_1.c>`_
         | `规则 5.9 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_05_09_2.c>`_
      -  N/A

         .. _MisraC_Rule_6_1:
    * -  37
      -  位域（bit-field）应仅以适当的类型声明
      -  `规则 6.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_06_01.c>`_
      -  `INT14-C <https://wiki.sei.cmu.edu/confluence/display/c/INT14-C.+Avoid+performing+bitwise+and+arithmetic+operations+on+the+same+data>`_

         .. _MisraC_Rule_6_2:
    * -  38
      -  单比特命名位域不应为有符号类型
      -  `规则 6.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_06_02.c>`_
      -  `INT14-C <https://wiki.sei.cmu.edu/confluence/display/c/INT14-C.+Avoid+performing+bitwise+and+arithmetic+operations+on+the+same+data>`_

         .. _MisraC_Rule_7_1:
    * -  39
      -  不应使用八进制常量
      -  `规则 7.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_01.c>`_
      -  `DCL18-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL18-C.+Do+not+begin+integer+constants+with+0+when+specifying+a+decimal+value>`_

         .. _MisraC_Rule_7_2:
    * -  40
      -  所有以无符号类型表示的整数常量都应添加 u 或 U 后缀
      -  `规则 7.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_02.c>`_
      -  N/A

         .. _MisraC_Rule_7_3:
    * -  41
      -  字面量后缀中不应使用小写字母 l
      -  `规则 7.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_03.c>`_
      -  `DCL16-C <https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152241>`_

         .. _MisraC_Rule_7_4:
    * -  42
      -  除非对象类型是指向 const 限定 char 的指针，否则不应将字符串字面量赋值给对象
      -  `规则 7.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_07_04.c>`_
      -  N/A

         .. _MisraC_Rule_8_1:
    * -  43
      -  应显式指定类型
      -  `规则 8.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_01.c>`_
      -  `DCL31-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL31-C.+Declare+identifiers+before+using+them>`_

         .. _MisraC_Rule_8_2:
    * -  44
      -  函数类型应以带命名参数的原型形式出现
      -  `规则 8.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_02.c>`_
      -  | `DCL07-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL07-C.+Include+the+appropriate+type+information+in+function+declarators>`_
         | `DCL20-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL20-C.+Explicitly+specify+void+when+a+function+accepts+no+arguments>`_
         | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `EXP37-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments>`_

         .. _MisraC_Rule_8_3:
    * -  45
      -  对象或函数的所有声明应使用相同的名称和类型限定符
      -  `规则 8.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_03.c>`_
      -  N/A

         .. _MisraC_Rule_8_4:
    * -  46
      -  定义具有外部链接的对象或函数时，应可见一个兼容的声明
      -  `规则 8.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_04.c>`_
      -  | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `DCL40-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL40-C.+Do+not+create+incompatible+declarations+of+the+same+function+or+object>`_

         .. _MisraC_Rule_8_5:
    * -  47
      -  外部对象或函数应恰好在一个文件中声明一次
      -  | `规则 8.5 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_05_1.c>`_
         | `规则 8.5 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_05_2.c>`_
      -  N/A

         .. _MisraC_Rule_8_6:
    * -  48
      -  具有外部链接的标识符应恰好有一个外部定义
      -  | `规则 8.6 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_06_1.c>`_
         | `规则 8.6 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_06_2.c>`_
      -  N/A

         .. _MisraC_Rule_8_8:
    * -  49
      -  具有内部链接的对象和函数的所有声明应使用 static 存储类说明符
      -  `规则 8.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_08.c>`_
      -  | `DCL15-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL15-C.+Declare+file-scope+objects+or+functions+that+do+not+need+external+linkage+as+static>`_
         | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_

         .. _MisraC_Rule_8_9:
    * -  50
      -  如果对象的标识符仅出现在单个函数中，则该对象应在块作用域中定义
      -  `规则 8.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_09.c>`_
      -  `DCL19-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL19-C.+Minimize+the+scope+of+variables+and+functions>`_

         .. _MisraC_Rule_8_10:
    * -  51
      -  内联函数应以 static 存储类声明
      -  `规则 8.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_10.c>`_
      -  N/A

         .. _MisraC_Rule_8_12:
    * -  52
      -  在枚举器列表中，隐式指定的枚举常量的值应是唯一的
      -  `规则 8.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_12.c>`_
      -  `INT09-C <https://wiki.sei.cmu.edu/confluence/display/c/INT09-C.+Ensure+enumeration+constants+map+to+unique+values>`_

         .. _MisraC_Rule_8_14:
    * -  53
      -  不应使用 restrict 类型限定符
      -  `规则 8.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_08_14.c>`_
      -  `EXP43-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP43-C.+Avoid+undefined+behavior+when+using+restrict-qualified+pointers>`_

         .. _MisraC_Rule_9_1:
    * -  54
      -  在自动存储期的对象被设置之前，不应读取其值
      -  `规则 9.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_01.c>`_
      -  N/A

         .. _MisraC_Rule_9_2:
    * -  55
      -  聚合或联合体（union）的初始化器应被花括号括起
      -  `规则 9.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_02.c>`_
      -  N/A

         .. _MisraC_Rule_9_3:
    * -  56
      -  数组不应被部分初始化
      -  `规则 9.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_03.c>`_
      -  N/A

         .. _MisraC_Rule_9_4:
    * -  57
      -  对象的元素不应被初始化多次
      -  `规则 9.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_04.c>`_
      -  N/A

         .. _MisraC_Rule_9_5:
    * -  58
      -  使用指定初始化器初始化数组对象时，应显式指定数组的大小
      -  `规则 9.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_09_05.c>`_
      -  `ARR02-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR02-C.+Explicitly+specify+array+bounds%2C+even+if+implicitly+defined+by+an+initializer>`_

         .. _MisraC_Rule_10_1:
    * -  59
      -  操作数不应具有不适当的本质类型
      -  `规则 10.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_01.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT12-C <https://wiki.sei.cmu.edu/confluence/display/c/INT12-C.+Do+not+make+assumptions+about+the+type+of+a+plain+int+bit-field+when+used+in+an+expression>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_2:
    * -  60
      -  本质为字符类型的表达式不应被不当地用于加法和减法运算
      -  `规则 10.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_02.c>`_
      -  | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_3:
    * -  61
      -  表达式的值不应被赋值给本质类型更窄或本质类型类别不同的对象
      -  `规则 10.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_03.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_4:
    * -  62
      -  执行通常算术转换的运算符的两个操作数应具有相同的本质类型类别
      -  `规则 10.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_04.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT07-C <https://wiki.sei.cmu.edu/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_
         | `STR04-C <https://wiki.sei.cmu.edu/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set>`_
         | `STR34-C <https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes>`_

         .. _MisraC_Rule_10_5:
    * -  63
      -  表达式的值不应被转换为不适当的本质类型
      -  `规则 10.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_05.c>`_
      -  | `EXP14-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP14-C.+Beware+of+integer+promotion+when+performing+bitwise+operations+on+integer+types+smaller+than+int>`_
         | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_

         .. _MisraC_Rule_10_6:
    * -  64
      -  复合表达式的值不应被赋值给本质类型更宽的对象
      -  `规则 10.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_06.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_

         .. _MisraC_Rule_10_7:
    * -  65
      -  如果复合表达式被用作执行通常算术转换的运算符的一个操作数，则另一个操作数的本质类型不应更宽
      -  `规则 10.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_07.c>`_
      -  | `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_
         | `INT31-C <https://wiki.sei.cmu.edu/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data>`_

         .. _MisraC_Rule_10_8:
    * -  66
      -  复合表达式的值不应被转换为不同的本质类型类别或更宽的本质类型
      -  `规则 10.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_10_08.c>`_
      -  `INT02-C <https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules>`_

         .. _MisraC_Rule_11_2:
    * -  67
      -  不应在不完整类型的指针与其他任何类型之间进行转换
      -  `规则 11.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_02.c>`_
      -  `EXP36-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types>`_

         .. _MisraC_Rule_11_6:
    * -  68
      -  不应在 void 指针与算术类型之间进行转换
      -  `规则 11.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_06.c>`_
      -  N/A

         .. _MisraC_Rule_11_7:
    * -  69
      -  不应在对象指针与非整数算术类型之间进行转换
      -  `规则 11.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_07.c>`_
      -  `EXP36-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types>`_

         .. _MisraC_Rule_11_8:
    * -  70
      -  转换不应从指针所指向的类型中去除任何 const 或 volatile 限定
      -  `规则 11.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_08.c>`_
      -  | `EXP05-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP05-C.+Do+not+cast+away+a+const+qualification>`_
         | `EXP32-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP32-C.+Do+not+access+a+volatile+object+through+a+nonvolatile+reference>`_

         .. _MisraC_Rule_11_9:
    * -  71
      -  宏 NULL 应是唯一允许的整数空指针常量形式
      -  `规则 11.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_11_09.c>`_
      -  N/A

         .. _MisraC_Rule_12_1:
    * -  72
      -  表达式中运算符的优先级应被显式化
      -  `规则 12.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_01.c>`_
      -  `EXP00-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP00-C.+Use+parentheses+for+precedence+of+operation>`_

         .. _MisraC_Rule_12_2:
    * -  73
      -  移位运算符的右操作数应位于 0 到左操作数本质类型位宽减 1 的范围内
      -  `规则 12.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_02.c>`_
      -  N/A

         .. _MisraC_Rule_12_4:
    * -  74
      -  常量表达式的求值不应导致无符号整数回绕
      -  `规则 12.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_04.c>`_
      -  N/A

         .. _MisraC_Rule_12_5:
    * -  75
      -  sizeof 运算符的操作数不应是声明为“类型数组”的函数参数
      -  `规则 12.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_12_05.c>`_
      -  N/A

         .. _MisraC_Rule_13_1:
    * -  76
      -  初始化器列表不应包含持久的副作用
      -  | `规则 13.1 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_01_1.c>`_
         | `规则 13.1 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_01_2.c>`_
      -  N/A

         .. _MisraC_Rule_13_2:
    * -  77
      -  表达式的值及其持久的副作用在所有允许的求值顺序下应相同
      -  `规则 13.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_02.c>`_
      -  `EXP30-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP30-C.+Do+not+depend+on+the+order+of+evaluation+for+side+effects>`_

         .. _MisraC_Rule_13_3:
    * -  78
      -  包含自增（++）或自减（--）运算符的完整表达式不应有其他潜在副作用，除了由自增或自减运算符引起的副作用
      -  `规则 13.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_03.c>`_
      -  N/A

         .. _MisraC_Rule_13_4:
    * -  79
      -  不应使用赋值运算符的结果
      -  `规则 13.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_04.c>`_
      -  N/A

         .. _MisraC_Rule_13_5:
    * -  80
      -  逻辑 && 或 || 运算符的右操作数不应包含持久的副作用
      -  | `规则 13.5 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_05_1.c>`_
         | `规则 13.5 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_05_2.c>`_
      -  `EXP10-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP10-C.+Do+not+depend+on+the+order+of+evaluation+of+subexpressions+or+the+order+in+which+side+effects+take+place>`_

         .. _MisraC_Rule_13_6:
    * -  81
      -  sizeof 运算符的操作数不应包含任何具有潜在副作用的表达式
      -  `规则 13.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_13_06.c>`_
      -  N/A

         .. _MisraC_Rule_14_1:
    * -  82
      -  循环计数器不应具有本质浮点类型
      -  `规则 14.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_01.c>`_
      -  `FLP30-C <https://wiki.sei.cmu.edu/confluence/display/c/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters>`_

         .. _MisraC_Rule_14_2:
    * -  83
      -  for 循环应是格式良好的
      -  `规则 14.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_02.c>`_
      -  N/A

         .. _MisraC_Rule_14_3:
    * -  84
      -  控制表达式不应是不变的
      -  `规则 14.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_03.c>`_
      -  N/A

         .. _MisraC_Rule_14_4:
    * -  85
      -  if 语句的控制表达式和迭代语句的控制表达式应具有本质布尔类型
      -  `规则 14.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_14_04.c>`_
      -  N/A

         .. _MisraC_Rule_15_2:
    * -  86
      -  goto 语句应跳转到同一函数中更晚声明的标签
      -  `规则 15.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_02.c>`_
      -  N/A

         .. _MisraC_Rule_15_3:
    * -  87
      -  goto 语句引用的标签应声明在同一块中，或声明在包围 goto 语句的任何块中
      -  `规则 15.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_03.c>`_
      -  N/A

         .. _MisraC_Rule_15_6:
    * -  88
      -  迭代语句或选择语句的语句体应是复合语句
      -  `规则 15.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_06.c>`_
      -  `EXP19-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP19-C.+Use+braces+for+the+body+of+an+if%2C+for%2C+or+while+statement>`_

         .. _MisraC_Rule_15_7:
    * -  89
      -  所有 if else if 结构应以 else 语句结尾
      -  `规则 15.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_15_07.c>`_
      -  `MSC01-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC01-C.+Strive+for+logical+completeness>`_

         .. _MisraC_Rule_16_1:
    * -  90
      -  所有 switch 语句应是格式良好的
      -  `规则 16.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_01.c>`_
      -  `DCL41-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL41-C.+Do+not+declare+variables+inside+a+switch+statement+before+the+first+case+label>`_

         .. _MisraC_Rule_16_2:
    * -  91
      -  仅当最紧密包围的复合语句是 switch 语句的语句体时，才应使用 switch 标签
      -  `规则 16.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_02.c>`_
      -  `MSC20-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC20-C.+Do+not+use+a+switch+statement+to+transfer+control+into+a+complex+block>`_

         .. _MisraC_Rule_16_3:
    * -  92
      -  无条件 break 语句应终止每个 switch 子句
      -  `规则 16.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_03.c>`_
      -  N/A

         .. _MisraC_Rule_16_4:
    * -  93
      -  每个 switch 语句应有一个 default 标签
      -  `规则 16.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_04.c>`_
      -  N/A

         .. _MisraC_Rule_16_5:
    * -  94
      -  default 标签应作为 switch 语句的第一个或最后一个 switch 标签出现
      -  `规则 16.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_05.c>`_
      -  N/A

         .. _MisraC_Rule_16_6:
    * -  95
      -  每个 switch 语句应至少有两个 switch 子句
      -  `规则 16.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_06.c>`_
      -  N/A

         .. _MisraC_Rule_16_7:
    * -  96
      -  switch 表达式不应具有本质布尔类型
      -  `规则 16.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_16_07.c>`_
      -  N/A

         .. _MisraC_Rule_17_1:
    * -  97
      -  不应使用 <stdarg.h> 的功能
      -  `规则 17.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_01.c>`_
      -  | `DCL10-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL10-C.+Maintain+the+contract+between+the+writer+and+caller+of+variadic+functions>`_
         | `DCL11-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL11-C.+Understand+the+type+issues+associated+with+variadic+functions>`_
         | `ERR00-C <https://wiki.sei.cmu.edu/confluence/display/c/ERR00-C.+Adopt+and+implement+a+consistent+and+comprehensive+error-handling+policy>`_

         .. _MisraC_Rule_17_2:
    * -  98
      -  函数不应直接或间接调用自身
      -  `规则 17.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_02.c>`_
      -  `MEM05-C <https://wiki.sei.cmu.edu/confluence/display/c/MEM05-C.+Avoid+large+stack+allocations>`_

         .. _MisraC_Rule_17_3:
    * -  99
      -  函数不应被隐式声明
      -  `规则 17.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_03.c>`_
      -  | `DCL36-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications>`_
         | `EXP37-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments>`_

         .. _MisraC_Rule_17_4:
    * -  100
      -  具有非 void 返回类型的函数的所有退出路径应具有带表达式的显式 return 语句
      -  `规则 17.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_04.c>`_
      -  N/A

         .. _MisraC_Rule_17_5:
    * -  101
      -  对应于声明为数组类型的参数的函数实参应具有适当数量的元素
      -  `规则 17.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_05.c>`_
      -  N/A

         .. _MisraC_Rule_17_6:
    * -  102
      -  数组参数的声明中不应在 [ ] 之间包含 static 关键字
      -  `规则 17.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_06.c>`_
      -  N/A

         .. _MisraC_Rule_17_7:
    * -  103
      -  具有非 void 返回类型的函数返回的值应被使用
      -  `规则 17.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_17_07.c>`_
      -  N/A

         .. _MisraC_Rule_18_1:
    * -  104
      -  对指针操作数执行算术运算所得到的指针应指向与该指针操作数相同的数组中的元素
      -  `规则 18.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_01.c>`_
      -  | `ARR30-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts>`_
         | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_2:
    * -  105
      -  指针之间的减法运算应仅应用于指向同一数组中元素的指针
      -  `规则 18.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_02.c>`_
      -  | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_3:
    * -  106
      -  关系运算符 >、>=、< 和 <= 不应应用于指针类型的对象，除非它们指向同一对象
      -  `规则 18.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_03.c>`_
      -  | `ARR39-C <https://wiki.sei.cmu.edu/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer>`_
         | `EXP08-C <https://wiki.sei.cmu.edu/confluence/display/c/EXP08-C.+Ensure+pointer+arithmetic+is+used+correctly>`_

         .. _MisraC_Rule_18_5:
    * -  107
      -  声明中不应包含超过两层的指针嵌套
      -  `规则 18.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_05.c>`_
      -  N/A

         .. _MisraC_Rule_18_6:
    * -  108
      -  不应将具有自动存储期的对象的地址复制到在第一个对象停止存在后仍持续存在的另一个对象中
      -  | `规则 18.6 示例 1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_06_1.c>`_
         | `规则 18.6 示例 2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_06_2.c>`_
      -  | `DCL30-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL30-C.+Declare+objects+with+appropriate+storage+durations>`_
         | `MEM30-C <https://wiki.sei.cmu.edu/confluence/display/c/MEM30-C.+Do+not+access+freed+memory>`_

         .. _MisraC_Rule_18_8:
    * -  109
      -  不应使用变长数组（VLA）类型
      -  `规则 18.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_18_08.c>`_
      -  N/A

         .. _MisraC_Rule_19_1:
    * -  110
      -  对象不应被赋值或复制到与之重叠的对象
      -  `规则 19.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_19_01.c>`_
      -  N/A

         .. _MisraC_Rule_20_2:
    * -  111
      -  头文件名中不应出现 ', 或 \ 字符以及 /* 或 // 字符序列
      -  `规则 20.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_02.c>`_
      -  N/A

         .. _MisraC_Rule_20_3:
    * -  112
      -  #include 指令后应跟随 <filename> 或 "filename" 序列
      -  `规则 20.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_03.c>`_
      -  N/A

         .. _MisraC_Rule_20_4:
    * -  113
      -  不应定义与关键字同名的宏
      -  `规则 20.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_04.c>`_
      -  N/A

         .. _MisraC_Rule_20_7:
    * -  114
      -  宏参数展开所得到的表达式应被括号括起
      -  `规则 20.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_07.c>`_
      -  `PRE01-C <https://wiki.sei.cmu.edu/confluence/display/c/PRE01-C.+Use+parentheses+within+macros+around+parameter+names>`_

         .. _MisraC_Rule_20_8:
    * -  115
      -  #if 或 #elif 预处理指令的控制表达式应求值为 0 或 1
      -  `规则 20.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_08.c>`_
      -  N/A

         .. _MisraC_Rule_20_9:
    * -  116
      -  #if 或 #elif 预处理指令控制表达式中使用的所有标识符应在求值前被 #define
      -  `规则 20.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_09.c>`_
      -  N/A

         .. _MisraC_Rule_20_11:
    * -  117
      -  紧跟在 # 运算符后面的宏参数不应紧接着被 ## 运算符跟随
      -  `规则 20.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_11.c>`_
      -  N/A

         .. _MisraC_Rule_20_12:
    * -  118
      -  作为 # 或 ## 运算符操作数、且本身还要接受进一步宏替换的宏参数，应仅作为这些运算符的操作数使用
      -  `规则 20.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_12.c>`_
      -  N/A

         .. _MisraC_Rule_20_13:
    * -  119
      -  第一个 token 为 # 的行应是有效的预处理指令
      -  `规则 20.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_13.c>`_
      -  N/A

         .. _MisraC_Rule_20_14:
    * -  120
      -  所有 #else、#elif 和 #endif 预处理指令应位于其相关的 #if、#ifdef 或 #ifndef 指令所在的同一文件中
      -  `规则 20.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_20_14.c>`_
      -  N/A

         .. _MisraC_Rule_21_1:
    * -  121
      -  不应在保留标识符或保留宏名上使用 #define 和 #undef
      -  `规则 21.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_01.c>`_
      -  `DCL37-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL37-C.+Do+not+declare+or+define+a+reserved+identifier>`_

         .. _MisraC_Rule_21_2:
    * -  122
      -  不应声明保留标识符或保留宏名
      -  `规则 21.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_02.c>`_
      -  `DCL37-C <https://wiki.sei.cmu.edu/confluence/display/c/DCL37-C.+Do+not+declare+or+define+a+reserved+identifier>`_

         .. _MisraC_Rule_21_3:
    * -  123
      -  不应使用 <stdlib.h> 的内存分配和释放函数
      -  `规则 21.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_03.c>`_
      -  | `API03-C <https://wiki.sei.cmu.edu/confluence/display/c/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions>`_
         | `API04-C <https://wiki.sei.cmu.edu/confluence/display/c/API04-C.+Provide+a+consistent+and+usable+error-checking+mechanism>`_
         | `MSC24-C <https://wiki.sei.cmu.edu/confluence/display/c/MSC24-C.+Do+not+use+deprecated+or+obsolescent+functions>`_

         .. _MisraC_Rule_21_4:
    * -  124
      -  不应使用标准头文件 <setjmp.h>
      -  `规则 21.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_04.c>`_
      -  N/A

         .. _MisraC_Rule_21_6:
    * -  125
      -  不应使用标准库输入/输出函数
      -  `规则 21.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_06.c>`_
      -  N/A

         .. _MisraC_Rule_21_7:
    * -  126
      -  不应使用 <stdlib.h> 的 atof、atoi、atol 和 atoll 函数
      -  `规则 21.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_07.c>`_
      -  N/A

         .. _MisraC_Rule_21_9:
    * -  127
      -  不应使用 <stdlib.h> 的库函数 bsearch 和 qsort
      -  `规则 21.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_09.c>`_
      -  N/A

         .. _MisraC_Rule_21_11:
    * -  128
      -  不应使用标准头文件 <tgmath.h>
      -  `规则 21.11 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_11.c>`_
      -  N/A

         .. _MisraC_Rule_21_12:
    * -  129
      -  不应使用 <fenv.h> 的异常处理功能
      -  `规则 21.12 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_12.c>`_
      -  N/A

         .. _MisraC_Rule_21_13:
    * -  130
      -  传递给 <ctype.h> 中函数的任何值应可表示为 unsigned char 或为值 EOF
      -  `规则 21.13 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_13.c>`_
      -  N/A

         .. _MisraC_Rule_21_14:
    * -  131
      -  不应使用标准库函数 memcmp 来比较以 null 结尾的字符串
      -  `规则 21.14 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_14.c>`_
      -  N/A

         .. _MisraC_Rule_21_15:
    * -  132
      -  标准库函数 memcpy、memmove 和 memcmp 的指针实参应指向兼容类型的限定版本或非限定版本
      -  `规则 21.15 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_15.c>`_
      -  N/A

         .. _MisraC_Rule_21_16:
    * -  133
      -  标准库函数 memcmp 的指针实参应指向指针类型、本质有符号类型、本质无符号类型、本质布尔类型或本质枚举类型
      -  `规则 21.16 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_16.c>`_
      -  N/A

         .. _MisraC_Rule_21_17:
    * -  134
      -  使用 <string.h> 的字符串处理函数不应导致访问超出其指针参数所引用对象的边界
      -  `规则 21.17 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_17.c>`_
      -  N/A

         .. _MisraC_Rule_21_18:
    * -  135
      -  传递给 <string.h> 中任何函数的 size_t 实参应具有适当的值
      -  `规则 21.18 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_18.c>`_
      -  N/A

         .. _MisraC_Rule_21_19:
    * -  136
      -  标准库函数 localeconv、getenv、setlocale 或 strerror 返回的指针应仅被当作指向 const 限定类型的指针使用
      -  `规则 21.19 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_19.c>`_
      -  N/A

         .. _MisraC_Rule_21_20:
    * -  137
      -  标准库函数 asctime、ctime、gmtime、localtime、localeconv、getenv、setlocale 或 strerror 返回的指针，在后续再次调用同一函数之后不应被使用
      -  `规则 21.20 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_21_20.c>`_
      -  N/A

         .. _MisraC_Rule_22_1:
    * -  138
      -  通过标准库函数动态获取的所有资源应被显式释放
      -  `规则 22.1 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_01.c>`_
      -  N/A

         .. _MisraC_Rule_22_2:
    * -  139
      -  内存块仅当它是通过标准库函数分配的才应被释放
      -  `规则 22.2 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_02.c>`_
      -  N/A

         .. _MisraC_Rule_22_3:
    * -  140
      -  同一文件不应同时在不同的流上以读和写方式打开
      -  `规则 22.3 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_03.c>`_
      -  N/A

         .. _MisraC_Rule_22_4:
    * -  141
      -  不应尝试向以只读方式打开的流写入
      -  `规则 22.4 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_04.c>`_
      -  N/A

         .. _MisraC_Rule_22_5:
    * -  142
      -  不应解引用指向 FILE 对象的指针
      -  `规则 22.5 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_05.c>`_
      -  N/A

         .. _MisraC_Rule_22_6:
    * -  143
      -  关联的流被关闭之后，不应再使用指向 FILE 的指针的值
      -  `规则 22.6 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_06.c>`_
      -  N/A

         .. _MisraC_Rule_22_7:
    * -  144
      -  宏 EOF 应仅与任何能够返回 EOF 的标准库函数未修改的返回值进行比较
      -  `规则 22.7 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_07.c>`_
      -  N/A

         .. _MisraC_Rule_22_8:
    * -  145
      -  在调用会设置 errno 的函数之前，应将 errno 的值设为零
      -  `规则 22.8 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_08.c>`_
      -  N/A

         .. _MisraC_Rule_22_9:
    * -  146
      -  在调用会设置 errno 的函数之后，应将 errno 的值与零进行比较
      -  `规则 22.9 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_09.c>`_
      -  N/A

         .. _MisraC_Rule_22_10:
    * -  147
      -  仅当最后调用的函数是会设置 errno 的函数时，才应测试 errno 的值
      -  `规则 22.10 <https://gitlab.com/MISRA/MISRA-C/MISRA-C-2012/Example-Suite/-/blob/master/R_22_10.c>`_
      -  N/A

附加规则
****************

规则 A.1：条件编译
=================================
严重级别
  必需

描述
  不要在头文件中条件编译函数声明。不要在头文件中条件编译结构体声明。你可以在结构体定义中条件性地排除字段，以避免在其支持的特性未启用时浪费内存。

依据
  基于编译期选项从头文件中排除声明可能会阻止其文档的生成。其缺失还会阻止在代码路径应根据所选选项改变时使用 ``if (IS_ENABLED(CONFIG_FOO)) {}`` 作为预处理器条件编译的替代方案。

.. _coding_guideline_inclusive_language:

规则 A.2：包容性语言
============================
严重级别
  必需

描述
  不要引入下列冒犯性术语的新用法。本规则适用于但不限于源代码、注释、文档和分支名称。替换术语可能因领域或子系统而异，但应尽可能遵循更新后的行业标准。

  对于维护现有实现，或为 Zephyr 项目外部治理的行业标准规范添加新实现，允许例外。

  建议一旦更新后的行业标准规范可用、或治理机构公开宣布新术语，或在不适用任何规范时立即更改现有用法。

  .. list-table::
     :header-rows: 1

     * - 冒犯性术语
       - 建议的替换

     * - ``{master,leader} / slave``
       - - ``{primary,main} / {secondary,replica}``
         - ``{initiator,requester} / {target,responder}``
         - ``{controller,host} / {device,worker,proxy,target}``
         - ``director / performer``
         - ``central / peripheral``

     * - ``blacklist / whitelist``
       - * ``denylist / allowlist``
         * ``blocklist / allowlist``
         * ``rejectlist / acceptlist``

     * - ``grandfather policy``
       - * ``legacy``

     * - ``sanity``
       - * ``coherence``
         * ``confidence``

依据
  冒犯性术语不会营造包容性的社区环境，因此违反了 Zephyr 项目的 `Code of Conduct`_。本编码规则受 `Linux`_ 中类似规则的启发。

  .. _Code of Conduct: https://github.com/zephyrproject-rtos/zephyr/blob/main/CODE_OF_CONDUCT.md
  .. _Linux: https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=49decddd39e5f6132ccd7d9fdc3d7c470b0061bb

状态
  相关的 GitHub Issues 和 Pull Requests 带有 `Inclusive Language Label`_ 标签。

  .. list-table::
     :header-rows: 1

     * - 领域
       - 选定的替换
       - 状态

     * - :ref:`Bluetooth <bluetooth_api>`
       - 参见 `Bluetooth Appropriate Language Mapping Tables`_
       -

     * - CAN
       - 这篇 `CAN in Automation Inclusive Language news post`_ 有一般性建议的列表。要用于规范文档更新的术语，参见 `CAN in Automation Inclusive Language`_。
       -

     * - eSPI
       - * ``master / slave`` => ``controller / target``
       - 新术语参见 `eSPI Specification`_

     * - gPTP
       - * ``master / slave`` => TBD
       -

     * - :ref:`i2c_api`
       - * ``master / slave`` => ``controller / target``
       - 新术语参见 `I2C Specification`_。

     * - :ref:`i2s_api`
       - * ``master / slave`` => ``controller / target``
       - 新术语参见 `I2S Specification`_。Zephyr I2S API 已在 Zephyr 4.4 迁移到这些术语；原宏名作为弃用别名保留，并将在 Zephyr 5.0 移除。

     * - SMP/AMP
       - * ``master / slave`` => TBD
       -

     * - :ref:`spi_api`
       - * ``master / slave`` => ``controller / peripheral``
         * ``MOSI / MISO / SS`` => ``SDO / SDI / CS``
       - 开源硬件协会（Open Source Hardware Association）选定了这些替换术语。参见 `OSHWA Resolution to Redefine SPI Signal Names`_。Zephyr SPI API 和代码树已在 v4.5 迁移到这些术语；原名称作为兼容性别名保留，自 v4.5 起弃用，并计划在 v5.0 移除。

     * - :ref:`twister_script`
       - * ``platform_whitelist`` => ``platform_allow``
         * ``sanitycheck`` => ``twister``
       -

  .. _Inclusive Language Label: https://github.com/zephyrproject-rtos/zephyr/issues?q=label%3A%22Inclusive+Language%22
  .. _I2C Specification: https://www.nxp.com/docs/en/user-guide/UM10204.pdf
  .. _I2S Specification: https://www.nxp.com/docs/en/user-manual/UM11732.pdf
  .. _Bluetooth Appropriate Language Mapping Tables: https://specificationrefs.bluetooth.com/language-mapping/Appropriate_Language_Mapping_Table.pdf
  .. _OSHWA Resolution to Redefine SPI Signal Names: https://oshwa.org/resources/a-resolution-to-redefine-spi-signal-names/
  .. _CAN in Automation Inclusive Language news post: https://www.can-cia.org/news/archive/view/?tx_news_pi1%5Bnews%5D=699&tx_news_pi1%5Bday%5D=6&tx_news_pi1%5Bmonth%5D=12&tx_news_pi1%5Byear%5D=2020&cHash=784e79eb438141179386cf7c29ed9438
  .. _CAN in Automation Inclusive Language: https://can-newsletter.org/canopen/categories/
  .. _eSPI Specification: https://downloadmirror.intel.com/27055/327432%20espi_base_specification%20R1-5.pdf


.. _coding_guideline_libc_usage_restrictions_in_zephyr_kernel:

规则 A.3：宏名冲突
===============================
严重级别
  必需

描述
  名为 ``MIN``、``MAX``、``ARRAY_SIZE`` 等常用名称的宏，不得被修改或保护以避免与其他实现发生名称冲突。特别是，不得给它们加前缀以放入 Zephyr 专用命名空间、不得使用 ``#undef`` 重新定义、也不得使用 ``#ifndef`` 条件性地将其排除出编译。相反，如果与源自 :ref:`模块 <modules>` 的现有定义发生冲突，则需要修改该模块自身的代码（理想情况下在上游，或者通过 Zephyr 自己的 fork 中的更改）。

  本规则总体上适用于 Zephyr 项目，无论宏引入的时间或其当前在代码树中的名称如何。如果宏名在多个其他知名开源项目中常用，则 Zephyr 中的实现应使用该名称。虽然“常用”的含义带有主观且不可测量的成分，但最终目标是为用户提供熟悉的宏。

  最后，本规则同样适用于模块间的名称冲突：在这种情况下，两个模块在被纳入之前都应被修改，以使用发生冲突的宏名的模块特定版本。

依据
  Zephyr 是一个附带以模块形式提供额外功能和依赖项的 RTOS。这些模块通常是独立的项目，可能使用与其他模块或 Zephyr 本身冲突的宏名。由于在本文档的上下文中，Zephyr 被视为中心或主项目，它应实现这些宏的非命名空间版本。鉴于 Zephyr 对每个模块使用对应上游的 fork，因此始终可以修补每个模块中的宏实现以避免冲突。

规则 A.4：Zephyr 内核中 C 标准库使用限制
================================================================
严重级别
  必需

描述
  Zephyr 内核中使用 C 标准库函数和宏应限于 ISO/IEC 9899:2011 标准（也称为 C11）及其扩展中的以下函数和宏：

  .. csv-table:: Zephyr 内核中允许的 libc 函数和宏列表
     :header: 函数,来源
     :widths: auto

     abort(),ISO/IEC 9899:2011
     abs(),ISO/IEC 9899:2011
     aligned_alloc(),ISO/IEC 9899:2011
     assert(),ISO/IEC 9899:2011
     atoi(),ISO/IEC 9899:2011
     bsearch(),ISO/IEC 9899:2011
     calloc(),ISO/IEC 9899:2011
     exit(),ISO/IEC 9899:2011
     fprintf(),ISO/IEC 9899:2011
     fputc(),ISO/IEC 9899:2011
     fputs(),ISO/IEC 9899:2011
     free(),ISO/IEC 9899:2011
     fwrite(),ISO/IEC 9899:2011
     gmtime(),ISO/IEC 9899:2011
     isalnum(),ISO/IEC 9899:2011
     isalpha(),ISO/IEC 9899:2011
     iscntrl(),ISO/IEC 9899:2011
     isdigit(),ISO/IEC 9899:2011
     isgraph(),ISO/IEC 9899:2011
     isprint(),ISO/IEC 9899:2011
     isspace(),ISO/IEC 9899:2011
     isupper(),ISO/IEC 9899:2011
     isxdigit(),ISO/IEC 9899:2011
     labs(),ISO/IEC 9899:2011
     llabs(),ISO/IEC 9899:2011
     malloc(),ISO/IEC 9899:2011
     memchr(),ISO/IEC 9899:2011
     memcmp(),ISO/IEC 9899:2011
     memcpy(),ISO/IEC 9899:2011
     memmove(),ISO/IEC 9899:2011
     memset(),ISO/IEC 9899:2011
     perror(),ISO/IEC 9899:2011
     printf(),ISO/IEC 9899:2011
     putc(),ISO/IEC 9899:2011
     putchar(),ISO/IEC 9899:2011
     puts(),ISO/IEC 9899:2011
     qsort(),ISO/IEC 9899:2011
     rand(),ISO/IEC 9899:2011
     realloc(),ISO/IEC 9899:2011
     snprintf(),ISO/IEC 9899:2011
     sprintf(),ISO/IEC 9899:2011
     sqrt(),ISO/IEC 9899:2011
     sqrtf(),ISO/IEC 9899:2011
     srand(),ISO/IEC 9899:2011
     strcat(),ISO/IEC 9899:2011
     strchr(),ISO/IEC 9899:2011
     strcmp(),ISO/IEC 9899:2011
     strcpy(),ISO/IEC 9899:2011
     strcspn(),ISO/IEC 9899:2011
     strerror(),ISO/IEC 9899:2011
     strlen(),ISO/IEC 9899:2011
     strncat(),ISO/IEC 9899:2011
     strncmp(),ISO/IEC 9899:2011
     strncpy(),ISO/IEC 9899:2011
     `strnlen()`_,POSIX.1-2008
     strrchr(),ISO/IEC 9899:2011
     strspn(),ISO/IEC 9899:2011
     strstr(),ISO/IEC 9899:2011
     strtol(),ISO/IEC 9899:2011
     strtoll(),ISO/IEC 9899:2011
     strtoul(),ISO/IEC 9899:2011
     strtoull(),ISO/IEC 9899:2011
     time(),ISO/IEC 9899:2011
     tolower(),ISO/IEC 9899:2011
     toupper(),ISO/IEC 9899:2011
     vfprintf(),ISO/IEC 9899:2011
     vprintf(),ISO/IEC 9899:2011
     vsnprintf(),ISO/IEC 9899:2011
     vsprintf(),ISO/IEC 9899:2011

  上述列出的所有函数都必须由 :ref:`最小 libc <c_library_minimal>` 实现，以确保 Zephyr 内核能够使用最小 libc 构建。

  此外，上述列表中不属于 ISO/IEC 9899:2011 标准的任何函数都必须由 :ref:`通用 libc <c_library_common>` 实现，以确保其在多个 C 标准库中可用。

  在满足上述要求的前提下，允许给出理由后将新的 C 标准库函数引入 Zephyr 内核。

  请注意，上述函数的使用须遵循安全编码实践，不应假定其在 Zephyr 内核中的使用因列于本规则而被无条件允许。

  本上下文中的“Zephyr 内核”由以下组件组成：

  * 内核（:file:`kernel`）
  * OS 库（:file:`lib/os`）
  * 架构移植（:file:`arch`）
  * 日志子系统（:file:`subsys/logging`）

依据
  Zephyr 内核必须能够使用 :ref:`最小 libc <c_library_minimal>` 构建，这是一个有限的 C 标准库实现，是 Zephyr RTOS 的一部分并由 Zephyr 项目维护，以便对内核和核心 OS 服务进行自包含的测试和验证。

  为确保 Zephyr 内核能够使用最小 libc 构建，有必要将 Zephyr 内核中 C 标准库函数和宏的使用限制在最小 libc 中可用的函数和宏范围内。

规则 A.5：Zephyr 代码库中 C 标准库使用限制
==================================================================
严重级别
  必需

描述
  Zephyr 代码库中使用 C 标准库函数和宏应限于 ISO/IEC 9899:2011 标准（也称为 C11）中的函数，排除附录 K “边界检查接口”，除非本规则豁免。

  本上下文中的“Zephyr 代码库”指提交到 `main Zephyr repository`_ 的所有嵌入式源代码文件，但不包括由 :ref:`coding_guideline_libc_usage_restrictions_in_zephyr_kernel` 定义的 Zephyr 内核。嵌入式源代码指打算在嵌入式目标上执行的代码，因此排除了主机工具，以及 :ref:`native <boards_posix>` 测试目标专用的代码。

  以下非 ISO 9899:2011（下文称为非标准）函数和宏被本规则豁免并允许在 Zephyr 代码库中使用：

  .. csv-table:: 允许的非标准 libc 函数列表
     :header: 函数,来源
     :widths: auto

     `gmtime_r()`_,POSIX.1-2001
     `strnlen()`_,POSIX.1-2008
     `strtok_r()`_,POSIX.1-2001

  上述列出的所有非标准函数和宏都必须由 :ref:`通用 libc <c_library_common>` 实现，以确保在使用未实现这些函数的 C 标准库时这些函数可以被提供。

  在满足上述要求的前提下，允许给出理由后将通用 C 标准库中的新非标准函数添加到上述列表。但是，当存在功能等效的标准函数时，应使用标准函数。

依据
  某些 C 标准库（如 Newlib 和 Picolibc）包含由扩展 ISO C 标准（例如 POSIX、Linux）的标准和事实标准定义的额外函数和宏。

  ISO/IEC 9899:2011 标准不要求 C 编译器工具链包含对这些非标准函数的支持，因此使用这些函数可能导致携带自身 C 标准库的第三方工具链出现兼容性问题。

  .. _main Zephyr repository: https://github.com/zephyrproject-rtos/zephyr
  .. _gmtime_r(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/gmtime_r.html
  .. _strnlen(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/strlen.html
  .. _strtok_r(): https://pubs.opengroup.org/onlinepubs/9699919799/functions/strtok.html
