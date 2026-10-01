.. _random_api:

随机数生成
########################

概述
********

随机数 API 子系统提供密码学安全与非密码学安全两种随机数生成 API。选择哪个随机数 API 取决于随机数的密码学要求。如果需要非密码学随机数，非密码学 API 的返回速度会快得多。

- 对于非密码学用途（如随机化延迟、数据洗牌或通用随机化），使用 :c:func:`sys_rand_get` 及相关函数。这些函数速度更快，但不适用于安全场景。

- 对于密码学用途（如生成加密密钥、nonce、初始化向量，或任何对攻击者必须不可预测的数据），使用 :c:func:`sys_csrand_get`。

.. warning::

   切勿将非密码学随机函数（:c:func:`sys_rand_get`、
   :c:func:`sys_rand8_get`、:c:func:`sys_rand16_get`、:c:func:`sys_rand32_get`、
   :c:func:`sys_rand64_get`）用于安全敏感操作。这些函数
   不提供密码学安全的随机数。

API 用法
*********

非密码学随机数
================

以下函数提供非密码学安全的随机数：

- :c:func:`sys_rand_get` - 用随机字节填充缓冲区
- :c:func:`sys_rand8_get` - 获取一个随机 8 位值
- :c:func:`sys_rand16_get` - 获取一个随机 16 位值
- :c:func:`sys_rand32_get` - 获取一个随机 32 位值
- :c:func:`sys_rand64_get` - 获取一个随机 64 位值

使用示例：

.. code-block:: c

   #include <zephyr/random/random.h>

   void example_random_usage(void)
   {
       uint8_t buffer[16];
       uint32_t random_value;

       /* Fill buffer with random bytes */
       sys_rand_get(buffer, sizeof(buffer));

       /* Get a single random 32-bit value */
       random_value = sys_rand32_get();
   }

密码学安全随机数
================================

对于密码学用途，使用 :c:func:`sys_csrand_get`：

.. code-block:: c

   #include <zephyr/random/random.h>

   int generate_encryption_key(uint8_t *key, size_t key_len)
   {
       int ret;

       ret = sys_csrand_get(key, key_len);
       if (ret != 0) {
           /* Handle error - entropy source may have failed */
           return ret;
       }

       return 0;
   }

.. note::

   :c:func:`sys_csrand_get` 成功时返回 0，熵源故障时返回 ``-EIO``。生成
   密码学材料时务必检查返回值。

.. _random_kconfig:

Kconfig 选项
***************

所有配置选项可在 :zephyr_file:`subsys/random/Kconfig` 中找到。

通用选项
==============

:kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`
  用于测试，该选项允许使用非随机数生成器，并允许随机数 API 返回并非真正随机的值。

  .. warning::

     该选项仅用于在没有硬件熵支持的平台上进行测试。启用该选项时生成的
     随机数是可预测的，不适用于任何安全敏感用途。

非密码学随机数生成器选择

:kconfig:option:`CONFIG_ENTROPY_DEVICE_RANDOM_GENERATOR`
   直接使用硬件熵驱动生成随机数。
   这提供高质量的随机数，但可能比伪随机方案更慢。当硬件熵源的
   性能足以满足应用需求时选择此选项。

:kconfig:option:`CONFIG_XOSHIRO_RANDOM_GENERATOR`
   使用由硬件熵源播种的 Xoshiro128++ 伪随机数生成器。这是一个快速、
   通用的 PRNG，具有 128 位状态，通过所有标准随机性测试。

   对于大多数需要快速非密码学随机数的应用，推荐选择此项。

:kconfig:option:`CONFIG_TIMER_RANDOM_GENERATOR`
   使用系统定时器生成伪随机数。该生成器
   产生可预测的值，**仅用于**在没有硬件熵支持的平台上
   进行测试。

   需要启用 :kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`。

密码学安全随机数生成器选择
==================================================

:kconfig:option:`CSPRNG_GENERATOR_CHOICE` kconfig choice 用于选择
密码学安全随机数生成的来源。

要在板级或 SoC 配置文件中覆盖默认值：

.. code-block:: kconfig

   choice CSPRNG_GENERATOR_CHOICE
	   default PSA_CSPRNG_GENERATOR
   endchoice

可用生成器：

:kconfig:option:`CONFIG_HARDWARE_DEVICE_CS_GENERATOR`
  直接使用硬件熵驱动作为密码学安全随机数的来源。当硬件随机数生成器
  已通过认证或验证可用于密码学用途时选择此项。

:kconfig:option:`CONFIG_PSA_CSPRNG_GENERATOR`
  启用一个使用 PSA Crypto API 的密码学安全随机数生成器。该 CSPRNG 实现利用底层 PSA Crypto
  库的安全随机数生成能力，在可用时可使用硬件熵源。PSA CSPRNG 提供适用于安全敏感应用的密码学安全
  随机数。

:kconfig:option:`CONFIG_TEST_CSPRNG_GENERATOR`
  将 :c:func:`sys_csrand_get` 的调用路由到 :c:func:`sys_rand_get`。
  这允许在没有硬件熵支持的平台上测试需要 CSPRNG 的库。

  需要启用 :kconfig:option:`CONFIG_TEST_RANDOM_GENERATOR`。

  .. warning::

     该选项**不提供任何密码学安全性**。仅用于测试。

设备树配置
************************

随机数子系统使用 ``zephyr,entropy`` chosen 节点来识别
硬件熵设备：

.. code-block:: devicetree

   / {
       chosen {
           zephyr,entropy = &rng;
       };
   };

如果平台具有硬件随机数生成器，请确保板级设备树正确指定了该 chosen 节点。

API 参考
*************

.. doxygengroup:: random_api
