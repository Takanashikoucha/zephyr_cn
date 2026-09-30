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

   以下为原文（待翻译）

      for information on approved RBGs and NIST SP 800-90B for
      information on testing a device's entropy source [th-entropy]_.

4. **Communication with the time service**. Ideally, the device shall
   contain hardware that maintains a secure time. However, most SoCs in
   use do not have support for this, and it will be necessary to consult
   an external time service.
   :rfc:`4330` and referenced RFCs describe the Simple Network Time
   Protocol that can be used to query the current time from a network time
   server.

5. **Device lifecycle**. An IoT device will have a lifecycle from
   production to destruction and disposal of the device. Aspects of this
   lifecycle that impact security include initial provisioning, normal
   operation, re-provisioning, and destruction.

   a. **Initial provisioning**. During the initial provisioning stage,
      it is necessary to program the bootloader, an initial application
      image, a device secret, and initial configuration data
      [th-initial-provision]_. In
      addition, the bootloader flash protection shall be installed. Of
      this information, only the device secret needs to differ per
      device. This secret shall be securely maintained, and destroyed in
      all locations outside of the device once it has been programmed
      [th-initial-secret]_.

   b. **Normal operation**. Normal operation includes the behavior
      described by the rest of this document.

   c. **Re-provisioning**. Sometimes it is necessary to re-provision a
      device, such as for a different application. One way to do this is
      to keep the same device secret, and replace the configuration
      data, as well as the cloud service data associated with the
      device. It is also possible to program a new device secret, but if
      this is done it shall be done securely, and the new secret
      destroyed externally once programmed into the device
      [th-reprovision]_.

   d. **Destruction**. To prevent the device secret from being used to
      spoof the device, upon decommissioning, the secret for a
      particular device shall be rendered ineffective
      [th-destruction]_. Possibilities include:

      i.    Hardware destruction of the device.

      ii.   Securely wiping the flash area containing the
            secret [3]_.

      iii.  Removing the device identity and certificate from the
            service.

Other Considerations
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
