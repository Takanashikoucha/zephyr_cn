.. _twister_console_harness:

Console
#######

``console`` 测试框架（harness）指示 Twister 解析测试的文本输出，以匹配测试 YAML 文件中定义的正则表达式。

当前支持的选项如下：

type: <one_line|multi_line>（必需）
    取决于要匹配的正则表达式字符串

regex: <list of regular expressions>（必需）
    包含正则表达式的字符串列表，用于与测试输出进行匹配，
    以确认测试按预期运行。

ordered: <True|False>（默认 False）
    按顺序或随机方式检查正则表达式字符串

record: <recording options>（可选）
  regex: <list of regular expressions>（必需）
    带命名子组的正则表达式，用于匹配测试实例输出行中找到的数据字段，
    这些数据字段提供某些自定义数据以供进一步分析。
    这些记录将写入构建目录的 ``recording.csv`` 文件，
    以及 ``twister.json`` 中测试套件对象的 ``recording`` 属性。

    给定多个正则表达式时，每个表达式都将应用到每个输出行，
    产生来自同一输出行的若干不同记录，或来自不同行的不同记录，
    或来自不同行的相似记录。

    .CSV 文件的列数与所有记录中检测到的字段数相同；缺失值以空字符串填充。

    例如，要提取三个数据字段 ``metric``、``cycles``、``nanoseconds``：

    .. code-block:: yaml

      record:
        regex:
          - "(?P<metric>.*):(?P<cycles>.*) cycles, (?P<nanoseconds>.*) ns"

  merge: <True|False>（默认 False）
    允许在测试实例中仅保留一条记录，包含由正则表达式提取的所有数据字段。
    同名字段将放入按其在记录中出现顺序排列的列表中。
    此类多值字段的值数量可能因正则表达式规则和测试输出而异。

  as_json: <list of regex subgroup names>（可选）
    由正则表达式提取到命名子组的数据字段，
    将被额外解析为 JSON 编码字符串，
    并写入 ``twister.json`` 作为嵌套的 ``recording`` 对象属性。
    对应的 ``recording.csv`` 列将原样包含 JSON 字符串。

    使用此选项，测试日志可以传达从测试镜像传递的分层数据结构，
    以供汇总结果、跟踪、统计等进一步分析。

    例如，此配置：

    .. code-block:: yaml

      record:
        regex: "RECORD:(?P<type>.*):DATA:(?P<metrics>.*)"
        as_json: [metrics]

    匹配到测试日志字符串：

    .. code-block:: none

      RECORD:jitter_drift:DATA:{"rollovers":0, "mean_us":1000.0}

    将在 ``twister.json`` 中报告为：

    .. code-block:: json

      "recording":[
          {
                "type":"jitter_drift",
                "metrics":{
                    "rollovers":0,
                    "mean_us":1000.0
                }
          }
      ]
