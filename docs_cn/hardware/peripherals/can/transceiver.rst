.. _can_transceiver_api:

CAN 收发器
###############

.. contents::
    :local:
    :depth: 2

概述
********

CAN 收发器是一种外部设备，用于将 CAN 控制器的逻辑电平信号转换为总线电平。
总线线称为 CAN High（CAN H）和 CAN Low（CAN L）。
从控制器到收发器的发送线称为 CAN TX，接收线称为 CAN RX。
这些线使用逻辑电平，而总线电平在 CAN H 和 CAN L 之间以差分方式解释。
总线可以处于隐性（recessive，逻辑 1）或显性（dominant，逻辑 0）状态。
隐性状态是 CAN H 和 CAN L 两条线大致处于相同电压电平的状态，该状态也是空闲（idle）状态。
要向总线写入显性位，开漏（open-drain）晶体管将 CAN H 连接到 Vdd、将 CAN L 连接到地。
第一个和最后一个节点在 CAN H 和 CAN L 之间使用 120 欧姆电阻来终结（terminate）总线。
显性状态始终覆盖隐性状态，这种结构称为线与（wired-AND）。

.. image:: transceiver.svg
    :width: 70%
    :align: center
    :alt: CAN 收发器

CAN 收发器 API 参考
*****************************

.. doxygengroup:: can_transceiver
