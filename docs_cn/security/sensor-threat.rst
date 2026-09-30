.. _sensor-threat:

Sensor
Device
Threat
Model
##########################

This
document
describes
a
threat
model
for
an
IoT
sensor
device。
Spelling
out
a
threat
model
helps
direct
development
effort
and
can
be
used
to
help
prioritize
these
efforts
as
well。

This
device
contains
a
sensor
of
some
type
（for
example
temperature、
or
a
pressure
in
a
pipe）
which
sends
this
data
to
an
SoC
running
a
microcontroller。
This
microcontroller
connects
to
a
cloud
service
and
relays
this
sensor
data
to
this
service。
The
cloud
service
is
also
able
to
send
configuration
data
to
the
device
as
well
as
software
update
images。
A
general
diagram
can
be
seen
in
Figure
1:

.. figure::
   media/sensor
   model.svg

   Figure
   1.
   Sensor
   General
   Diagram

In
this
sensor
device
the
sensor
connects
with
the
SoC
via
an
SPI
bus
and
the
SoC
has
a
network
interface
that
it
uses
to
communicate
with
the
cloud
service。
The
particulars
of
these
interfaces
can
impact
the
threat
model
in
unexpected
ways
and
variants
on
this
will
need
to
be
considered
（for
example
using
a
separate
network
interface
SoC
connected
via
some
type
of
bus）。

This
model
also
focuses
on
communicating
via
the
MQTT
over
TLS
protocol
as
this
seems
to
be
in
wide
use
[1]_。

Assets
======

One
aspect
of
the
threat
model
to
consider
are
assets
involved
in
the
operation
of
the
device。
The
following
list
enumerates
the
assets
included
in
this
model:

1.
**The
bootloader**.
This
is
a
small
code/data
image
contained
in
on
device
flash
that
is
the
first
code
to
run。
In
order
to
establish
a
root
of
trust
this
image
must
be
immutable。
This
model
assumes


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
====================

In addition to the above, network connected devices generally will need
a way to configure them to connect to the network environment they are
placed in. There are numerous ways of doing this, and it is important
for these configuration methods to not circumvent the security
requirements described above.

Threats
=======

.. [th-imboot] Must boot with an immutable bootloader.

.. [th-authrepl] Application image shall only be replaced with an
   authorized image.

.. [th-timely-update]
   Application updates shall be done in a timely manner.

.. [th-atomic-update]
   Application updates shall be atomic.

.. [th-root-certs]
   TLS must have a list of trusted root certificates.

.. [th-root-check]
   TLS must verify root certificate from server is valid.

.. [th-secret-storage]
   There must be a mechanism to securely store client secrets.  The
   least amount of code necessary shall have access to these secrets.

.. [th-time]
   System must have moderately accurate notion of the current
   date/time.

.. [th-conf]
   The system must receive, and keep configuration data.

.. [th-logs]
   The system must log security-related events, and either store them
   locally, or send to a service.

.. [th-all-tls]
   All communications with the cloud service shall use TLS.

.. [th-tls-ciphers]
   TLS shall be configured to allow only generally agreed cipher
   suites (including forward secrecy).

.. [th-tls-client-auth]
   The device shall authenticate itself with the cloud provider using
   one of the methods described.

.. [th-entropy]
   The TLS layer shall use a modern, accepted cryptographic random-bit
   generator seeded by an entropy source within the SoC.

.. [th-initial-provision]
   The device shall have a per-device secret loaded before deployment.

.. [th-initial-secret]
   The initial secret shall be securely maintained, and destroyed in
   any external location as soon as the device is provisioned.

.. [th-reprovision]
   Reprovisioning a device shall be done securely.

.. [th-destruction]
   Upon decommissioning, the device secret shall be rendered
   ineffective.

Notes
=====

.. [1]
   See https://www.slideshare.net/kartben/iot-developer-survey-2018. As
   of this writing, the three major cloud IoT service providers, AWS
   IoT, Google Cloud IoT, and Microsoft Azure IoT all provide MQTT over
   TLS. Some feedback has suggested that some find difficulty with UDP
   protocols and routing issues on various networks.

.. [2]
   As new exploits are discovered, what is considered secure can
   change.
   Organizations such as https://www.ssllabs.com/ provide information on
   current ideas of how TLS must be configured to be secure.

.. [3]
   Note that merely erasing this flash area is unlikely to be
   sufficient.