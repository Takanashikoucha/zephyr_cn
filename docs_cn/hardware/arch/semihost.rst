.. _semihost_guide:

Semihosting 指南
#################

概述
********

Semihosting 是一种机制，使运行在 ARM、RISC-V 和 Xtensa 目标上的代码能够与运行着调试器或模拟器的主机计算机进行通信，并使用主机上的输入/输出（I/O）设施。

关于可用功能的更完整文档，可参见 `ARM Github documentation`_。

RISC-V 的功能借鉴自 ARM 的定义，如 `RISC-V Github documentation`_ 中所述。

Xtensa 上的 Semihosting 实现支持 GDB File-I/O 扩展，其说明见 `GDB File-I/O Remote Protocol`_。

文件操作
***************

Semihosting 使主机计算机上的文件能够被应用程序打开、读取和修改。当需要验证代码在比模拟平台 ROM 容量更大的数据集上的行为时，这非常有用。文件路径可以是绝对路径，也可以是相对于运行进程所在目录的相对路径。

.. code-block:: c

   const char *path = "./data.bin";
   long file_len, bytes_read, fd;
   uint8_t buffer[16];

   /* Open the data file for reading */
   fd = semihost_open(path, SEMIHOST_OPEN_RB);
   if (fd < 0) {
      return -ENOENT;
   }
   /* Read all data from the file */
   file_len = semihost_flen(fd);
   while(file_len > 0) {
      bytes_read = semihost_read(fd, buffer, MIN(file_len, sizeof(buffer)));
      if (bytes_read < 0) {
         break;
      }
      /* Process read data */
      do_data_processing(buffer, bytes_read);
      /* Update remaining length */
      file_len -= bytes_read;
   }
   /* Close the file */
   semihost_close(fd);

附加功能
************************

通过 :c:func:`semihost_exec` 直接执行 :c:enum:`semihost_instr` 中定义的某条指令，可以获得附加功能。关于所需参数和返回码的完整文档，请参见 `ARM Github documentation`_。

API 参考
*************

.. doxygengroup:: semihost

.. _ARM Github documentation: https://github.com/ARM-software/abi-aa/blob/main/semihosting/semihosting.rst
.. _RISC-V Github documentation: https://github.com/riscv-non-isa/riscv-semihosting/blob/main/riscv-semihosting.adoc
.. _GDB File-I/O Remote Protocol: https://sourceware.org/gdb/current/onlinedocs/gdb.html/File_002dI_002fO-Remote-Protocol-Extension.html
