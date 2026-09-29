.. _external_module_libmpix:

libmpix
#######

简介
****

`libmpix`_ 项目提供一个用于在微控制器上处理图像数据的库。
它支持像素格式转换、debayer、模糊、锐化、色彩校正、缩放等。

它将多个操作串联为流水线，消除中间缓冲区。
这使得更大的图像分辨率能在受限系统中运行而不牺牲性能。

特性
****

* 简单的零拷贝流水线引擎，运行时开销低
* 降低内存开销（例如仅用 5 kB RAM 处理 1 MB 数据）
* POSIX 支持（Linux/BSD/MacOS）和 Zephyr 支持

在 Zephyr 中使用
****************

要将 libmpix 作为 Zephyr 模块引入，可以将其作为 West 项目添加到
:file:`west.yaml` 文件，或通过添加子 manifest（例如
``zephyr/submanifests/libmpix.yaml``）文件引入，内容如下，然后运行
:command:`west update`：

.. code-block:: yaml

   manifest:
     projects:
       - name: libmpix
         url: https://github.com/libmpix/libmpix.git
         revision: main
         path: modules/lib/libmpix

API 详情请参见 ``libmpix`` 头文件。简要示例如下。

.. code-block:: c

   #include <mpix/image.h>

   struct mpix_image img;

   mpix_image_from_buf(&img, buf_in, sizeof(buf_in), MPIX_FORMAT_RGB24);
   mpix_image_kernel(&img, MPIX_KERNEL_DENOISE, 5);
   mpix_image_kernel(&img, MPIX_KERNEL_SHARPEN, 3);
   mpix_image_convert(&img, MPIX_FORMAT_YUYV);
   mpix_image_to_buf(&img, buf_out, sizeof(buf_out));

   return img.err;

参考资料
********

.. target-notes::

.. _libmpix: https://github.com/libmpix/libmpix
