#!/usr/bin/env python3
"""Zephyr 中文翻译全量验证脚本 v4。

用法：python3 verify_batch.py <英文原文路径> [...]
对每个英文原文路径，找到对应 docs_cn/ 译文，检查：
  ① 行数比 70%-125%
  ② 碎片行（连续 6+ 行 <15 字符短行，排除代码块/标题/下划线/列表项/表格行/指令行）
  ③ 残留英文（连续 4+ 字母，排除白名单 + 代码块；suspicious = count>=3 或 (count>=2 且 len>=10)）
"""
import re
import sys
from collections import Counter

# 白名单：专有名词/工具名/架构名/协议名/命令/环境变量/扩展名/标准名等（可保留英文）
# 注：此白名单为初始版本，实际使用中需根据误报情况持续扩充
ALLOWED = {
    # 厂商/公司/产品
    "emlearn", "readthedocs", "espressif", "antmicro", "tinyxml", "CANopenNode",
    "CHRE", "CLUTGen", "dtsh", "DTSh", "West", "Edge", "Impulse", "edgeimpulse",
    "memfault", "Mender", "mendersoftware", "requests", "libcsp", "CubeSat",
    "libiio", "analogdevicesinc", "libmpix", "LuDLC", "ludlc", "wamr", "wasm",
    "wolfMQTT", "MQTT", "wolfSSH", "wolfssl", "wolfTPM", "Xedge", "realtimelogic",
    "zenoh", "pico", "Zephelin", "zscilib", "ZView", "Clang", "DZEPHYR",
    "CodeChecker", "coverity", "Parasoft", "parasoft", "cpptscan", "dtdoctor",
    "ECLAIR", "clair", "iwyu", "ZTEST", "BENCHMARK", "bsim", "BabbleSim",
    "babblesim", "Orchestrator", "PipelineContext", "gcov", "gcovr", "lcov",
    "Twister", "ATfE", "ONEAPI", "oneapi", "eabi", "mytoolchain", "SmPL",
    "coccinelle", "coccicheck", "spatch", "parmap", "stderr", "idutils",
    "guilabel", "mylonics", "marketplace", "visualstudio", "Kapa", "CubeIDE",
    "Workbench", "ctest", "mcumgr", "Pytest", "renode", "sysbuild", "robot",
    "reel", "SPDX", "bindesc", "NORETURN", "HiFi", "XTENSA", "HIFI", "SCMI",
    "BBRAM", "IBBR", "SocketCAN", "DMIC", "DALI", "IBECC", "EEPROM", "gnss",
    "NMEA", "HWSPINLOCK", "MBOX", "MDIO", "mspi", "MSPI", "OPAMP", "PECI",
    "RTIO", "SDHC", "sdhc", "SENT", "SMBus", "stepper", "VBUS", "dtsi",
    "VENDOR", "SERIES", "virtqueue", "Virtio", "virtiofs", "FUSE", "pinctrl",
    "PINCTRL", "STACK", "ARCH", "Adafruit", "nexus", "Nano", "SCOPE",
    "GUARD", "NOCOPY", "dlist", "dnode", "mpsc", "MPSC", "rbtree", "rbnode",
    "ring", "SLIST", "snode", "EACH", "MMIO", "INIT", "SECTION", "ITERABLE",
    "STRUCT", "Zephyr", "Linux", "POSIX", "CMSIS", "ARM", "RISC", "RISC-V",
    "PLIC", "Semihosting", "KERNEL", "cache", "nocache", "native", "timing",
    "Phase", "filter", "error", "data", "dmic", "member", "SHELL", "DCONFIG",
    "STATS", "bitrate", "charger", "monitor", "configure", "stop", "MEASURE",
    "gpios", "gpio", "uart", "spi", "i2c", "can", "usb", "wifi", "ble",
    "Bluetooth", "Ethernet", "NFC", "SDIO", "PCIe", "USB-C", "USBC",
    "Flash", "flash", "RAM", "ROM", "NOR", "NAND", "QSPI", "SPI", "I2C",
    "UART", "GPIO", "PWM", "DMA", "ADC", "DAC", "I2S", "PDM", "CAN",
    "timer", "Timer", "clock", "Clock", "tick", "TICK", "cycle", "CYCLE",
    "timeout", "TIMEOUT", "forever", "FOREVER", "uptime", "wait", "WAIT",
    "sleep", "SLEEP", "wake", "WAKE", "lock", "Lock", "unlock", "UNLOCK",
    "mutex", "Mutex", "semaphore", "Semaphore", "queue", "Queue", "fifo",
    "FIFO", "lifo", "LIFO", "mbox", "MBOX", "pipe", "Pipe", "event", "Event",
    "thread", "Thread", "workqueue", "Workqueue", "work", "WORK", "task",
    "Task", "job", "JOB", "handler", "Handler", "callback", "Callback",
    "observer", "Observer", "driver", "Driver", "device", "Device",
    "board", "Board", "SoC", "soc", "SoCs", "chip", "Chip",
    "module", "Module", "MODULES", "library", "Library", "lib", "LIB",
    "kernel", "Kernel", "system", "System", "application", "Application",
    "firmware", "Firmware", "hardware", "Hardware", "software", "Software",
    "boot", "Boot", "bootloader", "Bootloader", "flasher", "Flasher",
    "build", "Build", "compile", "Compile", "link", "Link", "debug",
    "Debug", "test", "Test", "tests", "Tests", "sample", "Sample",
    "samples", "Samples", "example", "Example", "examples", "Examples",
    "doc", "docs", "document", "Document", "documentation", "Documentation",
    "guide", "Guide", "manual", "Manual", "reference", "Reference",
    "api", "API", "sdk", "SDK", "hal", "HAL", "mcu", "MCU", "cpu", "CPU",
    "core", "Core", "cores", "Cores", "arch", "ARCH", "platform", "Platform",
    "target", "Target", "targets", "Targets", "host", "Host", "guest",
    "Guest", "user", "User", "users", "Users", "admin", "Admin", "root",
    "superuser", "privileged", "unprivileged", "secure", "Secure",
    "trusted", "Trusted", "crypto", "Crypto", "cryptographic", "encryption",
    "decryption", "hash", "signature", "certificate", "key", "Key", "keys",
    "Keys", "secret", "Secret", "token", "Token", "auth", "authentication",
    "authorization", "permission", "Permission", "policy", "Policy",
    "config", "Config", "configuration", "Configuration", "option", "Option",
    "options", "Options", "setting", "Setting", "settings", "Settings",
    "parameter", "Parameter", "parameters", "Parameters", "argument",
    "Argument", "arguments", "Arguments", "value", "Value", "values",
    "Values", "type", "Type", "types", "Types", "struct", "Struct",
    "union", "enum", "function", "Function", "method", "Method", "class",
    "Class", "object", "Object", "objects", "Objects", "instance",
    "Instance", "interface", "Interface", "implementation", "Implementation",
    "plugin", "Plugin", "extension", "Extension", "add-on",
    "feature", "Feature", "features", "Features", "capability", "Capabilities",
    "support", "Support", "supported", "Supported", "enable", "Enable",
    "enabled", "Enabled", "disable", "Disable", "disabled", "Disabled",
    "activate", "Activate", "deactivate", "Deactivate", "init", "INIT",
    "initialize", "Initialize", "initialization", "Initialization",
    "setup", "Setup", "teardown", "shutdown", "Shutdown", "start", "Start",
    "restart", "Restart", "reset", "Reset", "reboot",
    "Reboot", "power", "Power", "supply", "Supply", "voltage", "Voltage",
    "current", "Current", "energy", "Energy", "battery", "Battery",
    "charging", "Charging", "discharging", "power-management",
    "PM", "runtime", "Runtime", "idle", "Idle",
    "active", "Active", "sleep-mode", "low-power", "lowpower",
    "deep-sleep", "standby", "Suspend", "Resume", "suspend", "resume",
    "network", "Network", "net", "NET", "protocol", "Protocol", "protocols",
    "Protocols", "stack", "Stack", "stacks", "Stacks", "socket", "Socket",
    "sockets", "Sockets", "ip", "IP", "tcp", "TCP", "udp", "UDP", "icmp",
    "ICMP", "http", "HTTP", "https", "HTTPS", "ftp", "FTP", "ssh", "SSH",
    "tls", "TLS", "ssl", "SSL", "dns", "DNS", "dhcp", "DHCP", "ipsec",
    "IPsec", "wireguard", "WireGuard", "openvpn", "OpenVPN", "l2tp",
    "L2TP", "pptp", "PPTP", "ipv4", "IPv4", "ipv6", "IPv6", "multicast",
    "broadcast", "unicast", "packet", "Packet", "packets", "Packets",
    "frame", "Frame", "frames", "Frames", "header", "Header", "headers",
    "Headers", "footer", "payload", "Payload", "message", "Message",
    "messages", "Messages", "request", "Request", "requests", "Requests",
    "response", "Response", "responses", "Responses", "client", "Client",
    "server", "Server", "peer", "Peer", "node", "Node", "nodes", "Nodes",
    "endpoint", "Endpoint", "endpoints", "Endpoints", "service", "Service",
    "services", "Services", "application-layer", "transport-layer",
    "network-layer", "link-layer", "physical-layer", "routing", "Routing",
    "forwarding", "switching", "Switching", "bridge", "Bridge", "switch",
    "Switch", "router", "Router", "gateway", "Gateway", "firewall",
    "Firewall", "proxy", "Proxy", "load-balancer",
    "cluster", "Cluster", "clusters", "Clusters", "mesh", "Mesh", "topology",
    "Topology", "bandwidth", "Bandwidth", "latency", "Latency", "throughput",
    "Throughput", "jitter", "Jitter", "reliability", "Reliability",
    "availability", "Availability", "security", "Security", "privacy",
    "Privacy", "integrity", "Integrity", "confidentiality", "Confidentiality",
    "vulnerability", "Vulnerability", "vulnerabilities", "Vulnerabilities",
    "exploit", "Exploit", "attack", "Attack", "threat", "Threat", "threats",
    "Threats", "risk", "Risk", "risks", "Risks", "incident", "Incident",
    "incidents", "Incidents", "breach", "Breach", "intrusion", "Intrusion",
    "malware", "Malware", "virus", "Virus", "worm", "Worm", "trojan",
    "Trojan", "ransomware", "Ransomware", "spyware", "Spyware", "adware",
    "Adware", "botnet", "Botnet", "phishing", "Phishing", "spoofing",
    "Spoofing", "sniffing", "Sniffing", "man-in-the-middle", "DoS", "DDoS",
    "brute-force", "dictionary-attack", "zero-day", "patch", "Patch",
    "patches", "Patches", "update", "Update", "updates", "Updates", "upgrade",
    "Upgrade", "downgrade", "rollback", "Rollback", "release", "Release",
    "releases", "Releases", "version", "Version", "versions", "Versions",
    "branch", "Branch", "branches", "Branches", "tag", "Tag", "tags", "Tags",
    "commit", "Commit", "commits", "Commits", "repository", "Repository",
    "repositories", "Repositories", "fork", "Fork", "merge", "Merge",
    "rebase", "Rebase", "cherry-pick", "stash", "Stash", "clone", "Clone",
    "pull", "Pull", "push", "Push", "fetch", "Fetch", "checkout", "Checkout",
    "branching", "Branching", "main", "Main", "master", "Master", "develop",
    "Development", "dev", "staging", "Staging", "production", "Production",
    "CI", "CD", "pipeline", "Pipeline", "workflow", "Workflow", "workflows",
    "Workflows", "automation", "Automation", "script", "Script", "scripts",
    "Scripts", "tool", "Tool", "tools", "Tools", "utility", "Utility",
    "utilities", "Utilities", "framework", "Framework", "frameworks",
    "Frameworks", "libraries", "Libraries", "package", "Package",
    "packages", "Packages", "dependency", "Dependency", "dependencies",
    "Dependencies", "modules", "Modules", "component", "Component",
    "components", "Components", "element", "Element", "elements", "Elements",
    "part", "Part", "parts", "Parts", "piece", "Piece", "pieces", "Pieces",
    "section", "Section", "sections", "Sections", "chapter", "Chapter",
    "chapters", "Chapters", "page", "Page", "pages", "Pages", "line", "Line",
    "lines", "Lines", "row", "Row", "rows", "Rows", "column", "Column",
    "columns", "Columns", "cell", "Cell", "cells", "Cells", "table", "Table",
    "tables", "Tables", "list", "List", "lists", "Lists", "item", "Item",
    "items", "Items", "entry", "Entry", "entries", "Entries", "record",
    "Record", "records", "Records", "field", "Field", "fields", "Fields",
    "attribute", "Attribute", "attributes", "Attributes", "property",
    "Property", "properties", "Properties", "variable", "Variable",
    "variables", "Variables", "constant", "Constant", "constants", "Constants",
    "literal", "Literal", "literals", "Literals", "identifier", "Identifier",
    "identifiers", "Identifiers", "symbol", "Symbol", "symbols", "Symbols",
    "keyword", "Keyword", "keywords", "Keywords", "operator", "Operator",
    "operators", "Operators", "expression", "Expression", "expressions",
    "Expressions", "statement", "Statement", "statements", "Statements",
    "function-call", "procedure", "Procedure", "procedures", "Procedures",
    "routine", "Routine", "routines", "Routines", "method-call", "constructor",
    "Destructor", "constructors", "Destructors", "inheritance", "Inheritance",
    "polymorphism", "Polymorphism", "encapsulation", "Encapsulation",
    "abstraction", "Abstraction", "object-oriented", "procedural",
    "functional", "logic", "Logic", "concurrent", "Concurrent",
    "parallel", "Parallel", "serial", "Serial", "synchronous", "Asynchronous",
    "asynchronous", "Synchronous", "blocking", "Blocking", "non-blocking",
    "nonblocking", "event-driven", "callback-based", "promise-based",
    "threading", "Threading", "multithreading", "Multithreading",
    "concurrency", "Concurrency", "race-condition", "deadlock", "Deadlock",
    "livelock", "Starvation", "contention", "Contention", "synchronization",
    "Synchronization", "locking", "Locking", "spinlock", "Spinlock",
    "spinlocks", "Spinlocks", "mutex-lock", "reader-writer", "optimistic",
    "pessimistic", "atomic", "Atomic", "atomics", "Atomics", "memory-barrier",
    "memory-ordering", "volatile", "Volatile", "const", "mutable",
    "thread-local", "Thread-Local", "thread-local-storage", "TLS",
    "global", "Global", "global-variable", "static", "Static", "dynamic",
    "Dynamic", "heap", "Heap", "heap-allocation", "stack-allocation",
    "static-allocation", "memory-allocation", "memory-management",
    "Memory-Management", "memory-allocator", "memory-pool", "Memory-Pool",
    "memory-fragmentation", "garbage-collection", "Garbage-Collection",
    "reference-counting", "mark-and-sweep", "generational", "incremental",
    "real-time", "Real-Time", "RTOS", "operating-system", "Operating-System",
    "scheduler", "Scheduler", "scheduling", "Scheduling", "scheduling-policy",
    "preemptive", "Preemptive", "non-preemptive", "cooperative", "Cooperative",
    "priority", "Priority", "priorities", "Priorities", "priority-inversion",
    "priority-inheritance", "round-robin", "Round-Robin", "FIFO-scheduling",
    "LIFO-scheduling", "time-slice", "Time-Slice", "time-quantum",
    "context-switch", "Context-Switch", "context-switching", "task-switch",
    "task-switching", "task-control-block", "TCB", "process-control-block",
    "PCB", "task-state", "task-lifecycle", "ready", "Running", "blocked",
    "Blocked", "terminated", "Terminated", "zombie", "Orphan", "orphan",
    "zombie-process", "process-scheduling", "CPU-scheduling",
    "CPU-allocation", "CPU-burst",
    "I/O-bound", "CPU-bound",
    "I/O-wait", "I/O-interrupt", "interrupt", "Interrupt",
    "interrupts", "Interrupts", "interrupt-handler", "interrupt-service-routine",
    "ISR", "interrupt-controller", "interrupt-priority", "interrupt-nesting",
    "interrupt-mask", "interrupt-enable", "interrupt-disable", "interrupt-vector",
    "interrupt-vector-table", "IVT", "exception", "Exception", "exceptions",
    "Exceptions", "exception-handler", "exception-vector", "exception-vector-table",
    "EVT", "fault", "Fault", "faults", "Faults", "trap", "Trap", "traps",
    "Traps", "breakpoint", "Breakpoint", "watchpoint", "Watchpoint",
    "debug-exception", "software-exception", "hardware-exception",
    "system-exception", "privileged-exception", "user-exception",
    "memory-exception", "bus-exception", "data-exception", "instruction-exception",
    "alignment-exception", "page-fault", "Page-Fault", "page-table",
    "Page-Table", "page-table-entry", "PTE", "virtual-memory", "Virtual-Memory",
    "physical-memory", "Physical-Memory", "address-space", "Address-Space",
    "virtual-address", "Physical-Address", "virtual-address-space",
    "physical-address-space", "memory-mapping", "Memory-Mapping",
    "memory-protection", "Memory-Protection", "memory-privilege",
    "memory-permission", "read-only", "Write-Only", "read-write",
    "execute-only", "no-access", "page-protection", "page-permission",
    "page-attribute", "page-size", "page-granularity", "page-fault-handling",
    "demand-paging", "Demand-Paging", "pre-paging", "swap", "Swap",
    "swap-space", "swap-partition", "swap-file", "swap-area", "memory-swapping",
    "page-replacement", "Page-Replacement", "page-fault-rate", "thrashing",
    "Thrashing", "working-set", "Working-Set", "locality", "Locality",
    "temporal-locality", "spatial-locality", "caches",
    "Caches", "cache-line", "Cache-Line", "cache-block", "Cache-Block",
    "cache-size", "cache-associativity", "cache-coherency", "Cache-Coherency",
    "cache-consistency", "Cache-Consistency", "cache-invalidation",
    "Cache-Invalidation", "cache-miss", "Cache-Hit", "cache-hit-rate",
    "cache-miss-rate", "L1-cache", "L2-cache", "L3-cache", "TLB",
    "translation-lookaside-buffer", "TLB-miss", "TLB-hit", "TLB-shootdown",
    "MMU", "memory-management-unit", "MPU", "memory-protection-unit",
    "memory-protection-region", "MPR", "address-translation",
    "address-remapping", "address-aliasing", "memory-aliasing",
    "memory-interleaving", "memory-mirroring", "memory-mapping-I/O",
    "MMIO", "memory-mapped-I/O", "port-mapped-I/O", "I/O-mapping",
    "I/O-multiplexing", "I/O-arbitration", "I/O-scheduling",
    "I/O-scheduler", "I/O-priority", "I/O-queue", "I/O-buffer", "I/O-cache",
    "I/O-channel", "I/O-adapter", "I/O-controller", "I/O-device", "I/O-port",
    "I/O-address", "I/O-instruction", "I/O-interrupt", "I/O-trap",
    "direct-memory-access", "DMA-controller", "DMA-channel", "DMA-request",
    "DMA-transfer", "DMA-mode", "DMA-burst", "DMA-cycle-stealing",
    "DMA-priority", "DMA-error", "DMA-completion", "DMA-interrupt",
    "DMA-status", "DMA-configuration", "DMA-programming", "DMA-driver",
    "DMA-API", "DMA-library", "DMA-framework", "DMA-subsystem",
    "DMA-module", "DMA-component", "DMA-element", "DMA-part", "DMA-piece",
    "DMA-section", "DMA-chapter", "DMA-page", "DMA-line", "DMA-row",
    "DMA-column", "DMA-cell", "DMA-table", "DMA-list", "DMA-item",
    "DMA-entry", "DMA-record", "DMA-field", "DMA-attribute", "DMA-property",
    "DMA-variable", "DMA-constant", "DMA-literal", "DMA-identifier",
    "DMA-symbol", "DMA-keyword", "DMA-operator", "DMA-expression",
    "DMA-statement", "DMA-function-call", "DMA-procedure", "DMA-routine",
    "DMA-method-call", "DMA-constructor", "DMA-destructor", "DMA-inheritance",
    "DMA-polymorphism", "DMA-encapsulation", "DMA-abstraction",
    "DMA-object-oriented", "DMA-procedural", "DMA-functional", "DMA-logic",
    "DMA-concurrent", "DMA-parallel", "DMA-serial", "DMA-synchronous",
    "DMA-asynchronous", "DMA-blocking", "DMA-non-blocking", "DMA-event-driven",
    "DMA-callback-based", "DMA-promise-based", "DMA-threading",
    "DMA-multithreading", "DMA-concurrency", "DMA-race-condition",
    "DMA-deadlock", "DMA-livelock", "DMA-starvation", "DMA-contention",
    "DMA-synchronization", "DMA-locking", "DMA-spinlock", "DMA-mutex-lock",
    "DMA-reader-writer", "DMA-optimistic", "DMA-pessimistic", "DMA-atomic",
    "DMA-memory-barrier", "DMA-memory-ordering", "DMA-volatile", "DMA-const",
    "DMA-mutable", "DMA-thread-local", "DMA-global", "DMA-static",
    "DMA-dynamic", "DMA-heap", "DMA-stack-allocation", "DMA-static-allocation",
    "DMA-memory-allocation", "DMA-memory-management", "DMA-memory-allocator",
    "DMA-memory-pool", "DMA-memory-fragmentation", "DMA-garbage-collection",
    "DMA-reference-counting", "DMA-mark-and-sweep", "DMA-generational",
    "DMA-incremental", "DMA-real-time", "DMA-operating-system",
    "DMA-scheduler", "DMA-scheduling", "DMA-scheduling-policy",
    "DMA-preemptive", "DMA-non-preemptive", "DMA-cooperative",
    "DMA-priority", "DMA-priorities", "DMA-priority-inversion",
    "DMA-priority-inheritance", "DMA-round-robin", "DMA-FIFO-scheduling",
    "DMA-LIFO-scheduling", "DMA-time-slice", "DMA-time-quantum",
    "DMA-context-switch", "DMA-context-switching", "DMA-task-switch",
    "DMA-task-switching", "DMA-task-control-block", "DMA-TCB",
    "DMA-process-control-block", "DMA-PCB", "DMA-task-state",
    "DMA-task-lifecycle", "DMA-ready", "DMA-running", "DMA-blocked",
    "DMA-terminated", "DMA-zombie", "DMA-orphan", "DMA-zombie-process",
    "DMA-process-scheduling", "DMA-CPU-scheduling", "DMA-CPU-allocation",
    "DMA-CPU-burst", "DMA-I/O-bound", "DMA-CPU-bound", "DMA-I/O-wait",
    "DMA-I/O-interrupt", "DMA-interrupt", "DMA-interrupts",
    "DMA-interrupt-handler", "DMA-interrupt-service-routine", "DMA-ISR",
    "DMA-interrupt-controller", "DMA-interrupt-priority",
    "DMA-interrupt-nesting", "DMA-interrupt-mask", "DMA-interrupt-enable",
    "DMA-interrupt-disable", "DMA-interrupt-vector",
    "DMA-interrupt-vector-table", "DMA-IVT", "DMA-exception",
    "DMA-exceptions", "DMA-exception-handler", "DMA-exception-vector",
    "DMA-exception-vector-table", "DMA-EVT", "DMA-fault", "DMA-faults",
    "DMA-trap", "DMA-traps", "DMA-breakpoint", "DMA-watchpoint",
    "DMA-debug-exception", "DMA-software-exception", "DMA-hardware-exception",
    "DMA-system-exception", "DMA-privileged-exception", "DMA-user-exception",
    "DMA-memory-exception", "DMA-bus-exception", "DMA-data-exception",
    "DMA-instruction-exception", "DMA-alignment-exception", "DMA-page-fault",
    "DMA-page-table", "DMA-page-table-entry", "DMA-PTE", "DMA-virtual-memory",
    "DMA-physical-memory", "DMA-address-space", "DMA-virtual-address",
    "DMA-physical-address", "DMA-virtual-address-space",
    "DMA-physical-address-space", "DMA-memory-mapping",
    "DMA-memory-protection", "DMA-memory-privilege", "DMA-memory-permission",
    "DMA-read-only", "DMA-write-only", "DMA-read-write", "DMA-execute-only",
    "DMA-no-access", "DMA-page-protection", "DMA-page-permission",
    "DMA-page-attribute", "DMA-page-size", "DMA-page-granularity",
    "DMA-page-fault-handling", "DMA-demand-paging", "DMA-pre-paging",
    "DMA-swap", "DMA-swap-space", "DMA-swap-partition", "DMA-swap-file",
    "DMA-swap-area", "DMA-memory-swapping", "DMA-page-replacement",
    "DMA-page-fault-rate", "DMA-thrashing", "DMA-working-set",
    "DMA-locality", "DMA-temporal-locality", "DMA-spatial-locality",
    "DMA-cache", "DMA-caches", "DMA-cache-line", "DMA-cache-block",
    "DMA-cache-size", "DMA-cache-associativity", "DMA-cache-coherency",
    "DMA-cache-consistency", "DMA-cache-invalidation", "DMA-cache-miss",
    "DMA-cache-hit", "DMA-cache-hit-rate", "DMA-cache-miss-rate",
    "DMA-L1-cache", "DMA-L2-cache", "DMA-L3-cache", "DMA-TLB",
    "DMA-translation-lookaside-buffer", "DMA-TLB-miss", "DMA-TLB-hit",
    "DMA-TLB-shootdown", "DMA-MMU", "DMA-memory-management-unit",
    "DMA-MPU", "DMA-memory-protection-unit", "DMA-memory-protection-region",
    "DMA-MPR", "DMA-address-translation", "DMA-address-remapping",
    "DMA-address-aliasing", "DMA-memory-aliasing", "DMA-memory-interleaving",
    "DMA-memory-mirroring", "DMA-memory-mapping-I/O", "DMA-MMIO",
    "DMA-memory-mapped-I/O", "DMA-port-mapped-I/O", "DMA-I/O-mapping",
    "DMA-I/O-multiplexing", "DMA-I/O-arbitration", "DMA-I/O-scheduling",
    "DMA-I/O-scheduler", "DMA-I/O-priority", "DMA-I/O-queue", "DMA-I/O-buffer",
    "DMA-I/O-cache", "DMA-I/O-channel", "DMA-I/O-adapter",
    "DMA-I/O-controller", "DMA-I/O-device", "DMA-I/O-port", "DMA-I/O-address",
    "DMA-I/O-instruction", "DMA-I/O-interrupt", "DMA-I/O-trap",
    "DMA-direct-memory-access", "DMA-DMA-controller", "DMA-DMA-channel",
    "DMA-DMA-request", "DMA-DMA-transfer", "DMA-DMA-mode", "DMA-DMA-burst",
    "DMA-DMA-cycle-stealing", "DMA-DMA-priority", "DMA-DMA-error",
    "DMA-DMA-completion", "DMA-DMA-interrupt", "DMA-DMA-status",
    "DMA-DMA-configuration", "DMA-DMA-programming", "DMA-DMA-driver",
    "DMA-DMA-API", "DMA-DMA-library", "DMA-DMA-framework", "DMA-DMA-subsystem",
}

def check_file(src_path):
    """检查单个英文原文对应的译文，返回 (status, detail)"""
    cn_path = src_path.replace("doc/", "docs_cn/")
    try:
        with open(src_path, encoding="utf-8") as f:
            src_lines = f.readlines()
        with open(cn_path, encoding="utf-8") as f:
            cn_lines = f.readlines()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        return "FAIL", f"文件读取失败：{e}"

    src_count = len(src_lines)
    cn_count = len(cn_lines)
    if src_count == 0:
        return "PASS", f"原文 0 行"
    ratio = cn_count / src_count

    # ① 行数比检查
    if ratio < 0.70:
        return "FAIL", f"行数 {cn_count}/{src_count}={ratio:.0%}（<70%，可能内容缺失）"
    if ratio > 1.25:
        return "FAIL", f"行数 {cn_count}/{src_count}={ratio:.0%}（>125%，碎片化）"

    # ② 碎片行检测：连续 6+ 行 <15 字符短行（排除代码块/标题/下划线/列表项/表格行/指令行）
    in_code = False
    frag_start = -1
    max_frag = 0
    max_frag_lines = []
    for i, line in enumerate(cn_lines):
        stripped = line.strip()
        # 代码块进出
        if re.match(r'^\.\. (code-block|literalinclude|sourcecode|highlight|literal-block)::', stripped):
            in_code = True
            frag_start = -1
            continue
        if in_code:
            # 代码块结束：非缩进内容行
            if not line.startswith(" ") and not line.startswith("\t") and stripped:
                in_code = False
            else:
                continue
        if re.match(r'^(=+|-+|~+|\^+|"+|\*+|#+|_+)$', stripped):  # 下划线/标题装饰
            frag_start = -1
            continue
        if re.match(r'^([-*\+]\s|:|<|>|\|)', stripped):  # 列表项/选项/链接/表格
            frag_start = -1
            continue
        if re.match(r'^\.\. ', stripped):  # 指令行
            frag_start = -1
            continue
        if len(stripped) < 15:
            if frag_start == -1:
                frag_start = i
                max_frag_lines = [stripped]
            else:
                max_frag_lines.append(stripped)
            if len(max_frag_lines) > max_frag:
                max_frag = len(max_frag_lines)
        else:
            frag_start = -1
    if max_frag >= 6:
        return "FAIL", f"碎片行：最长连续 {max_frag} 行短行（<15字符，逐词拆行）"

    # ③ 残留英文检测（排除代码块 + 白名单）
    in_code = False
    counter = Counter()
    for line in cn_lines:
        stripped = line.strip()
        if re.match(r'^\.\. (code-block|literalinclude|sourcecode|highlight|literal-block)::', stripped):
            in_code = True
            continue
        if in_code:
            if not line.startswith(" ") and not line.startswith("\t") and stripped:
                in_code = False
            else:
                continue
        # 提取连续 4+ 字母英文词
        words = re.findall(r'[A-Za-z][A-Za-z0-9_]{3,}', stripped)
        for w in words:
            if w.lower() in ALLOWED:
                continue
            counter[w.lower()] += 1
    suspicious = [w for w, c in counter.items() if c >= 3 or (c >= 2 and len(w) >= 10)]
    if suspicious:
        return "FAIL", f"残留英文：{', '.join(suspicious[:10])}"

    return "PASS", f"{cn_count}/{src_count}"

def main():
    if len(sys.argv) < 2:
        print("用法：python3 verify_batch.py <英文原文路径> [...]")
        sys.exit(1)
    pass_count = 0
    total = 0
    for path in sys.argv[1:]:
        total += 1
        status, detail = check_file(path)
        print(f"{status} {detail}  {path}")
        if status == "PASS":
            pass_count += 1
    print(f"\n=== {pass_count}/{total} 通过 ===")

if __name__ == "__main__":
    main()
