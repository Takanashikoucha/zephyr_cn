.. _cmsis_rtos_v2:

CMSIS RTOS v2
##########################

Cortex-M 软件接口标准（CMSIS）RTOS 是面向 ARM Cortex-M 处理器系列的厂商无关硬件抽象层，
定义了通用工具接口。它最初仅针对 ARM Cortex-M 微控制器定义，但可以很容易地扩展到其他
微控制器，从而使其具有通用性。有关 CMSIS RTOS v2 的更多信息，请参阅
`CMSIS-RTOS2 文档 <https://arm-software.github.io/CMSIS_6/latest/RTOS2/index.html>`_。

Zephyr 实现中不支持的特性
***********************************************

内核
    ``osKernelGetState``、``osKernelSuspend``、``osKernelResume``、``osKernelInitialize``
    和 ``osKernelStart`` 均不受支持。

互斥锁
    ``osMutexPrioInherit`` 默认受支持且不可配置，
    您无法选择/取消选择该属性。

    ``osMutexRecursive`` 同样默认受支持。如果未设置该属性，
    同一线程第二次尝试获取它时将抛出错误。

    ``osMutexRobust`` 在 Zephyr 中不受支持。

Zephyr 实现中不支持的返回值
********************************************************

``osKernelUnlock``、``osKernelLock``、``osKernelRestoreLock``
    ``osError``（未指定的错误）不受支持。

``osSemaphoreDelete``
    ``osErrorResource``（由参数 semaphore_id 指定的信号量
    处于无效的信号量状态）不受支持。

``osMutexDelete``
    ``osErrorResource``（由参数 mutex_id 指定的互斥锁
    处于无效的互斥锁状态）不受支持。

``osTimerDelete``
    ``osErrorResource``（由参数 timer_id 指定的定时器
    处于无效的定时器状态）不受支持。

``osMessageQueueReset``
    ``osErrorResource``（由参数 msgq_id 指定的消息队列
    处于无效的消息队列状态）不受支持。

``osMessageQueueDelete``
    ``osErrorResource``（由参数 msgq_id 指定的消息队列
    处于无效的消息队列状态）不受支持。

``osMemoryPoolFree``
    ``osErrorResource``（由参数 mp_id 指定的内存池
    处于无效的内存池状态）不受支持。

``osMemoryPoolDelete``
    ``osErrorResource``（由参数 mp_id 指定的内存池
    处于无效的内存池状态）不受支持。

``osEventFlagsSet``、``osEventFlagsClear``
    ``osFlagsErrorUnknown``（未指定的错误）
    和 osFlagsErrorResource（由参数 ef_id 指定的事件标志对象
    尚未准备好使用）不受支持。

``osEventFlagsDelete``
    ``osErrorParameter``（参数 ef_id 的值
    不正确）不受支持。

``osThreadFlagsSet``
    ``osFlagsErrorUnknown``（未指定的错误）
    和 ``osFlagsErrorResource``（由参数 thread_id 指定的线程
    未处于可接收标志的活跃状态）不受支持。

``osThreadFlagsClear``
    ``osFlagsErrorResource``（正在运行的线程未处于
    可接收标志的活跃状态）不受支持。

``osDelayUntil``
    ``osParameter``（时间无法处理）不受支持。
