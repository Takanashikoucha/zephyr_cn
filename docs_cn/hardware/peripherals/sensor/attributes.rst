.. _sensor-attribute:

传感器属性
#################

:dfn:`属性`（在 :c:enum:`sensor_attribute` 中枚举）是传感器及其通道的不可变属性和可变属性。

属性允许获取元数据并更改传感器配置。常见的配置参数如通道缩放、采样频率、调整通道偏移、信号滤波、电源模式、片上缓冲区以及事件处理选项等非常普遍。属性提供了一套灵活的 API，用于检查和操作这些设备属性。

属性使用 :c:enum:`sensor_attribute` 指定，可配合 :c:func:`sensor_attr_get` 和 :c:func:`sensor_attr_set` 获取和设置传感器的属性。

一个快速示例……

.. code-block:: c

   const struct device *accel_dev = DEVICE_DT_GET(DT_ALIAS(accel0));
   struct sensor_value accel_sample_rate;
   int rc;

   rc = sensor_attr_get(accel_dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, &accel_sample_rate);
   if (rc != 0) {
               printk("Failed to get sampling frequency\n");
   }

   printk("Sample rate for accel %p is %d.06%d\n", accel_dev, accel_sample_rate.val1, accel_sample_rate.val2*1000000);

   accel_sample_rate.val1 = 2000;

   rc = sensor_attr_set(accel_dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, accel_sample_rate);
   if (rc != 0) {
               printk("Failed to set sampling frequency\n");
   }
