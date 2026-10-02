.. _posix_details:

实现细节
######################

在许多方面，Zephyr 提供的支持与任何 POSIX 操作系统类似：
API 绑定以 C 编程语言提供，在配置后，POSIX 头文件可在标准包含路径中使用。

与其他多用途 POSIX 操作系统不同：

- Zephyr 不是"一个 POSIX 操作系统"。Zephyr 内核并非围绕 POSIX 标准设计，
  POSIX 支持是一个可选（opt-in）特性
- Zephyr 应用不会单独链接，也不作为子进程执行
- Zephyr、库和应用代码被一起编译和链接，运行方式类似于单进程应用，
  运行在单个（可能是虚拟的）地址空间中
- Zephyr 不提供 POSIX shell、编译器、实用工具，也不是自托管的。

.. note::
   与 Linux 内核或 FreeBSD 不同，Zephyr 不为每个支持的架构维护系统调用编号的静态表，
   而是在构建时动态生成系统调用。更多信息参见 :ref:`System Calls <syscalls>`。

设计
======

作为库，Zephyr 的 POSIX API 实现力求成为应用、中间件与 Zephyr 内核之间的一层薄抽象层。

一些通用的设计考虑：

- POSIX 接口和实现应当是 Zephyr POSIX 库的一部分，而不是放在其他地方，
  除非该特性同时被 POSIX API 实现和某个其他特性所必需。一个实现应当保留在
  POSIX 实现中的例子是 ``getopt()``。实现应当属于独立库的例子是多线程和网络。

- 当 POSIX API 和另一个 Zephyr 子系统都依赖某个特性时，该特性的实现应作为一个独立的
  Zephyr 库，可被 POSIX API 和另一个库或子系统使用。这会降低代码中出现依赖循环的可能性。
  在可行的情况下，该规则应扩展到包含宏。在下面的例子中，``libposix`` 依赖 ``libzfoo``
  来实现 Zephyr 中某个功能"foo"。如果 ``libzfoo`` 也依赖 ``libposix``，
  那么就会形成依赖循环。可以通过相互依赖 ``libcommon`` 来消除该循环。

.. graphviz::
   :caption: POSIX 与另一个 Zephyr 库之间的依赖循环

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];

       libposix -> libzfoo;
       libzfoo -> libposix;
   }

.. graphviz::
   :caption: POSIX 与其他 Zephyr 库之间的相互依赖

   digraph {
       node [shape=rect, style=rounded];
       rankdir=LR;

       libposix [fillcolor="#d5e8d4"];
       libzfoo [fillcolor="#dae8fc"];
       libcommon [fillcolor="#f8cecc"];

       libposix -> libzfoo;
       libposix -> libcommon;
       libzfoo -> libcommon;
   }

- POSIX API 调用应作为常规可调用的 C 函数提供；如果实现的一部分需要
  Zephyr :ref:`System Call <syscalls>`，那么该系统调用的声明和实现应隐藏在 POSIX API 之后。
