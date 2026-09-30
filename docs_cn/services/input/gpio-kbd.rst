.. _gpio-kbd:

GPIO
Keyboard
Matrix
####################

:dtcompatible:`gpio-kbd-matrix`
driver
support
广泛
的
keyboard
matrix
hardware
configurations
并
有
numerous
的
options
用于
change
它
的
behavior。
这
是
some
common
的
setups
和
它们
如何
被
driver
supported
的
overview。

所有
这些
的
conventional
configuration
是
driver
在
row
GPIOs
（inputs）
上
read
并
在
columns
GPIOs
（output）
上
select。

Base
use
case
no
isolation
diodes
interrupt
capable
的
GPIOs
***********************************************************

这
是
在
consumer
keyboards
上
found
的
common
的
configuration
带
membrane
switches
和
flexible
circuit
boards
没有
isolation
diodes
require
ghosting
detection
（它
default
下
被
enabled）。

.. figure::
   no-diodes.svg
   :align:
   center
   :width:
   50%

   一
   个
   3x3
   matrix
   没有
   diodes

System
必须
support
GPIO
interrupts
且
interrupt
可以
同时
在
所有
row
GPIOs
上
被
enabled。

.. code-block::
   devicetree

   kbd-matrix
   {
        compatible
   =
   "gpio-kbd-matrix";
        row-gpios
   =
   <&gpio0
   0
   (GPIO_PULL_UP
   |
   GPIO_ACTIVE_LOW)>,
                <&gpio0
   1
   (GPIO_PULL_UP
   |
   GPIO_ACTIVE_LOW)>,
                <&gpio0
   2
   (GPIO_PULL_UP
   |
   GPIO_ACTIVE_LOW)>;
        col-gpios
   =
   <&gpio0
   3
   GPIO_ACTIVE_LOW>,
                <&gpio0
   4
   GPIO_ACTIVE_LOW>,
                <&gpio0
   5
   GPIO_ACTIVE_LOW>;
   };


.. note::

   以下为原文（待翻译）

If the key matrix is not complete, a map of the keys that are actually
populated can be specified using the ``actual-key-mask`` property. This allows
the matrix state to be filtered to remove keys that are not present before
ghosting detection, potentially allowing key combinations that would otherwise
be blocked by it.

For example for a 3x3 matrix missing a key:

.. figure:: no-sw4.svg
      :align: center
      :width: 50%

      A 3x3 matrix missing a key.

.. code-block:: devicetree

   kbd-matrix {
        compatible = "gpio-kbd-matrix";
        ...
        actual-key-mask = <0x07 0x05 0x07>;
   };

This would allow, for example, to detect pressing ``Sw1``, ``SW2`` and  ``SW4``
at the same time without triggering anti ghosting.

The actual key mask can be changed at runtime by enabling
:kconfig:option:`CONFIG_INPUT_KBD_ACTUAL_KEY_MASK_DYNAMIC` and the using the
:c:func:`input_kbd_matrix_actual_key_mask_set` API.

Keymap configuration
********************

Keyboard matrix devices report a series of x/y/touch events. These can be
mapped to normal key events using the :dtcompatible:`input-keymap` driver.

For example, the following would setup a ``keymap`` device that take the
x/y/touch events as an input and generate corresponding key events as an
output:

.. code-block:: devicetree

  kbd {
      ...
      keymap {
          compatible = "input-keymap";
          keymap = <
              MATRIX_KEY(0, 0, INPUT_KEY_1)
              MATRIX_KEY(0, 1, INPUT_KEY_2)
              MATRIX_KEY(0, 2, INPUT_KEY_3)
              MATRIX_KEY(1, 0, INPUT_KEY_4)
              MATRIX_KEY(1, 1, INPUT_KEY_5)
              MATRIX_KEY(1, 2, INPUT_KEY_6)
              MATRIX_KEY(2, 0, INPUT_KEY_7)
              MATRIX_KEY(2, 1, INPUT_KEY_8)
              MATRIX_KEY(2, 2, INPUT_KEY_9)
          >;
          row-size = <3>;
          col-size = <3>;
      };
  };

.. doxygengroup:: input_keymap

Keyboard matrix shell commands
******************************

The shell command ``kbd_matrix_state_dump`` can be used to test the
functionality of any keyboard matrix driver implemented using the keyboard
matrix library. Once enabled it logs the state of the matrix every time it
changes, and once disabled it prints an or-mask of any key that has been
detected, which can be used to set the ``actual-key-mask`` property.

The command can be enabled using the
:kconfig:option:`CONFIG_INPUT_SHELL_KBD_MATRIX_STATE`.

Example usage:

.. code-block:: console

   uart:~$ device list
   devices:
   - kbd-matrix (READY)
   uart:~$ input kbd_matrix_state_dump kbd-matrix
   Keyboard state logging enabled for kbd-matrix
   [00:01:41.678,466] <inf> input: kbd-matrix state [01 -- -- --] (1)
   [00:01:41.784,912] <inf> input: kbd-matrix state [-- -- -- --] (0)
   ...
   press more buttons
   ...
   uart:~$ input kbd_matrix_state_dump off
   Keyboard state logging disabled
   [00:01:47.967,651] <inf> input: kbd-matrix key-mask [07 05 07 --] (8)

Keyboard matrix library
***********************

The GPIO keyboard matrix driver is based on a generic keyboard matrix library,
which implements the core functionalities such as scanning delays, debouncing,
idle mode etc. This can be reused to implement other keyboard matrix drivers,
potentially application specific.

.. doxygengroup:: input_kbd_matrix
