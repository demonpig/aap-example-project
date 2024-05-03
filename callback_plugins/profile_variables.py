# (C) 2024, Max Mitschke, https://github.com/demonpig
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This plugin was heavily influenced by 'ansible.posix.profile_tasks'
# Link: https://github.com/ansible-collections/ansible.posix

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

      Use a semicolon (:) to specify multiple strings to look for in the variables name.

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

      Use a semicolon (:) to specify multiple strings to look for in the variables name.

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
    #CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        # Structure
        # [
        #     {
        #         'TASK_NAME': ''
        #         'HOSTS': [
        #             {
        #                 'HOST': ''
        #                 'VARIABLES': ''
        #             }
        #         }
        #     }
        # ]
        self.task_vars = []
        self.previous_task = None

        self.play = None

        self.record_tasks = None
        self.record_vars = None
        self.record_hosts = None

        self._ignore_vars = ('vars', 'hostvars', 'groups', 'group_names', 'omit', 'playbook_dir', 'play', 'play_hosts', 'role_names')

        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):

        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        record_tasks = self.get_option('record_tasks')
        match len(record_tasks):
            case 0:
                self.record_tasks = []
            case _:
                self.record_tasks = record_tasks.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

        record_vars = self.get_option('record_vars')
        match len(record_vars):
            case 0:
                self.record_vars = []
            case _:
                self.record_vars = record_vars.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

        record_hosts = self.get_option('record_hosts')
        match len(record_hosts):
            case 0:
                self.record_hosts = []
            case _:
                self.record_hosts = record_hosts.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

    def _record_variables(self):
        if self.record_tasks:
            checks = [True if x in self.previous_task.get_name() else False for x in self.record_tasks]
            if not all(checks):
                return

        task_obj = {
            'task_uuid': self.previous_task._uuid,
            'task_name': self.previous_task.get_name(),
            'hosts': []
        }

        # Record variables for each host right before the task is executed
        for host in self.play.get_variable_manager()._inventory.list_hosts():
            if self.record_hosts and str(host) not in self.record_hosts:
                continue

            allvars = self.play.get_variable_manager().get_vars(play=self.play, host=host, task=self.previous_task)
            for key in self.play.get_variable_manager().get_vars(play=self.play, host=host, task=self.previous_task).keys():
                # Remove some of the common variables that would be set by ansible
                # our goal here is to get the playbook variables
                if key.startswith("ansible_") or key.startswith('inventory_') or key in self._ignore_vars:
                    allvars.pop(key)

            if self.record_vars:
                common_vars = [h_var if r_var == h_var else '' for r_var in self.record_vars for h_var in allvars.keys()]
                allvars = {name:allvars.get(name) for name in common_vars if allvars.get(name)}

            task_obj['hosts'].append({'host': host, 'variables': allvars})

        if task_obj.get('hosts', []):
            self.task_vars.append(task_obj)

    def v2_playbook_on_play_start(self, play):
        # Capturing the play in order to use it to get any role variables
        # from the VariableManager
        self.play = play

        # Check to see if there extra_vars are being being specified
        # TODO: Fix this up as there is definitely a better way to do this
        #       I am simply re-using the above code as I know it works
        extra_vars = self.play.get_variable_manager().extra_vars
        if 'profile_variables_record_tasks' in extra_vars:
          record_tasks = extra_vars.get('profile_variables_record_tasks', '')
          match len(record_tasks):
              case 0:
                  self.record_tasks = []
              case _:
                  self.record_tasks = record_tasks.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

        if 'profile_variables_record_vars' in extra_vars:
          record_vars = extra_vars.get('profile_variables_record_vars', '')
          match len(record_vars):
              case 0:
                  self.record_vars = []
              case _:
                  self.record_vars = record_vars.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

        if 'profile_variables_record_hosts' in extra_vars:
            record_hosts = extra_vars.get('profile_variables_record_hosts', '')
            match len(record_hosts):
                case 0:
                    self.record_hosts = []
                case _:
                    self.record_hosts = record_hosts.strip('"').strip("'").lstrip(':').rstrip(':').split(':')

    def v2_playbook_on_task_start(self, task, is_conditional):
        if self.previous_task:
            self._record_variables()

        self.previous_task = task

    def v2_playbook_on_handler_task_start(self, task):
        if self.previous_task:
            self._record_variables()

        self.previous_task = task

    def v2_playbook_on_stats(self, stats):
        """
        Prints changes to the variables throughout the tasks
        """
        # Recording the state of variables for the last task executed
        self._record_variables()

        for task in self.task_vars:
            print(f"TASK: {task.get('task_name')} ({task.get('task_uuid')})")
            for host in task.get('hosts', []):
                print(f"HOST: {host.get('host')}")
                print(json.dumps(host.get('variables'), indent=4, default=str))
                print()
