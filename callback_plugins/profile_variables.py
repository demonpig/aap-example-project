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
- Ansible callback plugin used for tracking changes to variables throughout
- a playbook's execution.
requirements:
- enable in configuration - see examples section below for details.
options:
  record_tasks:
    description: |
      Capture variable data from a task or set of tasks. Values must be within the task name.

      Use a semicolon (:) to specify multiple strings to look for in the task's name.

      'profile_variables_record_tasks' must be used as an extra variable via the `-e` flag; can also
      use `-e @vars.yml` to include variables from a file.

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
    description: |
      Capture variable data for a variable or set of variables. The names must match the actual variable names.

      Use a semicolon (:) to specify multiple strings to look for in the variable's name.

      'profile_variables_record_vars' must be used as an extra variable via the `-e` flag; can also
      use `-e @vars.yml` to include variables from a file.

    default: ""
    type: string
    env:
      - name: PROFILE_VARIABLES_RECORD_VARS
    ini:
      - section: callback_profile_variables
        key: record_vars
    vars:
      - name: profile_variables_record_vars
  record_hosts:
    description: |
      Capture variable data for a host or set of hosts. The names must match the inventory_hostname.

      Use a semicolon (:) to specify multiple strings to look for in the inventory_hostname.

      'profile_variables_record_hosts' must be used as an extra variable via the `-e` flag; can also
      use `-e @vars.yml` to include variables from a file.

    default: ""
    type: string
    env:
      - name: PROFILE_VARIABLES_RECORD_HOSTS
    ini:
      - section: callback_profile_variables
        key: record_hosts
    vars:
      - name: profile_variables_record_hosts
'''

EXAMPLES = '''
example: >
To enable, add this to your ansible.cfg file in the defaults block
    [defaults]
    callbacks_enabled=profile_variables
sample output: >
    # PLAY [Test Playbook] ***************************************
    #
    # TASK [Use ansible.builtin.set_fact once] *******************
    # ok: [localhost]
    #
    # TASK [Use ansible.builtin.set_fact twice] ******************
    # ok: [localhost]
    #
    # PLAY RECAP ***********************************************
    # localhost                  : ok=2    changed=0 ...
    #
    # TASK: Use ansible.builtin.set_fact once (0271cbca-edf7-66fa-7c0d-000000000004)
    # HOST: localhost
    # {
    #     "test_var": 1
    # }
    #
    # TASK: Use ansible.builtin.set_fact twice (0271cbca-edf7-66fa-7c0d-000000000005)
    # HOST: localhost
    # {
    #     "test_var": 2,
    #     "random_var": "hello"
    # }
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