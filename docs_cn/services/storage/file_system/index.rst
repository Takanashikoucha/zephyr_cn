.. _file_system_api:

文件系统
############

Zephyr RTOS 的虚拟文件系统（VFS）允许应用程序在不同的挂载点（例如 ``/fatfs`` 和 ``/lfs``）挂载多个文件系统。挂载点数据结构包含实例化、挂载和操作一个文件系统所需的所有必要信息。文件系统开关（File system Switch）通过引入文件系统注册机制，将应用程序与直接访问某个文件系统的特定 API 或内部函数解耦。

在 Zephyr 中，任何文件系统实现或库都可以通过文件系统注册 API 插入或移除。每个文件系统实现必须有一个全局唯一的整数标识符；使用 :c:enumerator:`FS_TYPE_EXTERNAL_BASE` 以避免与树内标识符冲突。

.. code-block:: c

        int fs_register(int type, const struct fs_file_system_t *fs);

        int fs_unregister(int type, const struct fs_file_system_t *fs);

Zephyr RTOS 通过使用挂载点作为磁盘卷名来支持同一文件系统的多个实例，该卷名在文件系统库格式化或挂载磁盘时使用。

文件系统的声明方式如下：

.. code-block:: c

	static struct fs_mount_t mp = {
	.type = FS_FATFS,
	.mnt_point = FATFS_MNTP,
	.fs_data = &fat_fs,
	};

其中：

- ``FS_FATFS`` 是文件系统类型，例如 FATFS 或 LittleFS。
- ``FATFS_MNTP`` 是文件系统将被挂载的挂载点。
- ``fat_fs`` 是将被 fs_mount() API 使用的文件系统数据。



示例
*******

VFS 的示例主要集中在 ``samples/subsys/fs`` 中，尽管不同子系统的示例也将 VFS 使用作为重要功能提供。以下是值得关注的示例列表：

- :zephyr:code-sample:`fs` 是在 SDHC 介质上使用 FAT 文件系统的示例；
- :zephyr:code-sample:`shell-fs` 是 Shell fs 子系统的示例，使用格式化为 LittleFS 的内部 flash 分区；
- :zephyr:code-sample:`usb-mass` 是 USB 大容量存储设备的示例，根据示例配置，使用连接 RAM 或 SPI flash 的 FAT FS 驱动，或使用 flash 中的 LittleFS。

API 参考
*************

.. doxygengroup:: file_system_api
