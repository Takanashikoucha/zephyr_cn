.. _control_flow_integrity:

控制流完整性
######################

控制流完整性（CFI）是一项安全特性，确保程序的控制流遵循预定义路径，防止攻击者将执行重定向到恶意代码。CFI 在防御控制流劫持攻击（如返回导向编程（ROP）和跳转导向编程（JOP））方面特别有用。

CFI 通过在运行时验证程序的控制流来工作，确保函数调用和返回指向合法目标。这通常通过代码插桩实现，添加检查以验证控制流遵循程序控制流图定义的预期路径。

前向边与返回边
------------------------

在 CFI 的上下文中，控制流边可分为两类：

1. **前向边**：表示从一个函数到另一个函数的控制流，例如函数调用。前向边通常经过验证，以确保调用的目标是程序内的合法函数。
2. **返回边**：表示从函数返回到调用者的过程。返回边经过验证，以确保返回地址合法且对应于有效的调用点。

前向边可由编译器插桩支持，添加检查以验证函数调用目标有效。返回边可通过维护影子栈或使用其他机制支持，以确保返回地址合法。

Zephyr 支持维护影子栈，可通过 :kconfig:option:`CONFIG_HW_SHADOW_STACK` 启用。然后，内核将使用诸如 :c:macro:`K_THREAD_HW_SHADOW_STACK_DEFINE` 之类的宏，与其他线程栈相关宏配合，为线程使用的影子栈提供区域。通常，应用程序只需启用 :kconfig:option:`CONFIG_HW_SHADOW_STACK`（以及相关选项，如 :kconfig:option:`CONFIG_HW_SHADOW_STACK_PERCENTAGE_SIZE` 和 :kconfig:option:`CONFIG_HW_SHADOW_STACK_MIN_SIZE`）即可启用影子栈支持。内核随后会自动为每个线程管理影子栈。

实现细节
**********************

``K_THREAD_HW_SHADOW_STACK*`` 系列宏对影子栈参数进行最小化设置。然后，它们调用架构特定的 ``ARCH_THREAD_HW_SHADOW_STACK*`` 宏来执行实际设置。

硬件支持
----------------

虽然 CFI 可以用软件实现，但硬件支持可显著增强其有效性和性能。目前，Zephyr 支持 Intel 控制流执行技术（CET），为 CFI 提供基于硬件的支持。

Intel CET
*********

Intel 控制流执行技术（CET）是一组通过支持 CFI 增强应用安全的硬件特性。CET 包含两个主要组件：

1. **影子栈**：该特性为返回地址维护一个独立的栈，确保返回地址无法被篡改。当函数返回时，返回地址从影子栈弹出并与常规栈中的值比较，提供针对控制流劫持的额外保护层。
2. **间接分支跟踪（IBT）**：该特性跟踪间接分支（如函数指针），确保它们只指向代码中的有效位置。它防止攻击者通过 ROP 等技术将执行重定向到任意代码。

这两个特性分别证明了返回边和前向边验证。要在 Zephyr 中启用影子栈支持，在支持的硬件上，可使用 :kconfig:option:`CONFIG_HW_SHADOW_STACK` Kconfig 选项。要启用 IBT，使用 :kconfig:option:`CONFIG_X86_CET_IBT`。

由于 IBT 实际上由编译器实现，因此需要工具链支持。目前，Zephyr SDK x86 工具链可用于构建具有 IBT 支持的应用程序。然而，其预编译产物（如 ``libc`` 和 ``libgcc``）未启用 IBT。因此，对于 ``libc``，需要将其作为模块构建，例如使用 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE`。对于其他部分，则需要自定义工具链。

Intel CET 限制
^^^^^^^^^^^^^^^^^

目前，幕后创建的影子栈位于全局命名空间。因此，即使在不同编译单元之间，也*不能*重用线程栈名称。

ARM 指针认证与分支目标识别
*************************************************************

ARM 平台通过指针认证（PAC）和分支目标识别（BTI）提供基于硬件的 CFI 特性，在 Cortex-M 和 ARM64（Cortex-A/R）架构上均可用：

1. **指针认证（PAC）**：使用密码学签名对返回地址和其他指针进行签名。当返回地址压入栈时，使用每个线程唯一的密钥对其进行签名。在返回前，验证签名，确保返回地址未被篡改。这可防御返回导向编程（ROP）攻击。在 ARMv8.1-M Mainline（Cortex-M）和 ARMv8.3-A 及更高版本（ARM64）上可用。

2. **分支目标识别（BTI）**：用特殊的 BTI 着陆垫指令标记合法的间接分支目标。处理器验证间接分支只落在用 BTI 指令标记的有效目标上。这可防御跳转导向编程（JOP）攻击。在 ARMv8.1-M Mainline（Cortex-M）和 ARMv8.5-A 及更高版本（ARM64）上可用。

这些特性分别提供返回边和前向边验证。PAC 和 BTI 可通过 :kconfig:option:`ARM_PACBTI` 菜单启用。可用选项包括 :kconfig:option:`CONFIG_ARM_PACBTI_STANDARD`（PAC 和 BTI 两者）、:kconfig:option:`CONFIG_ARM_PACBTI_PACRET`（仅 PAC）、:kconfig:option:`CONFIG_ARM_PACBTI_BTI`（仅 BTI）及其他变体。两个特性可独立使用或组合使用，以实现全面的控制流完整性。

与 x86 CET IBT 类似，这些特性需要编译器支持和适当的 C 库插桩。PAC 要求函数使用适当的签名和验证指令，而 BTI 要求所有合法分支目标包含 BTI 着陆垫指令。工具链的预编译 C 库通常缺少此插桩。

要支持 BTI，C 库必须使用 ``-mbranch-protection`` 标志编译，以在所有函数中包含 BTI 着陆垫。因此，当使用任何启用 BTI 的选项时，只能使用 :kconfig:option:`CONFIG_MINIMAL_LIBC` 或通过 :kconfig:option:`CONFIG_PICOLIBC_USE_MODULE` 作为模块构建的 picolibc。工具链的 Newlib 不支持 BTI。

PAC 的要求不太严格，因为它主要影响函数序言和尾声，但为了最佳安全性，建议使用 PAC 支持构建 C 库。
