.. _smf:

State
Machine
Framework
#######################

.. highlight::
   c

Overview
========

State
Machine
Framework
（SMF）
是
一
个
application
agnostic
的
framework
它
provide
一
个
easy
的
way
用于
developers
integrate
state
machines
到
他们
的
application
中。
Framework
可以
被
added
到
任何
project
通过
enable
:kconfig:option:`CONFIG_SMF`
option。

State
Creation
==============

一
个
state
由
three
functions
represented
那里
一
个
function
implement
Entry
actions
另
一
个
function
implement
Run
actions
且
last
个
function
implement
Exit
actions。
Entry
和
exit
functions
的
prototype
是
``void
funct(void
*obj)``
且
run
action
的
prototype
是
``enum
smf_state_result
funct(void
*obj)``
那里
``obj``
parameter
是
一
个
user
defined
的
structure
它
有
state
machine
context
:c:struct:`smf_ctx`
作为
它
的
first
member。
例如::

   struct
   user_object
   {
      struct
   smf_ctx
   ctx;
      /*
   All
   User
   Defined
   Data
   Follows
   */
   };

:c:struct:`smf_ctx`
member
必须
是
first
的
因为
state
machine
framework
的
functions
用
:c:macro:`SMF_CTX`
macro
将
user
defined
的
object
cast
到
:c:struct:`smf_ctx`
type。

例如
而
不
是
做
``(struct
smf_ctx
*)&user_obj``
你
可以
use
``SMF_CTX(&user_obj)``。

Default
下
一
个
state
可以
没有
ancestor
states
resulting
在
flat
的
state
machine。
但
要
enable
create
一
个
hierarchical
的
state
machine
the


.. note::

    本节已整理为中文摘要，原文细节请参考上游英文文档。
.. graphviz::
   :caption: Hierarchical state machine diagram

   digraph smf_hierarchical {
      node [style = rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];
      STATE_S2 [shape = box];

      subgraph cluster_0 {
         label = "PARENT";
         style = rounded;
         STATE_S0 -> STATE_S1;
      }

      init -> STATE_S0;
      STATE_S1 -> STATE_S2;
      STATE_S2 -> STATE_S0;
   }

Code::

	#include <zephyr/smf.h>

	/* Forward declaration of state table */
	static const struct smf_state demo_states[];

	/* List of demo states */
	enum demo_state { PARENT, S0, S1, S2 };

	/* User defined object */
	struct s_object {
		/* This must be first */
		struct smf_ctx ctx;

		/* Other state specific data add here */
	} s_obj;

	/* Parent State */
	static void parent_entry(void *o)
	{
		/* Do something */
	}
	static void parent_exit(void *o)
	{
		/* Do something */
	}

	/* State S0 */
	static enum smf_state_result s0_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
		return SMF_EVENT_HANDLED;
	}

	/* State S1 */
	static enum smf_state_result s1_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S2]);
		return SMF_EVENT_HANDLED;
	}

	/* State S2 */
	static enum smf_state_result s2_run(void *o)
	{
		smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
		return SMF_EVENT_HANDLED;
	}

	/* Populate state table */
	static const struct smf_state demo_states[] = {
		/* Parent state does not have a run action */
		[PARENT] = SMF_CREATE_STATE(parent_entry, NULL, parent_exit, NULL, NULL),
		/* Child states do not have entry or exit actions */
		[S0] = SMF_CREATE_STATE(NULL, s0_run, NULL, &demo_states[PARENT], NULL),
		[S1] = SMF_CREATE_STATE(NULL, s1_run, NULL, &demo_states[PARENT], NULL),
		/* State S2 do not have entry or exit actions and no parent */
		[S2] = SMF_CREATE_STATE(NULL, s2_run, NULL, NULL, NULL),
	};

	int main(void)
	{
		int32_t ret;

		/* Set initial state */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Run the state machine */
		while(1) {
			/* State machine terminates if a non-zero value is returned */
			ret = smf_run_state(SMF_CTX(&s_obj));
			if (ret) {
				/* handle return code and terminate state machine */
				break;
			}
			k_msleep(1000);
		}
	}

When designing hierarchical state machines, the following should be considered:

- Ancestor entry actions are executed before the sibling entry actions. For
  example, the parent_entry function is called before the s0_entry function.
- Transitioning from one sibling to another with a shared ancestry does not
  re-execute the ancestor\'s entry action or execute the exit action.
  For example, the parent_entry function is not called when transitioning
  from S0 to S1, nor is the parent_exit function called.
- Ancestor exit actions are executed after the exit action of the current
  state. For example, the s1_exit function is called before the parent_exit
  function is called.
- The parent_run function only executes if the child_run function does not
  call either :c:func:`smf_set_state` or return :c:enum:`SMF_EVENT_HANDLED`.
- Avoid malformed hierarchical state machines by ensuring the state always
  transitions to a leaf state when :kconfig:option:`CONFIG_SMF_INITIAL_TRANSITION`
  is not enabled, or when a parent state's initial state is undefined.

Event Driven State Machine Example
**********************************

Events are not explicitly part of the State Machine Framework but an event driven
state machine can be implemented using Zephyr :ref:`events`.

.. graphviz::
   :caption: Event driven state machine diagram

   digraph smf_flat {
      node [style=rounded];
      init [shape = point];
      STATE_S0 [shape = box];
      STATE_S1 [shape = box];

      init -> STATE_S0;
      STATE_S0 -> STATE_S1 [label = "BTN EVENT"];
      STATE_S1 -> STATE_S0 [label = "BTN EVENT"];
   }

Code::

	#include <zephyr/kernel.h>
	#include <zephyr/drivers/gpio.h>
	#include <zephyr/smf.h>

	#define SW0_NODE        DT_ALIAS(sw0)

	/* List of events */
	#define EVENT_BTN_PRESS BIT(0)

	static const struct gpio_dt_spec button =
		GPIO_DT_SPEC_GET_OR(SW0_NODE, gpios, {0});

	static struct gpio_callback button_cb_data;

	/* Forward declaration of state table */
	static const struct smf_state demo_states[];

	/* List of demo states */
	enum demo_state { S0, S1 };

	/* User defined object */
	struct s_object {
		/* This must be first */
		struct smf_ctx ctx;

		/* Events */
		struct k_event smf_event;
		int32_t events;

		/* Other state specific data add here */
	} s_obj;

	/* State S0 */
	static void s0_entry(void *o)
	{
		printk("STATE0\n");
	}

	static enum smf_state_result s0_run(void *o)
	{
		struct s_object *s = (struct s_object *)o;

		/* Change states on Button Press Event */
		if (s->events & EVENT_BTN_PRESS) {
			smf_set_state(SMF_CTX(&s_obj), &demo_states[S1]);
		}
		return SMF_EVENT_HANDLED;
	}

	/* State S1 */
	static void s1_entry(void *o)
	{
		printk("STATE1\n");
	}

	static enum smf_state_result s1_run(void *o)
	{
		struct s_object *s = (struct s_object *)o;

		/* Change states on Button Press Event */
		if (s->events & EVENT_BTN_PRESS) {
			smf_set_state(SMF_CTX(&s_obj), &demo_states[S0]);
		}
		return SMF_EVENT_HANDLED;
	}

	/* Populate state table */
	static const struct smf_state demo_states[] = {
		[S0] = SMF_CREATE_STATE(s0_entry, s0_run, NULL, NULL, NULL),
		[S1] = SMF_CREATE_STATE(s1_entry, s1_run, NULL, NULL, NULL),
	};

	void button_pressed(const struct device *dev,
			struct gpio_callback *cb, uint32_t pins)
	{
		/* Generate Button Press Event */
		k_event_post(&s_obj.smf_event, EVENT_BTN_PRESS);
	}

	int main(void)
	{
		int ret;

		if (!gpio_is_ready_dt(&button)) {
			printk("Error: button device %s is not ready\n",
				button.port->name);
			return;
		}

		ret = gpio_pin_configure_dt(&button, GPIO_INPUT);
		if (ret != 0) {
			printk("Error %d: failed to configure %s pin %d\n",
				ret, button.port->name, button.pin);
			return;
		}

		ret = gpio_pin_interrupt_configure_dt(&button,
			GPIO_INT_EDGE_TO_ACTIVE);
		if (ret != 0) {
			printk("Error %d: failed to configure interrupt on %s pin %d\n",
				ret, button.port->name, button.pin);
			return;
		}

		gpio_init_callback(&button_cb_data, button_pressed, BIT(button.pin));
		gpio_add_callback(button.port, &button_cb_data);

		/* Initialize the event */
		k_event_init(&s_obj.smf_event);

		/* Set initial state */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Run the state machine */
		while(1) {
			/* Block until an event is detected */
			s_obj.events = k_event_wait(&s_obj.smf_event,
					EVENT_BTN_PRESS, true, K_FOREVER);

			/* State machine terminates if a non-zero value is returned */
			ret = smf_run_state(SMF_CTX(&s_obj));
			if (ret) {
				/* handle return code and terminate state machine */
				break;
			}
		}
	}

State Machine Example With Initial Transitions And Transition To Self
*********************************************************************

:zephyr_file:`tests/lib/smf/src/test_lib_self_transition_smf.c` defines a state
machine for testing the initial transitions and transitions to self in a parent
state. The statechart for this test is below.


.. graphviz::
   :caption: Test state machine for UML State Transitions

   digraph smf_hierarchical_initial {
      compound=true;
      node [style = rounded];
      "smf_set_initial()" [shape=plaintext fontname=Courier];
      ab_init_state [shape = point];
      STATE_A [shape = box];
      STATE_B [shape = box];
      STATE_C [shape = box];
      STATE_D [shape = box];
      DC[shape=point height=0 width=0 label="" style="invis"]

      subgraph cluster_root {
         label = "ROOT";
         style = rounded;

         subgraph cluster_ab {
            label = "PARENT_AB";
            style = rounded;
            ab_init_state -> STATE_A;
            STATE_A -> STATE_B;
         }

         subgraph cluster_c {
            label = "PARENT_C";
            style = rounded;
            STATE_B -> STATE_C [ltail=cluster_ab]
         }

         STATE_C -> DC [ltail=cluster_c, dir=none];
         DC -> STATE_C [lhead=cluster_c];
         STATE_C -> STATE_D
      }

      "smf_set_initial()" -> STATE_A [lhead=cluster_ab]
   }


Test Instrumentation
====================

The SMF provides optional instrumentation hooks for observing state machine
behavior during testing. To enable them, set
:kconfig:option:`CONFIG_SMF_INSTRUMENTATION`.

When enabled, three hook callbacks can be registered on a state machine context
via :c:func:`smf_set_hooks`:

- **on_action** — called before each entry, run, or exit action executes.
- **on_transition** — called after the current state pointer is updated but
  before the new state's entry actions execute.
- **on_error** — called when an invalid operation is detected (e.g. a NULL
  transition target or a transition attempted from an exit action).

.. important:: :c:func:`smf_set_hooks` must be called **after**
   :c:func:`smf_set_initial`, because :c:func:`smf_set_initial` resets the
   hooks pointer to ``NULL``. As a consequence, entry actions executed during
   :c:func:`smf_set_initial` (i.e. the initial state's entry actions and those
   of its ancestors) will **not** be captured by the hooks.

Example::

	#include <zephyr/smf.h>

	static void on_action(struct smf_ctx *ctx,
			      const struct smf_state *state,
			      smf_action_type action_type)
	{
		/* Log or record the action */
	}

	static void on_transition(struct smf_ctx *ctx,
				  const struct smf_state *source,
				  const struct smf_state *dest)
	{
		/* Log or record the transition */
	}

	static const struct smf_hooks hooks = {
		.on_action = on_action,
		.on_transition = on_transition,
		/* .on_error = NULL — any member may be NULL */
	};

	void test_example(void)
	{
		struct s_object s_obj;

		/* Set the initial state first */
		smf_set_initial(SMF_CTX(&s_obj), &demo_states[S0]);

		/* Install hooks after init — initial entry actions are not captured */
		smf_set_hooks(SMF_CTX(&s_obj), &hooks);

		/* Run the state machine — hooks fire on every action and transition */
		while (!smf_run_state(SMF_CTX(&s_obj))) {
			/* ... */
		}
	}

When :kconfig:option:`CONFIG_SMF_INSTRUMENTATION` is not set, all
instrumentation code is compiled out and there is zero runtime overhead.

API Reference
=============

.. doxygengroup:: smf