..
    Zephyr 项目文档主文件

.. _zephyr-home:

Zephyr 项目文档
############################

.. raw:: html

   <script>
     function openVersionSelector() {
       // Open the mobile menu if visible
       var mobileMenu = document.querySelector('[data-toggle="wy-nav-top"]');
       if (mobileMenu && mobileMenu.offsetParent !== null) {
         mobileMenu.click();
       }
       // Open the version selector
       var versionSelector = document.querySelector('[data-toggle="rst-current-version"]');
       if (versionSelector) {
         versionSelector.click();
       }
     }
   </script>

.. only:: release

   .. admonition:: 欢迎使用 Zephyr 项目文档（|version| 版本）。
      :class: welcome

      .. raw:: html

         <p>
           使用<a href="#" onclick="openVersionSelector(); return false;">版本选择器</a>
           查看 Zephyr 其他版本的文档。
         </p>

.. only:: development

   .. admonition:: 欢迎使用 Zephyr 项目 ``main`` 分支（|version|）文档。
      :class: welcome

      .. raw:: html

         <p>
           使用<a href="#" onclick="openVersionSelector(); return false;">版本选择器</a>
           查看之前发布版本的文档。
         </p>

.. toctree::
   :maxdepth: 1
   :hidden:

   introduction/index.rst
   develop/index.rst
   kernel/index.rst
   services/index.rst
   build/index.rst
   hardware/index.rst
   contribute/index.rst
   project/index.rst
   security/index.rst
   safety/index.rst
   samples/index.rst
   boards/index.rst
   releases/index.rst
   源码阅读指南.rst
