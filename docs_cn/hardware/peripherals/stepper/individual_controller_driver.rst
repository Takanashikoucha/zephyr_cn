.. _stepper-individual-controller-driver:

独立步进电机运动控制器和驱动
###############################################

以下是带专用步进电机运动控制器的步进电机驱动的设备树配置示例：

.. code-block:: dts

    / {
        aliases {
            stepper_driver = &tmc2209
            stepper_ctrl = &step_dir_motion_control;
        };

        tmc2209: tmc2209 {
            compatible = "adi,tmc2209";
            enable-gpios = <&gpioa 6 GPIO_ACTIVE_HIGH>;
            m0-gpios = <&gpiob 0 GPIO_ACTIVE_HIGH>;
            m1-gpios = <&gpioa 7 GPIO_ACTIVE_HIGH>;
        };

        step_dir_motion_control: step-dir-motion-control {
            compatible = "zephyr,gpio-step-dir-stepper-ctrl";
            step-gpios = <&gpioa 9 GPIO_ACTIVE_HIGH>;
            dir-gpios = <&gpioc 7 GPIO_ACTIVE_HIGH>;
            invert-direction;
            stepper-driver = <&tmc2209>;
        };
    };

按照上述配置，步进电机驱动子系统可以在应用代码中如下使用：

.. code-block:: c

    static const struct device *stepper_driver = DEVICE_DT_GET(DT_ALIAS(stepper_driver));
    static const struct device *stepper_ctrl = DEVICE_DT_GET(DT_ALIAS(stepper_ctrl));
    ...
    stepper_ctrl_move_to(stepper_ctrl, 200);
    stepper_ctrl_stop(stepper_ctrl);
    stepper_disable(stepper_driver);
