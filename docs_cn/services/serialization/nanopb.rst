.. _nanopb_reference:

Nanopb
######

`Nanopb
<https://jpa.kapsi.fi/nanopb/>`_
是
Google
的
`Protocol
Buffers
<https://protobuf.dev/>`_
的
一
个
C
implementation。

Requirements
************

Nanopb
use
protocol
buffer
compiler
generate
source
和
header
files
确保
``protoc``
executable
被
installed
且
available。

.. tabs::

   .. group-tab::
      Ubuntu

      用
      ``apt``
      install
      dependency：

         .. code-block::
            shell

            sudo
            apt
            install
            protobuf-compiler

   .. group-tab::
      macOS

      用
      ``brew``
      install
      dependency：

         .. code-block::
            shell

            brew
            install
            protobuf

   .. group-tab::
      Windows

      用
      ``choco``
      install
      dependency：

         .. code-block::
            shell

            choco
            install
            protoc
