.. _bluetooth_mesh_dfu:

Device
Firmware
Update
（DFU）
############################

Bluetooth
Mesh
支持
在
mesh
network
中
distribute
firmware
images。
Bluetooth
mesh
DFU
subsystem
实现
Bluetooth
Mesh
Device
Firmware
Update
Model
specification
version
1.0。

Bluetooth
Mesh
DFU
实现
firmware
images
的
distribution
mechanism
并
不
对
images
的
size、
format
或
usage
放
任何
restrictions。
Subsystem
的
primary
design
goal
是
提供
Bluetooth
Mesh
DFU
specification
的
qualifiable
parts
并
将
usage、
firmware
validation
和
deployment
留
给
application。

DFU
specification
在
Zephyr
Bluetooth
Mesh
DFU
subsystem
中
被
实现
为
三
个
separate
的
models：

.. toctree::
   :maxdepth:
   1

   dfu_srv
   dfu_cli
   dfd_srv

Overview
********

DFU
roles
=========

Bluetooth
Mesh
DFU
subsystem
定义
三
个
不同
的
roles
mesh
nodes
在
firmware
images
的
distribution
中
必须
assume：

Target
node
   Target
   node
   是
   transferred
   firmware
   images
   的
   receiver
   和
   user。
   它
   所有
   的
   functionality
   由
   :ref:`bluetooth_mesh_dfu_srv`
   model
   实现。
   一
   个
   transfer
   可能
   指向
   任何
   数量
   的
   Target
   nodes
   它们
   都
   会
   被
   concurrently
   updated。

Distributor
   Distributor
   role
   在
   DFU
   process
   中
   服务
   两
   个
   purposes。
   首先
   它
   作为
   Target


.. note::

   以下为原文（待翻译）

   URI is optional, and its max length is determined by
   :kconfig:option:`CONFIG_BT_MESH_DFU_URI_MAXLEN`.

   .. note::

      The out-of-band distribution mechanism is not supported.

.. _bluetooth_mesh_dfu_firmware_effect:

Firmware effect
---------------

A new image may have the Composition Data Page 0 different from the one allocated on a Target node.
This may have an effect on the provisioning data of the node and how the Distributor finalizes the
DFU. Depending on the availability of the Remote Provisioning Server model on the old and new image,
the device may either boot up unprovisioned after applying the new firmware or require to be
re-provisioned. The complete list of available options is defined in :c:enum:`bt_mesh_dfu_effect`:

:c:enumerator:`BT_MESH_DFU_EFFECT_NONE`
   The device stays provisioned after the new firmware is programmed. This effect is chosen if the
   composition data of the new firmware doesn't change.
:c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE_NO_RPR`
   This effect is chosen when the composition data changes and the device doesn't support the remote
   provisioning. The new composition data takes place only after re-provisioning.
:c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE`
   This effect is chosen when the composition data changes and the device supports the remote
   provisioning. In this case, the device stays provisioned and the new composition data takes place
   after re-provisioning using the Remote Provisioning models.
:c:enumerator:`BT_MESH_DFU_EFFECT_UNPROV`
  This effect is chosen if the composition data in the new firmware changes, the device does not
  support the remote provisioning, and the new composition data takes effect after applying the
  firmware. The effect can also be chosen, if it is necessary to unprovision the device for
  application-specific reasons.

When the Target node receives the Firmware Update Firmware Metadata Check message, the Firmware
Update Server model calls the :c:member:`bt_mesh_dfu_srv_cb.check` callback, the application can
then process the metadata and provide the effect value. If the effect is
:c:enumerator:`BT_MESH_DFU_EFFECT_COMP_CHANGE`, the application must call functions
:c:func:`bt_mesh_comp_change_prepare` and :c:func:`bt_mesh_models_metadata_change_prepare` to
prepare the Composition Data Page and Models Metadata Page contents before applying the new
firmware image. See :ref:`bluetooth_mesh_dfu_srv_comp_data_and_models_metadata` for more
information.


DFU procedures
**************

The DFU protocol is implemented as a set of procedures that must be performed in a certain order.

The Initiator controls the Upload stage of the DFU protocol, and all Distributor side handling of
the upload subprocedures is implemented in the :ref:`bluetooth_mesh_dfd_srv`.

The Distribution stage is controlled by the Distributor, as implemented by the
:ref:`bluetooth_mesh_dfu_cli`. The Target node implements all handling of these procedures in the
:ref:`bluetooth_mesh_dfu_srv`, and notifies the application through a set of callbacks.

.. figure:: images/dfu_stages_procedures_mesh.svg
   :align: center
   :alt: Overview of DFU stages and procedures

   DFU stages and procedures as seen from the Distributor

Uploading the firmware
======================

The Upload Firmware procedure uses the :ref:`bluetooth_mesh_blob` to transfer the firmware image
from the Initiator to the Distributor. The Upload Firmware procedure works in two steps:

1. The Initiator generates a BLOB ID, and sends it to the Distributor's Firmware Distribution Server
   along with the firmware information and other input parameters of the BLOB transfer. The Firmware
   Distribution Server stores the information, and prepares its BLOB Transfer Server for the
   incoming transfer before it responds with a status message to the Initiator.
#. The Initiator's BLOB Transfer Client model transfers the firmware image to the Distributor's BLOB
   Transfer Server, which stores the image in a predetermined flash partition.

When the BLOB transfer finishes, the firmware image is ready for distribution. The Initiator may
upload several firmware images to the Distributor, and ask it to distribute them in any order or at
any time. Additional procedures are available for querying and deleting firmware images from the
Distributor.

The following Distributor's capabilities related to firmware images can be configured using the
configuration options:

* :kconfig:option:`CONFIG_BT_MESH_DFU_SLOT_CNT`: Amount of image slots available on the device.
* :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_SLOT_MAX_SIZE`: Maximum allowed size for each image.
* :kconfig:option:`CONFIG_BT_MESH_DFD_SRV_SLOT_SPACE`: Available space for all images.

Populating the Distributor's receivers list
===========================================

Before the Distributor can start distributing the firmware image, it needs a list of Target nodes to
send the image to. The Initiator gets the full list of Target nodes either by querying the potential
targets directly, or through some external authority. The Initiator uses this information to
populate the Distributor's receivers list with the address and relevant firmware image index of each
Target node. The Initiator may send one or more Firmware Distribution Receivers Add messages to
build the Distributor's receivers list, and a Firmware Distribution Receivers Delete All message to
clear it.

The maximum number of receivers that can be added to the Distributor is configured through the
:kconfig:option:`CONFIG_BT_MESH_DFD_SRV_TARGETS_MAX` configuration option.

Initiating the distribution
===========================

Once the Distributor has stored a firmware image and received a list of Target nodes, the Initiator
may initiate the distribution procedure. The BLOB transfer parameters for the distribution are
passed to the Distributor along with an update policy. The update policy decides whether the
Distributor should request that the firmware is applied on the Target nodes or not. The Distributor
stores the transfer parameters and starts distributing the firmware image to its list of Target
nodes.

Firmware distribution
---------------------

The Distributor's Firmware Update Client model uses its BLOB Transfer Client model's broadcast
subsystem to communicate with all Target nodes. The firmware distribution is performed with the
following steps:

1. The Distributor's Firmware Update Client model generates a BLOB ID and sends it to each Target
   node's Firmware Update Server model, along with the other BLOB transfer parameters, the Target
   node firmware image index and the firmware image metadata. Each Target node performs a metadata
   check and prepares their BLOB Transfer Server model for the transfer, before sending a status
   response to the Firmware Update Client, indicating if the firmware update will have any effect on
   the Bluetooth Mesh state of the node.
#. The Distributor's BLOB Transfer Client model transfers the firmware image to all Target nodes.
#. Once the BLOB transfer has been received, the Target nodes' applications verify that the firmware
   is valid by performing checks such as signature verification or image checksums against the image
   metadata.
#. The Distributor's Firmware Update Client model queries all Target nodes to ensure that they've
   all verified the firmware image.

If the distribution procedure completed with at least one Target node reporting that the image has
been received and verified, the distribution procedure is considered successful.

.. note::
   The firmware distribution procedure only fails if *all* Target nodes are lost. It is up to the
   Initiator to request a list of failed Target nodes from the Distributor and initiate additional
   attempts to update the lost Target nodes after the current attempt is finished.

Suspending the distribution
---------------------------

The Initiator can also request the Distributor to suspend the firmware distribution. In this case,
the Distributor will stop sending any messages to Target nodes. When the firmware distribution is
resumed, the Distributor will continue sending the firmware from the last successfully transferred
block.

Applying the firmware image
===========================

If the Initiator requested it, the Distributor can initiate the Apply Firmware on Target Node
procedure on all Target nodes that successfully received and verified the firmware image. The Apply
Firmware on Target Node procedure takes no parameters, and to avoid ambiguity, it should be
performed before a new transfer is initiated. The Apply Firmware on Target Node procedure consists
of the following steps:

1. The Distributor's Firmware Update Client model instructs all Target nodes that have verified the
   firmware image to apply it. The Target nodes' Firmware Update Server models respond with a status
   message before calling their application's ``apply`` callback.
#. The Target node's application performs any preparations needed before applying the transfer, such
   as storing a snapshot of the Composition Data or clearing its configuration.
#. The Target node's application swaps the current firmware with the new image and updates its
   firmware image list with the new firmware ID.
#. The Distributor's Firmware Update Client model requests the full list of firmware images from
   each Target node, and scans through the list to make sure that the new firmware ID has replaced
   the old.

.. note::
   During the metadata check in the distribution procedure, the Target node may have reported that
   it will become unprovisioned after the firmware image is applied. In this case, the Distributor's
   Firmware Update Client model will send a request for the full firmware image list, and expect no
   response.

Cancelling the distribution
===========================

The firmware distribution can be cancelled at any time by the Initiator. In this case, the
Distributor starts the cancelling procedure by sending a cancelling message to all Target nodes. The
Distributor waits for the response from all Target nodes. Once all Target nodes have replied, or the
request has timed out, the distribution procedure is cancelled. After this the distribution
procedure can be started again from the ``Firmware distribution`` section.


API reference
*************

This section lists the types common to the Device Firmware Update mesh models.

.. doxygengroup:: bt_mesh_dfd

.. doxygengroup:: bt_mesh_dfu

.. doxygengroup:: bt_mesh_dfu_metadata
