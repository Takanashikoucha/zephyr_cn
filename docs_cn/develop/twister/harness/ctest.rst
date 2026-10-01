.. _twister_ctest_harness:

Ctest
#####

ctest_args: <list of arguments>（默认空）
    指定传递给 ``ctest`` 的额外参数列表，例如：
    ``ctest_args: ['--repeat until-pass:5']``。
    注意 ``--ctest-args`` 可多次传递，
    以向 ctest 传递多个参数。
