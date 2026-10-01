.. _pm-device-runtime:

设备运行时电源管理
###############################

简介
************

设备运行时电源管理（PM）框架是一种主动电源管理机制，它通过挂起空闲
或未被使用的设备来降低整个系统的功耗，且与系统状态无关。可通过设置
:kconfig:option:`CONFIG_PM_DEVICE_RUNTIME` 启用。在该模型中，设备驱动负责
指示其何时需要设备、何时不需要。这些信息用于根据使用计数决定何时
挂起或恢复设备。

当某设备启用了设备运行时电源管理后，其状态初始将被设置为
:c:enumerator:`PM_DEVICE_STATE_SUSPENDED`，表示该设备未被使用。在第一次
设备请求时，设备将被恢复并进入 :c:enumerator:`PM_DEVICE_STATE_ACTIVE` 状态。
设备将保持在该状态，直到不再被使用。此时，设备将被挂起，
直到下一次设备请求。如果挂起操作是同步执行的，
设备将立即被置为 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态；
而如果挂起是异步执行的，设备将先被置为
:c:enumerator:`PM_DEVICE_STATE_SUSPENDING` 状态，然后在操作执行时
再进入 :c:enumerator:`PM_DEVICE_STATE_SUSPENDED` 状态。

对于位于电源域（通过设备树 'power-domains' 属性）上的设备，
设备运行时电源管理会自动尝试根据子设备上的
:c:func:`pm_device_runtime_get` 和 :c:func:`pm_device_runtime_put`
调用来请求和释放所依赖的电源域。

为了能够自动控制电源域状态，必须在电源域设备上启用设备运行时 PM。
要全局启用设备运行时 PM，请启用
:kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_DEFAULT_ENABLE`。
要仅为特定设备启用设备运行时 PM，请设置
``zephyr,pm-device-runtime-auto`` 设备树属性，或对特定设备使用
:c:func:`pm_device_runtime_enable`。

.. graphviz::
   :caption: 设备状态与转换

    digraph {
        node [shape=box];
        init [shape=point];

        SUSPENDED [label=PM_DEVICE_STATE_SUSPENDED];
        ACTIVE [label=PM_DEVICE_STATE_ACTIVE];
        SUSPENDING [label=PM_DEVICE_STATE_SUSPENDING];

        init -> SUSPENDED;
        SUSPENDED -> ACTIVE;
        ACTIVE -> SUSPENDED;
        ACTIVE -> SUSPENDING [constraint=false]
        SUSPENDING -> SUSPENDED [constraint=false];
        SUSPENDED -> SUSPENDING [style=invis];
        SUSPENDING -> ACTIVE [style=invis];
    }

设备运行时电源管理框架的设计目标是：以最小的应用工作量来最小化设备功耗。
设备驱动负责指示其何时需要设备处于工作状态、何时不需要。
因此，应用程序不能手动挂起或恢复设备。不过，应用程序可以决定
何时禁用或启用某设备的运行时电源管理。这在某些情况下会很有用，
例如应用程序希望某个设备始终保持激活状态。

设计原则
*****************

当某设备启用运行时 PM 后，在系统电源状态转换期间将不再对其进行
恢复或挂起操作。相反，设备完全负责指示其何时需要设备、何时不需要。
设备运行时 PM API 使用引用计数来跟踪设备的使用情况。这使得 API 能够
判断设备何时需要恢复或挂起。该 API 使用 *get* 和 *put* 术语
分别表示设备何时被需要和何时不再被需要。该机制在考虑设备依赖关系时
起着关键作用。例如，如果一个总线设备被多个传感器使用，
我们可以让总线保持激活状态，直到最后一个传感器使用完毕。

.. note::

    截至目前，设备运行时电源管理 API 尚不管理设备依赖关系。
    这意味着，如果一个设备的运行依赖于其他设备（例如传感器
    可能依赖于总线设备），总线将在每次事务时都被恢复和挂起。
    一般而言，在子设备被使用时保持父设备激活状态效率更高，
    因为子设备可能在短时间内执行多次事务。在该特性添加之前，
    设备可以手动对其依赖关系执行 *get* 或 *put* 操作。

设备驱动可以使用 :c:func:`pm_device_runtime_get` 函数来表示其
*需要*设备处于激活或工作状态。该函数会增加设备使用计数，
并在必要时恢复设备。类似地，:c:func:`pm_device_runtime_put` 函数
可用于表示设备不再被需要。该函数会减少设备使用计数，
并在必要时挂起设备。值得注意的是，在这两种情况下，
操作都是同步执行的。下面的时序图说明了设备如何使用该 API
以及预期的事件顺序。

.. figure:: images/devr-sync-ops.svg

    单个设备上的同步操作

同步模型简单至极。不过，它可能引入不必要的延迟，
因为在设备被挂起之前（如果设备不再被使用），
应用程序无法获得操作结果。如果操作很快，这通常不成问题，
例如切换一个寄存器。然而，如果挂起涉及通过慢速总线发送数据包，
情况就不同了。出于这个原因，设备驱动还可以使用
:c:func:`pm_device_runtime_put_async` 函数。该函数将调度挂起操作，
同样是在设备不再被使用时。

默认情况下，运行时 PM 操作被卸载到系统工作队列。
不过，设备驱动在挂起期间不得执行任何阻塞操作，
因为这会阻塞系统工作队列并对系统响应性产生负面影响。

为解决此问题，应用程序可以配置运行时 PM 使用专用工作队列，
方法是启用 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_USE_DEDICATED_WQ`。

如果需要阻塞行为——例如访问慢速外设或等待总线事务——
则必须改用 PM 子系统工作队列。需要此行为的驱动
可以通过启用 :kconfig:option:`CONFIG_PM_DEVICE_DRIVER_NEEDS_DEDICATED_WQ`
显式请求。

对于资源受限且不需要异步操作的目标，
可以通过取消选择 :kconfig:option:`CONFIG_PM_DEVICE_RUNTIME_ASYNC`
完全禁用该功能，从而减少内存占用和系统复杂度。

.. figure:: images/devr-async-ops.svg

    单个设备上的异步操作

实现指南
*************************

首先，设备驱动需要实现 PM 子系统用于挂起或恢复设备的 PM 动作回调。

.. code-block:: c

    static int mydev_pm_action(const struct device *dev,
                               enum pm_device_action action)
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
        default:
            return -ENOTSUP;
        }

        return 0;
    }

PM 动作回调由 PM 子系统串行化，因此无需特殊同步。

要在某设备上启用设备运行时电源管理，驱动需要在初始化时调用
:c:func:`pm_device_runtime_enable`。注意，如果设备状态为
:c:enumerator:`PM_DEVICE_STATE_ACTIVE`，该函数将挂起设备。
如果设备在物理上已被挂起，init 函数应在调用
:c:func:`pm_device_runtime_enable` 之前先调用
:c:func:`pm_device_init_suspended`。

.. code-block:: c

    /* device driver initialization function */
    static int mydev_init(const struct device *dev)
    {
        int ret;
        ...

        /* OPTIONAL: mark device as suspended if it is physically suspended */
        pm_device_init_suspended(dev);

        /* enable device runtime power management */
        ret = pm_device_runtime_enable(dev);
        if (ret < 0) {
            return ret;
        }
    }

通过在对应的设备树节点上添加 ``zephyr,pm-device-runtime-auto`` 标志，
也可以在设备实例上自动启用设备运行时电源管理。如果启用，
:c:func:`pm_device_runtime_enable` 将在设备 ``init`` 函数运行
并成功返回后立即被调用。

.. code-block:: dts

    foo {
        /* ... */
        zephyr,pm-device-runtime-auto;
    };

假设一个实现了 ``operation`` API 调用的示例设备驱动，
*get* 和 *put* 操作可以按如下方式执行：

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, suspends device if no more users) */
        return pm_device_runtime_put(dev);
    }

如果挂起操作*很慢*，设备驱动可以使用异步 API：

.. code-block:: c

    static int mydev_operation(const struct device *dev)
    {
        int ret;

        /* "get" device (increases usage count, resumes device if suspended) */
        ret = pm_device_runtime_get(dev);
        if (ret < 0) {
            return ret;
        }

        /* do something with the device */
        ...

        /* "put" device (decreases usage count, schedule suspend if no more users) */
        return pm_device_runtime_put_async(dev, K_NO_WAIT);
    }

示例
********

一些展示设备运行时电源管理功能的有用示例：

* :zephyr_file:`tests/subsys/pm/device_runtime_api/`
* :zephyr_file:`tests/subsys/pm/device_power_domains/`
* :zephyr_file:`tests/subsys/pm/power_domain/`
