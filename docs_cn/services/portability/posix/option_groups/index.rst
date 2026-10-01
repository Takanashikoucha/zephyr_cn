POSIX 选项与选项组详情
#####################################

.. _posix_option_groups:

POSIX 选项组
===================

.. _posix_option_group_barriers:

POSIX_BARRIERS
++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_BARRIERS` 启用此选项组。

.. csv-table:: POSIX_BARRIERS
   :header: API, 支持
   :widths: 50,10

   pthread_barrier_destroy(),yes
   pthread_barrier_init(),yes
   pthread_barrier_wait(),yes
   pthread_barrierattr_destroy(),yes
   pthread_barrierattr_init(),yes

.. _posix_option_group_c_lang_jump:

POSIX_C_LANG_JUMP
+++++++++++++++++

``POSIX_C_LANG_JUMP`` 选项组包含在 ISO C 标准中。

.. note::
   当使用 Newlib、Picolibc 或符合 ISO C 标准的其他 C 库时，
   ``POSIX_C_LANG_JUMP`` 选项组被认为受到支持。

.. csv-table:: POSIX_C_LANG_JUMP
   :header: API, 支持
   :widths: 50,10

   setjmp(), yes
   longjmp(), yes

.. _posix_option_group_c_lang_math:

POSIX_C_LANG_MATH
+++++++++++++++++

``POSIX_C_LANG_MATH`` 选项组包含在 ISO C 标准中。

.. note::
   当使用 Newlib、Picolibc 或符合 ISO C 标准的其他 C 库时，
   ``POSIX_C_LANG_MATH`` 选项组被认为受到支持。

有关 ``POSIX_C_LANG_MATH`` 选项组的详情，请参考 `Subprofiling Considerations`_。

.. _posix_option_group_c_lang_support:

POSIX_C_LANG_SUPPORT
++++++++++++++++++++

POSIX_C_LANG_SUPPORT 选项组包含通用的 ISO C 库。

.. note::
   当使用 Newlib、Picolibc 或符合 ISO C 标准的其他 C 库时，
   整个 ``POSIX_C_LANG_SUPPORT`` 选项组被认为受到支持。

有关 ``POSIX_C_LANG_SUPPORT`` 选项组的详情，请参考 `Subprofiling Considerations`_。

有关使用 C 编程语言开发 Zephyr 应用的更多信息，请参考 :ref:`details<language_support>`。

.. _posix_option_group_c_lang_support_r:

POSIX_C_LANG_SUPPORT_R
++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_C_LANG_SUPPORT_R` 启用此选项组。

.. csv-table:: POSIX_C_LANG_SUPPORT_R
   :header: API, 支持
   :widths: 50,10

   asctime_r(),yes
   ctime_r(),yes
   gmtime_r(),yes
   localtime_r(),yes
   rand_r(),yes
   strerror_r(),yes
   strtok_r(),yes

.. _posix_option_group_c_lib_ext:

POSIX_C_LIB_EXT
+++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_C_LIB_EXT` 启用此选项组。

.. csv-table:: POSIX_C_LIB_EXT
   :header: API, 支持
   :widths: 50,10

   fnmatch(), yes
   getopt(), yes
   getsubopt(),
   optarg, yes
   opterr, yes
   optind, yes
   optopt, yes
   stpcpy(),
   stpncpy(),
   strcasecmp(),
   strdup(),
   strfmon(),
   strncasecmp(), yes
   strndup(),
   strnlen(), yes

.. _posix_option_group_clock_selection:

POSIX_CLOCK_SELECTION
+++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_CLOCK_SELECTION` 启用此选项组。

.. csv-table:: POSIX_CLOCK_SELECTION
   :header: API, 支持
   :widths: 50,10

   pthread_condattr_getclock(),yes
   pthread_condattr_setclock(),yes
   clock_nanosleep(),yes

.. _posix_option_group_device_io:

POSIX_DEVICE_IO
+++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_DEVICE_IO` 启用此选项组。

.. note::
   当使用 Newlib、Picolibc 或符合 ISO C 标准的其他 C 库时，
   ``POSIX_DEVICE_IO`` 选项组的 C89 部分被认为受到支持。

.. csv-table:: POSIX_DEVICE_IO
   :header: API, 支持
   :widths: 50,10

   FD_CLR(),yes
   FD_ISSET(),yes
   FD_SET(),yes
   FD_ZERO(),yes
   clearerr(),yes
   close(),yes
   fclose(),yes
   fdopen(),yes
   feof(),yes
   ferror(),yes
   fflush(),yes
   fgetc(),yes
   fgets(),yes
   fileno(),yes
   fopen(),yes
   fprintf(),yes
   fputc(),yes
   fputs(),yes
   fread(),yes
   freopen(),yes
   fscanf(),yes
   fwrite(),yes
   getc(),yes
   getchar(),yes
   gets(),yes
   open(),yes
   perror(),yes
   poll(),yes
   printf(),yes
   pread(),yes
   pselect(),yes
   putc(),yes
   putchar(),yes
   puts(),yes
   pwrite(),yes
   read(),yes
   scanf(),yes
   select(),yes
   setbuf(),yes
   setvbuf(),yes
   stderr,yes
   stdin,yes
   stdout,yes
   ungetc(),yes
   vfprintf(),yes
   vfscanf(),yes
   vprintf(),yes
   vscanf(),yes
   write(),yes

.. _posix_option_group_fd_mgmt:

POSIX_FD_MGMT
+++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_FD_MGMT` 启用此选项组。

.. csv-table:: POSIX_FD_MGMT
   :header: API, 支持
   :widths: 50,10

   dup(),
   dup2(),
   fcntl(),
   fgetpos(),
   fseek(),
   fseeko(),
   fsetpos(),
   ftell(),
   ftello(),
   ftruncate(),yes
   lseek(),
   rewind(),

.. _posix_option_group_file_locking:

POSIX_FILE_LOCKING
++++++++++++++++++

.. csv-table:: POSIX_FILE_LOCKING
   :header: API, 支持
   :widths: 50,10

   flockfile(),
   ftrylockfile(),
   funlockfile(),
   getc_unlocked(),
   getchar_unlocked(),
   putc_unlocked(),
   putchar_unlocked(),

.. _posix_option_group_file_system:

POSIX_FILE_SYSTEM
+++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_FILE_SYSTEM` 启用此选项组。

.. csv-table:: POSIX_FILE_SYSTEM
   :header: API, 支持
   :widths: 50,10

   access(),
   chdir(),
   closedir(), yes
   creat(),
   fchdir(),
   fpathconf(),
   fstat(), yes
   fstatvfs(),
   getcwd(),
   link(),
   mkdir(), yes
   mkstemp(),
   opendir(), yes
   pathconf(),
   readdir(), yes
   remove(), yes
   rename(), yes
   rewinddir(),
   rmdir(), yes
   stat(), yes
   statvfs(),
   tmpfile(),
   tmpnam(),
   truncate(),
   unlink(), yes
   utime(),

.. _posix_option_group_file_system_r:

POSIX_FILE_SYSTEM_R
+++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_FILE_SYSTEM_R` 启用此选项。

.. csv-table:: POSIX_FILE_SYSTEM_R
   :header: API, 支持
   :widths: 50,10

   readdir_r(), yes

.. _posix_option_group_mapped_files:

POSIX_MAPPED_FILES
++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MAPPED_FILES` 启用此选项组。

.. csv-table:: POSIX_MAPPED_FILES
   :header: API, 支持
   :widths: 50,10

   mmap(),yes
   msync(),yes
   munmap(),yes

.. _posix_option_group_memory_protection:

POSIX_MEMORY_PROTECTION
+++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MEMORY_PROTECTION` 启用此选项组。

.. csv-table:: POSIX_MEMORY_PROTECTION
   :header: API, 支持
   :widths: 50,10

   mprotect(), yes :ref:`†<posix_undefined_behaviour>`

.. _posix_option_group_multi_process:

POSIX_MULTI_PROCESS
+++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MULTI_PROCESS` 启用此选项组。

.. csv-table:: POSIX_MULTI_PROCESS
   :header: API, 支持
   :widths: 50,10

   _Exit(), yes
   _exit(), yes
   assert(), yes
   atexit(),:ref:`†<posix_undefined_behaviour>`
   clock(),
   execl(),:ref:`†<posix_undefined_behaviour>`
   execle(),:ref:`†<posix_undefined_behaviour>`
   execlp(),:ref:`†<posix_undefined_behaviour>`
   execv(),:ref:`†<posix_undefined_behaviour>`
   execve(),:ref:`†<posix_undefined_behaviour>`
   execvp(),:ref:`†<posix_undefined_behaviour>`
   exit(), yes
   fork(),:ref:`†<posix_undefined_behaviour>`
   getpgrp(),:ref:`†<posix_undefined_behaviour>`
   getpgid(),:ref:`†<posix_undefined_behaviour>`
   getpid(), yes :ref:`†<posix_undefined_behaviour>`
   getppid(),:ref:`†<posix_undefined_behaviour>`
   getsid(),:ref:`†<posix_undefined_behaviour>`
   setsid(),:ref:`†<posix_undefined_behaviour>`
   sleep(),yes
   times(),
   wait(),:ref:`†<posix_undefined_behaviour>`
   waitid(),:ref:`†<posix_undefined_behaviour>`
   waitpid(),:ref:`†<posix_undefined_behaviour>`

.. _posix_option_group_networking:

POSIX_NETWORKING
++++++++++++++++

函数 ``sockatmark()`` 尚不受支持，预期会失败并将 ``errno``
设置为 ``ENOSYS`` :ref:`†<posix_undefined_behaviour>`。

使用 :kconfig:option:`CONFIG_POSIX_NETWORKING` 启用此选项组。

.. csv-table:: POSIX_NETWORKING
   :header: API, 支持
   :widths: 50,10

   accept(),yes
   bind(),yes
   connect(),yes
   endhostent(),yes
   endnetent(),yes
   endprotoent(),yes
   endservent(),yes
   freeaddrinfo(),yes
   gai_strerror(),yes
   getaddrinfo(),yes
   gethostent(),yes
   gethostname(),yes
   getnameinfo(),yes
   getnetbyaddr(),yes
   getnetbyname(),yes
   getnetent(),yes
   getpeername(),yes
   getprotobyname(),yes
   getprotobynumber(),yes
   getprotoent(),yes
   getservbyname(),yes
   getservbyport(),yes
   getservent(),yes
   getsockname(),yes
   getsockopt(),yes
   htonl(),yes
   htons(),yes
   if_freenameindex(),yes
   if_indextoname(),yes
   if_nameindex(),yes
   if_nametoindex(),yes
   inet_addr(),yes
   inet_ntoa(),yes
   inet_ntop(),yes
   inet_pton(),yes
   listen(),yes
   ntohl(),yes
   ntohs(),yes
   recv(),yes
   recvfrom(),yes
   recvmsg(),yes
   send(),yes
   sendmsg(),yes
   sendto(),yes
   sethostent(),yes
   setnetent(),yes
   setprotoent(),yes
   setservent(),yes
   setsockopt(),yes
   shutdown(),yes
   socket(),yes
   sockatmark(),yes :ref:`†<posix_undefined_behaviour>`
   socketpair(),yes

.. _posix_option_group_pipe:

POSIX_PIPE
++++++++++

.. csv-table:: POSIX_PIPE
   :header: API, 支持
   :widths: 50,10

   pipe(),

.. _posix_option_group_realtime_signals:

POSIX_REALTIME_SIGNALS
++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_REALTIME_SIGNALS` 启用此选项组。

.. csv-table:: POSIX_REALTIME_SIGNALS
   :header: API, 支持
   :widths: 50,10

   sigqueue(),
   sigtimedwait(),
   sigwaitinfo(),

..
   此链接已"弃用"——主要保留在此处，以便旧链接仍然有效

.. _posix_option_reader_writer_locks:

.. _posix_option_group_rw_locks:

POSIX_RW_LOCKS
++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_RW_LOCKS` 启用此选项。

.. csv-table:: POSIX_RW_LOCKS
   :header: API, 支持
   :widths: 50,10

   pthread_rwlock_destroy(),yes
   pthread_rwlock_init(),yes
   pthread_rwlock_rdlock(),yes
   pthread_rwlock_tryrdlock(),yes
   pthread_rwlock_trywrlock(),yes
   pthread_rwlock_unlock(),yes
   pthread_rwlock_wrlock(),yes
   pthread_rwlockattr_destroy(),yes
   pthread_rwlockattr_getpshared(),yes
   pthread_rwlockattr_init(),yes
   pthread_rwlockattr_setpshared(),yes

.. _posix_option_group_semaphores:

POSIX_SEMAPHORES
++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_SEMAPHORES` 启用此选项组。

.. csv-table:: POSIX_SEMAPHORES
   :header: API, 支持
   :widths: 50,10

   sem_close(),yes
   sem_destroy(),yes
   sem_getvalue(),yes
   sem_init(),yes
   sem_open(),yes
   sem_post(),yes
   sem_trywait(),yes
   sem_unlink(),yes
   sem_wait(),yes

.. _posix_option_group_signal_jump:

POSIX_SIGNAL_JUMP
+++++++++++++++++

.. csv-table:: POSIX_SIGNAL_JUMP
   :header: API, 支持
   :widths: 50,10

   siglongjmp(),
   sigsetjmp(),

.. _posix_option_group_signals:

POSIX_SIGNALS
+++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_SIGNALS` 启用此选项组。

.. note::
   由于 Zephyr 尚不支持进程，ISO C 函数 ``abort()``、``signal()`` 和 ``raise()``，
   以及下面列出的其他 POSIX 函数，可能表现出未定义行为。POSIX 函数
   ``kill()``、``pause()``、``sigaction()``、``sigpending()``、``sigsuspend()``
   和 ``sigwait()`` 已实现，以确保符合标准的应用程序可以链接，
   但预期它们会失败，将 errno 设置为 ``ENOSYS``
   :ref:`†<posix_undefined_behaviour>`。

.. csv-table:: POSIX_SIGNALS
   :header: API, 支持
   :widths: 50,10

   abort(),yes :ref:`†<posix_undefined_behaviour>`
   alarm(),yes :ref:`†<posix_undefined_behaviour>`
   kill(),yes :ref:`†<posix_undefined_behaviour>`
   pause(),yes :ref:`†<posix_undefined_behaviour>`
   raise(),yes :ref:`†<posix_undefined_behaviour>`
   sigaction(),yes :ref:`†<posix_undefined_behaviour>`
   sigaddset(),yes
   sigdelset(),yes
   sigemptyset(),yes
   sigfillset(),yes
   sigismember(),yes
   signal(),yes :ref:`†<posix_undefined_behaviour>`
   sigpending(),yes :ref:`†<posix_undefined_behaviour>`
   sigprocmask(),yes
   sigsuspend(),yes :ref:`†<posix_undefined_behaviour>`
   sigwait(),yes :ref:`†<posix_undefined_behaviour>`
   strsignal(),yes

.. _posix_option_group_single_process:

POSIX_SINGLE_PROCESS
++++++++++++++++++++

POSIX_SINGLE_PROCESS 选项组包含面向单进程应用的服务。

使用 :kconfig:option:`CONFIG_POSIX_SINGLE_PROCESS` 启用此选项组。

.. csv-table:: POSIX_SINGLE_PROCESS
   :header: API, 支持
   :widths: 50,10

   confstr(),yes
   environ,yes
   errno,yes
   getenv(),yes
   setenv(),yes
   sysconf(),yes
   uname(),yes
   unsetenv(),yes

.. _posix_option_group_spin_locks:

POSIX_SPIN_LOCKS
++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_SPIN_LOCKS` 启用此选项组。

.. csv-table:: POSIX_SPIN_LOCKS
   :header: API, 支持
   :widths: 50,10

   pthread_spin_destroy(),yes
   pthread_spin_init(),yes
   pthread_spin_lock(),yes
   pthread_spin_trylock(),yes
   pthread_spin_unlock(),yes

.. _posix_option_group_threads_base:

POSIX_THREADS_BASE
++++++++++++++++++

此配置档（profile）的基本假设是系统由单个（隐式的）进程和多个线程组成。
因此，标准要求所有基本线程服务，与多进程相关的除外。

使用 :kconfig:option:`CONFIG_POSIX_THREADS` 启用此选项组。

.. csv-table:: POSIX_THREADS_BASE
   :header: API, 支持
   :widths: 50,10

   pthread_atfork(),yes
   pthread_attr_destroy(),yes
   pthread_attr_getdetachstate(),yes
   pthread_attr_getschedparam(),yes
   pthread_attr_init(),yes
   pthread_attr_setdetachstate(),yes
   pthread_attr_setschedparam(),yes
   pthread_barrier_destroy(),yes
   pthread_barrier_init(),yes
   pthread_barrier_wait(),yes
   pthread_barrierattr_destroy(),yes
   pthread_barrierattr_getpshared(),yes
   pthread_barrierattr_init(),yes
   pthread_barrierattr_setpshared(),yes
   pthread_cancel(),yes
   pthread_cleanup_pop(),yes
   pthread_cleanup_push(),yes
   pthread_cond_broadcast(),yes
   pthread_cond_destroy(),yes
   pthread_cond_init(),yes
   pthread_cond_signal(),yes
   pthread_cond_timedwait(),yes
   pthread_cond_wait(),yes
   pthread_condattr_destroy(),yes
   pthread_condattr_init(),yes
   pthread_create(),yes
   pthread_detach(),yes
   pthread_equal(),yes
   pthread_exit(),yes
   pthread_getspecific(),yes
   pthread_join(),yes
   pthread_key_create(),yes
   pthread_key_delete(),yes
   pthread_kill(),
   pthread_mutex_destroy(),yes
   pthread_mutex_init(),yes
   pthread_mutex_lock(),yes
   pthread_mutex_trylock(),yes
   pthread_mutex_unlock(),yes
   pthread_mutexattr_destroy(),yes
   pthread_mutexattr_init(),yes
   pthread_once(),yes
   pthread_self(),yes
   pthread_setcancelstate(),yes
   pthread_setcanceltype(),yes
   pthread_setspecific(),yes
   pthread_sigmask(),yes
   pthread_testcancel(),yes
   sched_yield(),yes

.. _posix_option_group_posix_threads_ext:

POSIX_THREADS_EXT
+++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREADS_EXT` 启用此选项组。

.. csv-table:: POSIX_THREADS_EXT
   :header: API, 支持
   :widths: 50,10

   pthread_attr_getguardsize(),yes
   pthread_attr_setguardsize(),yes
   pthread_mutexattr_gettype(),yes
   pthread_mutexattr_settype(),yes

.. _posix_option_group_timers:

POSIX_TIMERS
++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_TIMERS` 启用此选项组。

.. csv-table:: POSIX_TIMERS
   :header: API, 支持
   :widths: 50,10

   clock_getres(),yes
   clock_gettime(),yes
   clock_settime(),yes
   nanosleep(),yes
   timer_create(),yes
   timer_delete(),yes
   timer_gettime(),yes
   timer_getoverrun(),yes
   timer_settime(),yes

.. _posix_option_group_xsi_realtime:

XSI_REALTIME
++++++++++++

``XSI_REALTIME`` 选项组表示已启用
:ref:`_POSIX_FSYNC<posix_option_fsync>`、
:ref:`_POSIX_MEMLOCK<posix_option_memlock>`、
:ref:`_POSIX_MEMLOCK_RANGE<posix_option_memlock_range>`、
:ref:`_POSIX_MESSAGE_PASSING<posix_option_message_passing>`、
:ref:`_POSIX_PRIORITY_SCHEDULING<posix_option_priority_scheduling>`、
:ref:`_POSIX_SHARED_MEMORY_OBJECTS<posix_option_shared_memory_objects>` 和
:ref:`_POSIX_SYNCHRONIZED_IO<posix_option_synchronized_io>` 选项。

使用 :kconfig:option:`CONFIG_XSI_REALTIME` 启用此选项组。

启用此选项组时，``_XOPEN_REALTIME`` 特性测试宏将被定义为一个非 -1 的值。

.. _posix_option_group_xsi_single_process:

XSI_SINGLE_PROCESS
++++++++++++++++++

使用 :kconfig:option:`CONFIG_XSI_SINGLE_PROCESS` 启用此选项组。

.. csv-table:: XSI_SINGLE_PROCESS
   :header: API, 支持
   :widths: 50,10

   gethostid(),yes
   gettimeofday(),yes
   putenv(),yes

.. _posix_option_group_xsi_system_logging:

XSI_SYSTEM_LOGGING
++++++++++++++++++

使用 :kconfig:option:`CONFIG_XSI_SYSTEM_LOGGING` 启用此选项组。

.. csv-table:: XSI_SYSTEM_LOGGING
   :header: API, 支持
   :widths: 50,10

   closelog(),yes
   openlog(),yes
   setlogmask(),yes
   syslog(),yes

.. _posix_option_group_xsi_threads_ext:

XSI_THREADS_EXT
+++++++++++++++

XSI_THREADS_EXT 选项组是必需的，因为它提供了控制线程栈的函数。
这对任何实时应用都被认为是有用的。

使用 :kconfig:option:`CONFIG_XSI_THREADS_EXT` 启用此选项组。

.. csv-table:: XSI_THREADS_EXT
   :header: API, 支持
   :widths: 50,10

   pthread_attr_getstack(),yes
   pthread_attr_setstack(),yes
   pthread_getconcurrency(),yes
   pthread_setconcurrency(),yes

.. _posix_options:

POSIX 选项
=============

.. _posix_option_asynchronous_io:

_POSIX_ASYNCHRONOUS_IO
++++++++++++++++++++++

``_POSIX_ASYNCHRONOUS_IO`` 选项的一部分函数未在 Zephyr 中实现，
但已提供，以便符合标准的应用程序仍然可以链接。
这些函数将失败，将 ``errno`` 设置为 ``ENOSYS``:ref:`†<posix_undefined_behaviour>`。

使用 :kconfig:option:`CONFIG_POSIX_ASYNCHRONOUS_IO` 启用此选项。

.. csv-table:: _POSIX_ASYNCHRONOUS_IO
   :header: API, 支持
   :widths: 50,10

   aio_cancel(),yes :ref:`†<posix_undefined_behaviour>`
   aio_error(),yes :ref:`†<posix_undefined_behaviour>`
   aio_fsync(),yes :ref:`†<posix_undefined_behaviour>`
   aio_read(),yes :ref:`†<posix_undefined_behaviour>`
   aio_return(),yes :ref:`†<posix_undefined_behaviour>`
   aio_suspend(),yes :ref:`†<posix_undefined_behaviour>`
   aio_write(),yes :ref:`†<posix_undefined_behaviour>`
   lio_listio(),yes :ref:`†<posix_undefined_behaviour>`

.. _posix_option_cputime:

_POSIX_CPUTIME
++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_CPUTIME` 启用此选项。

.. csv-table:: _POSIX_CPUTIME
   :header: API, 支持
   :widths: 50,10

   CLOCK_PROCESS_CPUTIME_ID,yes

.. _posix_option_fsync:

_POSIX_FSYNC
++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_FSYNC` 启用此选项。

.. csv-table:: _POSIX_FSYNC
   :header: API, 支持
   :widths: 50,10

   fsync(),yes

.. _posix_option_ipv6:

_POSIX_IPV6
+++++++++++

支持 Internet Protocol Version 6（IPv6）。

更多信息请参考 :ref:`Networking <networking>`。

使用 :kconfig:option:`CONFIG_POSIX_IPV6` 启用此选项。

.. _posix_option_memlock:

_POSIX_MEMLOCK
++++++++++++++

Zephyr 的 :ref:`Demand Paging API <memory_management_api_demand_paging>`
尚不支持锁定或解锁所有虚拟内存区域。
下面的函数预期会失败并将 ``errno`` 设置为 ``ENOSYS``
:ref:`†<posix_undefined_behaviour>`。

使用 :kconfig:option:`CONFIG_POSIX_MEMLOCK` 启用此选项。

.. csv-table:: _POSIX_MEMLOCK
   :header: API, 支持
   :widths: 50,10

   mlockall(), yes
   munlockall(), yes

.. _posix_option_memlock_range:

_POSIX_MEMLOCK_RANGE
++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MEMLOCK_RANGE` 启用此选项。

.. csv-table:: _POSIX_MEMLOCK_RANGE
   :header: API, 支持
   :widths: 50,10

   mlock(), yes
   munlock(), yes

.. _posix_option_message_passing:

_POSIX_MESSAGE_PASSING
++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MESSAGE_PASSING` 启用此选项。

.. csv-table:: _POSIX_MESSAGE_PASSING
   :header: API, 支持
   :widths: 50,10

   mq_close(),yes
   mq_getattr(),yes
   mq_notify(),yes
   mq_open(),yes
   mq_receive(),yes
   mq_send(),yes
   mq_setattr(),yes
   mq_unlink(),yes

.. _posix_option_monotonic_clock:

_POSIX_MONOTONIC_CLOCK
++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_MONOTONIC_CLOCK` 启用此选项。

.. csv-table:: _POSIX_MONOTONIC_CLOCK
   :header: API, 支持
   :widths: 50,10

   CLOCK_MONOTONIC,yes

.. _posix_option_priority_scheduling:

_POSIX_PRIORITY_SCHEDULING
++++++++++++++++++++++++++

由于 Zephyr 尚不支持进程，函数 ``sched_rr_get_interval()``、
``sched_setparam()`` 和 ``sched_setscheduler()``
预期会失败并将 ``errno`` 设置为 ``ENOSYS``:ref:`†<posix_undefined_behaviour>`。

使用 :kconfig:option:`CONFIG_POSIX_PRIORITY_SCHEDULING` 启用此选项。

.. csv-table:: _POSIX_PRIORITY_SCHEDULING
   :header: API, 支持
   :widths: 50,10

   sched_get_priority_max(),yes
   sched_get_priority_min(),yes
   sched_getparam(),yes
   sched_getscheduler(),yes
   sched_rr_get_interval(),yes :ref:`†<posix_undefined_behaviour>`
   sched_setparam(),yes :ref:`†<posix_undefined_behaviour>`
   sched_setscheduler(),yes :ref:`†<posix_undefined_behaviour>`

.. _posix_option_raw_sockets:

_POSIX_RAW_SOCKETS
++++++++++++++++++

支持原始套接字（raw sockets）。

更多信息请参考 :kconfig:option:`CONFIG_NET_SOCKETS_PACKET`。

使用 :kconfig:option:`CONFIG_POSIX_RAW_SOCKETS` 启用此选项。

.. _posix_shared_memory_objects:

.. _posix_option_shared_memory_objects:

_POSIX_SHARED_MEMORY_OBJECTS
++++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_SHARED_MEMORY_OBJECTS` 启用此选项。

.. csv-table:: _POSIX_SHARED_MEMORY_OBJECTS
   :header: API, 支持
   :widths: 50,10

   mmap(), yes
   munmap(), yes
   shm_open(), yes
   shm_unlink(), yes

.. _posix_option_synchronized_io:

_POSIX_SYNCHRONIZED_IO
++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_SYNCHRONIZED_IO` 启用此选项。

.. csv-table:: _POSIX_SYNCHRONIZED_IO
   :header: API, 支持
   :widths: 50,10

   fdatasync(),yes
   fsync(),yes
   msync(),yes

.. _posix_option_thread_attr_stackaddr:

_POSIX_THREAD_ATTR_STACKADDR
++++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_ATTR_STACKADDR` 启用此选项。

.. csv-table:: _POSIX_THREAD_ATTR_STACKADDR
   :header: API, 支持
   :widths: 50,10

   pthread_attr_getstackaddr(),yes
   pthread_attr_setstackaddr(),yes

.. _posix_option_thread_attr_stacksize:

_POSIX_THREAD_ATTR_STACKSIZE
++++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_ATTR_STACKSIZE` 启用此选项。

.. csv-table:: _POSIX_THREAD_ATTR_STACKSIZE
   :header: API, 支持
   :widths: 50,10

   pthread_attr_getstacksize(),yes
   pthread_attr_setstacksize(),yes

.. _posix_option_thread_cputime:

_POSIX_THREAD_CPUTIME
+++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_CPUTIME` 启用此选项。

.. csv-table:: _POSIX_THREAD_CPUTIME
   :header: API, 支持
   :widths: 50,10

   CLOCK_THREAD_CPUTIME_ID,yes
   pthread_getcpuclockid(),yes

.. _posix_option_thread_prio_inherit:

_POSIX_THREAD_PRIO_INHERIT
++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_PRIO_INHERIT` 启用此选项。

.. csv-table:: _POSIX_THREAD_PRIO_INHERIT
   :header: API, 支持
   :widths: 50,10

   pthread_mutexattr_getprotocol(),yes
   pthread_mutexattr_setprotocol(),yes

.. _posix_option_thread_prio_protect:

_POSIX_THREAD_PRIO_PROTECT
++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_PRIO_PROTECT` 启用此选项。

.. csv-table:: _POSIX_THREAD_PRIO_PROTECT
   :header: API, 支持
   :widths: 50,10

   pthread_mutex_getprioceiling(),yes
   pthread_mutex_setprioceiling(),yes
   pthread_mutexattr_getprioceiling(),yes
   pthread_mutexattr_getprotocol(),yes
   pthread_mutexattr_setprioceiling(),yes
   pthread_mutexattr_setprotocol(),yes

.. _posix_option_thread_priority_scheduling:

_POSIX_THREAD_PRIORITY_SCHEDULING
+++++++++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_PRIORITY_SCHEDULING` 启用此选项。

.. csv-table:: _POSIX_THREAD_PRIORITY_SCHEDULING
   :header: API, 支持
   :widths: 50,10

   pthread_attr_getinheritsched(),yes
   pthread_attr_getschedpolicy(),yes
   pthread_attr_getscope(),yes
   pthread_attr_setinheritsched(),yes
   pthread_attr_setschedpolicy(),yes
   pthread_attr_setscope(),yes
   pthread_getschedparam(),yes
   pthread_setschedparam(),yes
   pthread_setschedprio(),yes

.. _posix_option_thread_safe_functions:

_POSIX_THREAD_SAFE_FUNCTIONS
++++++++++++++++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_THREAD_SAFE_FUNCTIONS` 启用此选项。

.. csv-table:: _POSIX_THREAD_SAFE_FUNCTIONS
    :header: API, 支持
    :widths: 50,10

    asctime_r(), yes
    ctime_r(), yes (UTC timezone only)
    flockfile(),
    ftrylockfile(),
    funlockfile(),
    getc_unlocked(),
    getchar_unlocked(),
    getgrgid_r(),yes :ref:`†<posix_undefined_behaviour>`
    getgrnam_r(),yes :ref:`†<posix_undefined_behaviour>`
    getpwnam_r(),yes :ref:`†<posix_undefined_behaviour>`
    getpwuid_r(),yes :ref:`†<posix_undefined_behaviour>`
    gmtime_r(), yes
    localtime_r(), yes (UTC timezone only)
    putc_unlocked(),
    putchar_unlocked(),
    rand_r(), yes
    readdir_r(), yes
    strerror_r(), yes
    strtok_r(), yes

.. _posix_option_timeouts:

_POSIX_TIMEOUTS
+++++++++++++++

使用 :kconfig:option:`CONFIG_POSIX_TIMEOUTS` 启用此选项。

.. csv-table:: _POSIX_TIMEOUTS
   :header: API, 支持
   :widths: 50,10

   mq_timedreceive(),yes
   mq_timedsend(),yes
   pthread_mutex_timedlock(),yes
   pthread_rwlock_timedrdlock(),yes
   pthread_rwlock_timedwrlock(),yes
   sem_timedwait(),yes
   posix_trace_timedgetnext_event(),

.. _posix_option_xopen_streams:

_XOPEN_STREAMS
++++++++++++++

除 ``ioctl()`` 外，``_XOPEN_STREAMS`` 选项组中的函数
未在 Zephyr 中实现，但已提供，以便符合标准的应用程序仍然可以链接。
此选项组中未实现的函数将失败，将 ``errno`` 设置为 ``ENOSYS``
:ref:`†<posix_undefined_behaviour>`。

使用 :kconfig:option:`CONFIG_XSI_STREAMS` 启用此选项。

.. csv-table:: _XOPEN_STREAMS
   :header: API, 支持
   :widths: 50,10

   fattach(), yes :ref:`†<posix_undefined_behaviour>`
   fdetach(), yes :ref:`†<posix_undefined_behaviour>`
   getmsg(), yes :ref:`†<posix_undefined_behaviour>`
   getpmsg(), yes :ref:`†<posix_undefined_behaviour>`
   ioctl(), yes
   isastream(), yes :ref:`†<posix_undefined_behaviour>`
   putmsg(), yes :ref:`†<posix_undefined_behaviour>`
   putpmsg(), yes :ref:`†<posix_undefined_behaviour>`

.. _Subprofiling Considerations:
   https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_subprofiles.html
