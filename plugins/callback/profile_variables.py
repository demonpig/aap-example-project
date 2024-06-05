# (C) 2024, Max Mitschke, https://github.com/demonpig
# (C) 2024, Ryan Erickson, https://gitlab.com/epryan
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
name: profile_variables
type: aggregate
short_description: Track changes to variables throughout playbook run
description:
  - Ansible callback plugin used for tracking changes to variables throughout a playbook's execution.
requirements:
  - Enable in configuration - see examples section below for details.
options:
  record_hosts:
    description:
      - Capture variable data from a host or set of hosts. Values must match the hosts' `inventory_hostname`.
      - Provide either a string with entries separated by a semicolon (:) to specify multiple strings or provide a list.
      - The variable `profile_variables_record_hosts` must be used as an extra variable via the `-e` flag; can also use `-e @vars.yml` to include variables from a file.
    default: ""
    type: string
    env:
      - name: PROFILE_VARIABLES_RECORD_HOSTS
    ini:
      - section: callback_profile_variables
        key: record_hosts
    vars:
      - name: profile_variables_record_hosts
  record_tasks:
    description:
      - Capture variable data from a task or set of tasks. Values must be within the task name.
      - Provide either a string with entries separated by a semicolon (:) to specify multiple strings or provide a list.
      - The variable `profile_variables_record_tasks` must be used as an extra variable via the `-e` flag; can also use `-e @vars.yml` to include variables from a file.
    default: ""
    type: string
    env:
      - name: PROFILE_VARIABLES_RECORD_TASKS
    ini:
      - section: callback_profile_variables
        key: record_tasks
    vars:
      - name: profile_variables_record_tasks
  record_vars:
    description:
      - Capture variable data from a variable or set of variables. Values must match the variable name.
      - Provide either a string with entries separated by a semicolon (:) to specify multiple strings or provide a list.
      - The variable `profile_variables_record_vars` must be used as an extra variable via the `-e` flag; can also use `-e @vars.yml` to include variables from a file.
    default: ""
    type: string
    env:
      - name: PROFILE_VARIABLES_RECORD_VARS
    ini:
      - section: callback_profile_variables
        key: record_vars
    vars:
      - name: profile_variables_record_vars
'''

EXAMPLES = '''
ENABLE: >
  Add the following to an `ansible.cfg` file

    [defaults]
    callbacks_enabled = profile_variables

    # [callback_profile_variables]
    # record_hosts = ""
    # record_tasks = ""
    # record_vars  = ""

  Another option is to use the environment variable ANSIBLE_CALLBACK_PLUGINS

    ANSIBLE_CALLBACK_PLUGINS="profile_variables" ansible-playbook -i inventory playbook.yml

SAMPLE_COMMANDS: >

  Here are ways to utilize the different variables for the plugin

    # Passing in extra variables (must encapsulate the entire variable and its value in quotes)

    ansible-playbook -i inventory -e "profile_variables_record_vars='variable_name'"


    # Add variables to vars.yml (filename is arbitrary)

    ```
    ---
    profile_variables_record_tasks:
      - task_name
      - task with spaces
    ```

    ansible-playbook -i inventory -e @vars.yml playbook.yml


    # Use environment variables

    PROFILE_VARIABLES_RECORD_HOSTS="localhost" PROFILE_VARIABLES_RECORD_TASKS="debug" ansible-playbook -i inventory playbook.yml


SAMPLE_OUTPUT: >

  # PLAY [all] **************************************************************************************************************************
  # Parsing 'record_tasks' from string to list ...
  # record_tasks=['']
  # Parsing 'record_vars' from string to list ...
  # record_vars=['var_on_play']
  # Parsing 'record_hosts' from string to list ...
  # record_hosts=['hosta']

  # TASK [Debug 1] **********************************************************************************************************************
  # ok: [hosta] => {
  #     "msg": "hello play"
  # }
  # ok: [hostb] => {
  #     "msg": "hello play"
  # }

  # TASK [Instantiate another value] ****************************************************************************************************
  # ok: [hosta]
  # ok: [hostb]

  # TASK [Debug 2] **********************************************************************************************************************
  # ok: [hosta] => (item=var_on_play) => {
  #     "ansible_loop_var": "item",
  #     "item": "var_on_play",
  #     "var_on_play": "hello play"
  # }
  # ok: [hosta] => (item=var_set_during_play) => {
  #     "ansible_loop_var": "item",
  #     "item": "var_set_during_play",
  #     "var_set_during_play": "hello set_fact"
  # }
  # ok: [hostb] => (item=var_on_play) => {
  #     "ansible_loop_var": "item",
  #     "item": "var_on_play",
  #     "var_on_play": "hello play"
  # }
  # ok: [hostb] => (item=var_set_during_play) => {
  #     "ansible_loop_var": "item",
  #     "item": "var_set_during_play",
  #     "var_set_during_play": "hello set_fact"
  # }

  # TASK [Include Role] *****************************************************************************************************************

  # TASK [OneDebugRole : Debug In Role] *************************************************************************************************
  # ok: [hosta] => {
  #     "msg": "Consider it included!"
  # }
  # ok: [hostb] => {
  #     "msg": "Consider it included!"
  # }

  # TASK [Trigger Handler] **************************************************************************************************************
  # changed: [hosta] => {
  #     "msg": "Triggering Handler"
  # }
  # changed: [hostb] => {
  #     "msg": "Triggering Handler"
  # }

  # RUNNING HANDLER [handleit] **********************************************************************************************************
  # ok: [hosta] => {
  #     "msg": "Consider it handled"
  # }
  # ok: [hostb] => {
  #     "msg": "Consider it handled"
  # }

  # PLAY RECAP **************************************************************************************************************************
  # hosta                      : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
  # hostb                      : ok=6    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

  # [
  #     {
  #         "host": "hosta",
  #         "task": "Debug 1",
  #         "task_arguments": {
  #             "msg": "{{ var_on_play }}"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "Instantiate another value",
  #         "task_arguments": {
  #             "var_set_during_play": "hello set_fact"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "Debug 2",
  #         "task_arguments": {
  #             "var": "{{ item }}"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "Include Role",
  #         "task_arguments": {
  #             "name": "OneDebugRole"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block",
  #             "message": "Consider it included!"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "OneDebugRole : Debug In Role",
  #         "task_arguments": {
  #             "msg": "{{ message }}"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block",
  #             "message": "Consider it included!"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "Trigger Handler",
  #         "task_arguments": {
  #             "msg": "Triggering Handler"
  #         },
  #         "task_variables": {
  #             "var_on_block": "hello block"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     },
  #     {
  #         "host": "hosta",
  #         "task": "handleit",
  #         "task_arguments": {
  #             "msg": "{{ message }}"
  #         },
  #         "task_variables": {
  #             "message": "Consider it handled"
  #         },
  #         "tracked_variables": {
  #             "var_on_play": "hello play"
  #         }
  #     }
  # ]
'''

import json

from ansible.plugins.callback import CallbackBase

class CallbackModule(CallbackBase):

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'profile_variables'

    def __init__(self):
        self.record_tasks = None
        self.record_vars = None
        self.record_hosts = None

        self.output = []
        self.play = None

        super(CallbackModule, self).__init__()

    def print_out(self, s):
        self._display.display(f"{s}")

    def parse_var(self, name, val):
        retval = []

        if isinstance(val, str):
            self.print_out(f"Parsing '{name}' from string to list ...")
            if len(val) > 0:
                retval = val.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

        elif isinstance(val, list):
            self.print_out(f"Using '{name}' list as is ...")
            retval = val
        else:
            # NOTE: All variables currently "optional" in that the callback does nothing if given nothing
            self.print_out(f"Optional variable '{name}' is neither a string or a list. The profile_variables callback plugin requires variables in string or list format. Please see docs.")
            # TODO: plugin is continuing with undefined behavior at this point. It should terminate itself and not run.

        self.print_out(f"{name}={retval}")
        return retval

    def record(self, host, task):
        hostname = host.get_name()
        taskname = task.get_name()

        # If no var list or task list is specified, do not record
        if not self.record_vars and not self.record_tasks:
            return

        # If a host list is specified, only record tasks for that host
        if self.record_hosts and hostname not in self.record_hosts:
            return

        # If a task list is specified, only record tasks that pattern match
        if self.record_tasks and not any([wanted_taskname in taskname for wanted_taskname in self.record_tasks]):
            return

        allvars = self.play.get_variable_manager().get_vars(play=self.play, host=host, task=task)['vars']
        hostvars = dict(allvars['hostvars'][hostname])

        retvars = {}
        for wanted_var in self.record_vars:
            retvars[wanted_var] = allvars.get(wanted_var) or hostvars.get(wanted_var) or 'VARIABLE IS UNDEFINED'

        self.output.append({
            'host': hostname,
            'task': taskname,
            'task_arguments': task.args,
            'task_variables': task.get_vars(),
            'tracked_variables': retvars
        })

    def v2_playbook_on_play_start(self, play):
        self.play = play

        extra_vars = self.play.get_variable_manager().extra_vars

        self.record_tasks = self.parse_var(
            'record_tasks',
            extra_vars.get('profile_variables_record_tasks') or self.get_option('record_tasks')
        )

        self.record_vars = self.parse_var(
            'record_vars',
            extra_vars.get('profile_variables_record_vars') or self.get_option('record_vars')
        )

        self.record_hosts = self.parse_var(
            'record_hosts',
            extra_vars.get('profile_variables_record_hosts') or self.get_option('record_hosts')
        )

    def v2_runner_on_start(self, host, task):
        self.record(host, task)

    def v2_playbook_on_stats(self, stats):
        self.print_out(json.dumps(self.output, indent=4, default=str))