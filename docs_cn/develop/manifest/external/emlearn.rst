.. _external_module_emlearn:

emlearn
#######

简介
****

`emlearn`_ 是一个用于在微控制器和嵌入式系统上部署机器学习模型的开源库。它提供从 scikit-learn 或 Keras 训练的模型生成可移植 C 代码的能力。

该 Python 库可将复杂的机器学习模型转换为最小的 C 代码表示形式，从而能够在资源受限的嵌入式设备上运行 ML 推理。

emlearn 采用 MIT 许可。

在 Zephyr 中使用
****************

emlearn 仓库是一个 Zephyr :ref:`module <modules>`，为 Zephyr 应用提供 TinyML 能力，使机器学习模型可以直接在搭载 Zephyr 的设备上运行。

要将 emlearn 作为 Zephyr 模块引入，可以将其作为 West 项目添加到 ``west.yaml`` 文件，或通过添加子 manifest（例如 ``zephyr/submanifests/emlearn.yaml``）文件引入，内容如下，然后运行 ``west update``：

.. code-block:: yaml

   manifest:
     projects:
       - name: emlearn
         url: https://github.com/emlearn/emlearn.git
         revision: master
         path: modules/lib/emlearn # adjust the path as needed

更详细的步骤和 API 文档请参阅 `emlearn 文档`_，特别是 `在 Zephyr RTOS 上入门`_ 部分。

参考资料
********

.. target-notes::

.. _emlearn:
   https://github.com/emlearn/emlearn

.. _emlearn 文档:
   https://emlearn.readthedocs.io/en/latest/

.. _在 Zephyr RTOS 上入门:
   https://emlearn.readthedocs.io/en/latest/getting_started_zephyr.html
