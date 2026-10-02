加载扩展
##################

扩展构建完成且 ELF 文件可用后，即可使用 LLEXT API 将其加载到 Zephyr 应用程序中。该 API 提供将扩展加载到内存、访问其符号并调用其函数的方式。

加载扩展
==================

扩展可以使用任何 :c:struct:`llext_loader` 实现来加载，该实现拥有一组函数指针，提供读取 ELF 数据所需的必要功能。加载器还为 :c:func:`llext_load` 函数提供所需的最小上下文（内存）。目前已提供多个加载器：

 * 一个基于缓冲区的实现，缓冲区位于可寻址内存中并包含 ELF，可用 :c:struct:`llext_buf_loader` 获取。要使用这种加载器，最好使用 :c:macro:`LLEXT_TEMPORARY_BUF_LOADER`、:c:macro:`LLEXT_PERSISTENT_BUF_LOADER` 或 :c:macro:`LLEXT_WRITABLE_BUF_LOADER` 宏之一，以告知 LLEXT 相应类型的内存缓冲区。

 * 一个从文件系统文件中读取数据的实现，可用 :c:struct:`llext_fs_loader` 获取。创建加载器时必须使用 :c:macro:`LLEXT_FS_LOADER` 宏提供文件路径。

 * 一个使用半托管（semihosting）从宿主文件系统文件中读取数据的实现，可用 :c:struct:`llext_semihost_loader` 获取。创建加载器时必须使用 :c:macro:`LLEXT_SEMIHOST_LOADER` 宏提供文件路径。

扩展通过调用 :c:func:`llext_load` 函数加载，传入扩展名称和配置好的加载器。一旦成功完成，扩展即被加载到内存中，可以使用。

.. note::
   启用 :ref:`用户模式 <usermode_api>` 时，扩展不会包含在任何用户内存域中。要允许从用户模式访问，必须调用 :c:func:`llext_add_domain` 函数。

初始化和清理扩展
==========================================

扩展可能定义若干初始化函数，必须在加载之后、使用其中任何函数之前调用；这在 C++ 等提供对象构造器概念的语言中很常见。清理函数也是如此，必须在卸载扩展之前调用。

LLEXT 支持使用 :c:func:`llext_bringup` 函数调用 ELF 文件中 ``.preinit_array`` 和 ``.init_array`` 段列出的函数，使用 :c:func:`llext_teardown` 函数调用 ``.fini_array`` 段列出的函数。这些 API 与 :ref:`用户模式 <usermode_api>` 兼容，因此可以从内核上下文或用户上下文调用。

.. important::
   这些函数运行的代码完全由 ELF 文件的内容决定。如果其来源不可信，这可能带来安全影响。

如果扩展需要专用线程，可以使用 :c:func:`llext_bootstrap` 函数来减少样板代码。该函数的签名与 :c:func:`k_thread_create` API 兼容，会调用 :c:func:`llext_bringup`，然后在同一上下文中调用用户指定的函数，最后返回前调用 :c:func:`llext_teardown`。

访问代码和数据
======================

要与新加载的扩展交互，宿主应用程序必须使用 :c:func:`llext_find_sym` 函数获取导出符号的地址。返回的 ``void *`` 可以转换为相应类型并使用。

:c:func:`llext_call_fn` 提供了一个用于调用无参函数的封装。

需要直接访问新加载扩展各区域的高级用户可以参考 :c:func:`llext_get_section_info` 和其他 LLEXT 检查 API。

使用后的清理
====================

扩展不再需要时，必须调用 :c:func:`llext_unload` 函数释放扩展占用的内存。此调用完成后，之前获取的所有指向扩展中符号的指针都将失效。

故障排除
###############

该功能正在积极开发中，因此可能出现一些问题。由于链接会修改二进制代码，出错时结果难以预测。常见问题可能包括：

* :c:func:`llext_find_sym` 的结果指向无效地址；

* 扩展中定义的常量和变量没有预期的值；

* 调用扩展中定义的函数导致硬故障，或从该函数返回后主应用程序中的内存被破坏。

如果发生上述任何情况，以下提示可能有助于理解问题：

* 确保 :kconfig:option:`CONFIG_LLEXT_LOG_LEVEL` 设置为 ``DEBUG``，然后获取 :c:func:`llext_load` 调用的日志。

* 如果可能，禁用内存保护（MMU/MPU），观察是否出现不同的行为。

* 尝试将扩展简化到能复现该问题的最少代码。

* 使用调试器检查内存和寄存器，尝试理解发生了什么。更多细节参见 :ref:`调试扩展 <llext_debug>`。

如果问题仍然存在，请在 GitHub 仓库中提交 issue，并附上上述所有信息。
