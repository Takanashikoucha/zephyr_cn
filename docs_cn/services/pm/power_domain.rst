.. _pm-power-domain:

电源域
############

简介
************

Zephyr 电源域抽象被设计用于支持由共同电源供电的设备分组，以便以通用方式通知电源状态变化。使用设备 A 的应用程序代码不需要知道设备 B 位于同一电源域上并且也应该被配置为低功耗状态。

电源域在 Zephyr 中是可选的，要启用该特性，必须设置选项 :kconfig:option:`CONFIG_PM_DEVICE_POWER_DOMAIN`。

当电源域自身开启或关闭时，电源域负责通过其电源管理回调通知所有使用它的设备，该回调分别以 :c:enumerator:`PM_DEVICE_ACTION_TURN_ON` 或 :c:enumerator:`PM_DEVICE_ACTION_TURN_OFF` 调用。此工作流程在下图中展示。

.. _pm-domain-work-flow:

.. graphviz::
   :caption: 电源域工作流程

    digraph {
        rankdir="TB";

        action [style=invis]
        {
            rank = same;
            rankdir="LR"
            devA [label="gpio0"]
            devB [label="gpio1"]
        }
        domain [label="gpio_domain"]

       action -> devA [label="pm_device_runtime_get()"]
       devA:se -> domain:n [label="pm_device_runtime_get()"]

       domain -> devB [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
       domain:sw -> devA:sw [label="action_cb(PM_DEVICE_ACTION_TURN_ON)"]
    }

内部电源域
----------------------

SoC 中的大多数设备具有独立的电源控制，可以开启或关闭以降低功耗。但存在大量无法仅通过设备电源管理控制的静态电流泄漏。为解决此问题，SoC 通常被划分为若干区域，将通常一起使用的设备分组，以便未使用的区域可以完全断电以消除该泄漏。这些区域被称为"电源域"，可以以层级形式存在并且可以嵌套。

外部电源域
----------------------

SoC 外部的设备可以由 SoC 主电源以外的电源供电。这些外部电源通常是开关、稳压器或专用电源 IC。多个设备可以由同一电源供电，这种设备分组通常被称为"电源域"。

将设备放置在电源域上可以出于多种原因，包括使高功耗设备在低功耗模式下能够在未使用时完全关闭。

实现指南
*************************

首先，充当电源域的设备需要声明与 ``power-domain`` 兼容。以 :ref:`pm-domain-work-flow` 为例，以下代码定义了一个名为 ``gpio_domain`` 的电源域。

.. code-block:: devicetree

	gpio_domain: gpio_domain@4 {
		compatible = "power-domain";
		...
	};

电源域需要实现 PM 子系统用于开启和关闭设备的 PM 动作回调。

.. code-block:: c

    static int mydomain_pm_action(const struct device *dev,
                               enum pm_device_action action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_RESUME:
            /* resume the domain */
            ...
            /* notify children domain is now powered */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_ON, NULL);
            break;
        case PM_DEVICE_ACTION_SUSPEND:
            /* notify children domain is going down */
            pm_device_children_action_run(dev, PM_DEVICE_ACTION_TURN_OFF, NULL);
            /* suspend the domain */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* turn on the domain (e.g. setup control pins to disabled) */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* turn off the domain (e.g. reset control pins to default state) */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

属于该电源域的设备可以在 ``power-domain`` 节点的属性中引用该电源域来声明。下面的示例声明了属于电源域 ``gpio_domain`` 的设备 ``gpio0`` 和 ``gpio1``。

.. code-block:: devicetree

        &gpio0 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

        &gpio1 {
                compatible = "zephyr,gpio-emul";
                gpio-controller;
                power-domains = <&gpio_domain>;
        };

当电源域状态改变时，该电源域下的所有设备都会收到通知。这些通知作为动作通过设备的 PM 动作回调发送，设备可以使用它们执行所需的额外工作。不过这些通知可以安全地忽略。

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action *action)
    {
        switch (action) {
        case PM_DEVICE_ACTION_SUSPEND:
            /* suspend the device */
            ...
            break;
        case PM_DEVICE_ACTION_RESUME:
            /* resume the device */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_ON:
            /* configure the device into low power mode */
            ...
            break;
        case PM_DEVICE_ACTION_TURN_OFF:
            /* prepare the device for power down */
            ...
            break;
        default:
            return -ENOTSUP;
        }

        return 0;
    }

.. note::

   如果依赖某电源域的设备被用作"唤醒"源，则将该电源域设置为"唤醒"源是驱动或应用程序的责任。

示例
********

一些展示电源域特性的有用示例：

* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
