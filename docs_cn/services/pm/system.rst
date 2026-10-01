.. _pm-system:

系统电源管理
#######################

简介
************

当内核没有可调度任务时，内核进入空闲状态。启用 :kconfig:option:`CONFIG_PM` 后，内核可以调用电源管理子系统，将空闲系统置为受支持的电源状态之一。内核请求一段希望挂起的时长，然后 PM 子系统根据配置的电源管理策略决定应转换到的合适电源状态。

设置唤醒事件是应用程序的责任。唤醒事件通常是由 SoC 外设模块触发的中断。示例包括 SysTick、RTC、计数器或 GPIO。需要注意的是，根据 SoC 和所涉及的电源模式，并非所有外设都处于激活状态，因此某些唤醒源可能无法在所有电源模式下使用。

下图描述了系统电源管理：

.. graphviz::
   :caption: 系统电源管理

    digraph G {
        compound=true
        node [height=1.2 style=rounded]

        lock [label="Lock interrupts"]
        config_pm [label="CONFIG_PM" shape=diamond style="rounded,dashed"]
        forced_state [label="state forced ?", shape=diamond style="rounded,dashed"]
        config_system_managed_device_pm [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
        config_system_managed_device_pm2 [label="CONFIG_PM_DEVICE" shape=diamond style="rounded,dashed"]
        pm_policy [label="Check policy manager\nfor a power state "]
        pm_suspend_devices [label="Suspend\ndevices"]
        pm_resume_devices [label="Resume\ndevices"]
        pm_state_set [label="Enter power state\n(SoC API)" style="rounded,bold"]
        pm_system_resume [label="Resume bookkeeping\n(post ops, notify, clock)" style="rounded,bold"]
        unlock_irq [label="Unlock interrupts"]
        handle_interrupts [label="Handle interrupts\nand schedule threads"]
        k_cpu_idle [label="k_cpu_idle()"]

        subgraph cluster_idle {
            style=dashed
            label = "idle()"

            lock -> config_pm
            config_pm -> k_cpu_idle [label="no"]
            k_cpu_idle -> unlock_irq
        }

        subgraph cluster_pm_system_suspend {
            style=dashed
            label = "pm_system_suspend()"

            forced_state -> config_system_managed_device_pm [label="yes"]
            forced_state -> pm_policy [label="no"]
            pm_policy -> config_system_managed_device_pm
            config_system_managed_device_pm -> pm_state_set [label="no"]
            config_system_managed_device_pm -> pm_suspend_devices [label="yes"]
            pm_suspend_devices -> pm_state_set
            pm_state_set -> config_system_managed_device_pm2
            config_system_managed_device_pm2 -> pm_resume_devices [label="yes"]
            config_system_managed_device_pm2 -> pm_system_resume [label="no"]
            pm_resume_devices -> pm_system_resume
        }

        {rankdir=LR k_cpu_idle; forced_state}
        config_pm -> forced_state [label="yes"]
        pm_policy -> k_cpu_idle [label="PM_STATE_ACTIVE\n(no power state meets requirements)"]
        pm_system_resume -> unlock_irq [constraint=false]
        unlock_irq -> handle_interrupts
        handle_interrupts -> lock:n [label="no runnable thread"]
    }

空闲线程在调用 :c:func:`pm_system_suspend` 之前锁定中断，并保留原始架构中断密钥的所有权。如果 PM 子系统进入低功耗状态，在任何系统管理的设备被恢复之后，PM 恢复簿记在中断仍被锁定的状态下运行，包括 :c:func:`pm_state_exit_post_ops`、PM 退出通知和系统时钟空闲退出统计。在该簿记完成且 :c:func:`pm_system_suspend` 返回后，空闲线程恢复原始中断密钥。

未选择 ``CONFIG_PM_STATE_SET_IRQ_UNLOCKED`` 的架构和 SoC 在低功耗指令的紧邻前后使用架构钩子，以便仍能观察到唤醒事件而无需先分发唤醒源 ISR。在该模式下，:c:func:`pm_state_set` 和 :c:func:`pm_state_exit_post_ops` 只能用于 SoC 特定的硬件工作，不能作为最终的中断解除屏蔽点。

当使用该默认约定时，中断所有权序列如下：

.. mermaid::
   :caption: 系统 PM 中断恢复所有权
   :alt: 时序图，展示空闲线程锁定中断、PM 进入 SoC 电源状态、架构 PM 状态钩子允许无 ISR 分发地唤醒、PM 恢复簿记以及空闲线程解锁中断。

    sequenceDiagram
         participant Workers as Other threads
         participant Idle as idle()<br/>(idle thread context)
         participant PM as pm_system_suspend()
         participant SoC as pm_state_set()<br/>(SoC hook)
         participant HW as Hardware

         loop Idle cycle
             Note over Workers: Thread enters SLEEP/PENDING state<br/>e.g. k_sleep() / k_sem_take()
             alt Runnable thread(s) remaining
                 Workers-->>Workers: Schedule another thread
             else No runnable thread remaining
                 Workers-->>Idle: Switch to idle thread
             end
             Idle->>Idle: Lock interrupts
             Note left of Idle: Interrupts are locked<br/>during PM sequence
             Idle->>PM: Suspend idle CPU
             PM->>PM: Suspend devices<br/>(if applicable)
             PM->>PM: Set idle timeout
             PM->>PM: Notify PM state entry
             PM->>SoC: Enter power state
             SoC->>SoC: SoC-specific pre-entry operations
             SoC->>SoC: Run arch PM prepare hook
             SoC->>HW: Trigger low-power state entry
             HW-->>SoC: Wake-up event occurs
             SoC->>SoC: Run arch PM finish hook
             SoC->>SoC: SoC-specific post-wakeup operations
             SoC-->>PM: Power state exit complete
             PM->>PM: Resume devices<br/>(if applicable)
             PM->>PM: Run post ops, notify exit, clock idle exit
             PM-->>Idle: Resume complete
             Idle->>Idle: Unlock interrupts
             HW-->>Idle: Pending interrupts are handled
             Idle-->>Workers: Idle thread yields<br/>or is preempted
             Note over Workers: Non-idle thread starts executing
         end

使用该默认约定的 SoC 实现不得从 :c:func:`pm_state_set` 或 :c:func:`pm_state_exit_post_ops` 解除中断屏蔽。仍然从这些钩子调用 ``irq_unlock(0)``、``arch_irq_unlock(0)``、``__enable_irq()`` 或等效操作的旧实现，在迁移之前必须选择 ``CONFIG_PM_STATE_SET_IRQ_UNLOCKED``。

.. note::

    上述顺序保证仅适用于 :c:func:`arch_irq_lock` 可以屏蔽的中断。零延迟中断不在该顺序之内。参见 :ref:`zlis`。

电源状态
================

电源管理子系统定义了一组状态，由每个状态关联的功耗和上下文保留来描述。

电源状态集合由 :c:enum:`pm_state` 定义。一般而言，更低的电源状态（枚举中索引更高）将提供更大幅度的节电，并具有更高的唤醒延迟。

电源管理策略
=========================

电源管理子系统支持以下电源管理策略：

* 基于驻留时间
* 应用定义

策略管理器是电源管理子系统中负责决定系统应转换到哪个电源状态的组件。策略管理器只能在该平台已定义的状态之间进行选择。施加于该决策的其他约束可能包括禁止某些电源状态的锁，或根据策略而异的各种最小和最大延迟值。

关于状态定义的更多细节可在 :dtcompatible:`zephyr,power-state` 绑定文档中找到。

驻留时间
---------

在驻留时间策略下，系统将进入提供最大节电的电源状态，约束条件是最小驻留时间值（参见 :dtcompatible:`zephyr,power-state`）与退出该模式的延迟之和必须小于或等于内核调度的系统空闲时长。

因此，核心逻辑可以用以下表达式概括：

.. code-block:: c

   if (time_to_next_scheduled_event >= (state.min_residency_us + state.exit_latency)) {
      return state
   }

应用
-----------

应用程序通过实现 :c:func:`pm_policy_next_state` 函数来定义电源管理策略。在该策略中，应用程序可以基于距下一次计划超时的剩余时间自由决定系统应转换到哪个电源状态。

一个定义自身策略的应用程序示例可在 :zephyr_file:`tests/subsys/pm/power_mgmt/` 中找到。

自定义滴答钩子
-----------------

除了内核滴答超时和 PM 策略事件列表外，应用程序和 SoC 特定代码可能需要从专有或硬件特定的数据源推导下一次唤醒时间。示例包括硬件寄存器、仅二进制的第三方模块，或难以建模为标准 PM 策略事件的复杂/遗留数据结构。

当启用 :kconfig:option:`CONFIG_PM_CUSTOM_TICKS_HOOK` 时，PM 核心在 :c:func:`pm_system_suspend()` 期间调用可选函数 :c:func:`pm_policy_next_custom_ticks()`。该钩子返回到下一次自定义事件的滴答数，如果无需考虑自定义事件则返回 ``K_TICKS_FOREVER``。

然后 PM 核心从以下各项中选择最早的超时：

* 内核滴答超时，
* PM 策略事件列表滴答数（来自 :c:func:`pm_policy_next_event_ticks()`），
* 自定义滴答值（来自 :c:func:`pm_policy_next_custom_ticks()`）。

该机制允许开发板和应用程序在不修改 PM 事件列表基础设施的情况下，将额外的定时源集成到系统电源管理决策中。

.. _pm-policy-power-states:

策略与电源状态
------------------------

电源管理子系统允许不同的 Zephyr 组件和应用程序配置策略管理器，以阻止系统转换到某些电源状态。设备在执行后台任务时可以使用该机制，防止系统进入会丢失上下文的特定状态。参见 :c:func:`pm_policy_state_lock_get`。

示例
========

一些展示不同电源管理特性的有用示例：

* :zephyr_file:`samples/boards/st/power_mgmt/blinky/`
* :zephyr_file:`samples/boards/espressif/deep_sleep/`
* :zephyr_file:`samples/subsys/pm/device_pm/`
* :zephyr_file:`tests/subsys/pm/power_mgmt/`
* :zephyr_file:`tests/subsys/pm/power_mgmt_soc/`
* :zephyr_file:`tests/subsys/pm/power_states_api/`
