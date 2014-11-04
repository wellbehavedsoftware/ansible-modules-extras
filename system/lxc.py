#!/usr/bin/python
#coding: utf-8 -*-

# (c) 2014, José Luis Moreno Durán <joseluis@wellbehavedsoftware.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

DOCUMENTATION = '''
---
module: lxc
version_added: 1.8
short_description: start/stops a lxc container
description:
   - Checks the action of the specified linux container and executes the specified action: start or stop.
options:
   name:
     description:
        - hostname of the container
     required: true
   action:
     description:
        - indicate the desired action of the container
     choices: ['start', 'stop', 'destroy', 'create']
     required: true
   config_file:
     description:
        - config file parameter for creating a container
     required: false
   template:
     description:
        - template used for creating a container
     required: false
   backing_store:
     description:
        - backing store parameter for creating a container
     required: false
   template_options:
     description:
        - template options for the templated used
     required: false
'''

EXAMPLES = '''
# starts empty01 linux container
- lxc: name=empty01 action=start

# stops empty01 linux container
- lxc: name=empty01 action=stop

# destroys empty01 linux container
- lxc: name=empty01 action=destroy

# creates empty01 linux container
- lxc: name=empty01 action=create template=ubuntu template_options="-r precise"

'''

import commands
import os

def _start_container(container):
    name = container.params['name']

    if "STOPPED" in commands.getoutput('sudo lxc-info -n '+name):
       os.system("sudo lxc-start -n "+name+" --daemon")
       container.exit_json(changed=True, msg="Container "+name+" started.")
    else:
        container.exit_json(changed=False, msg="Container already running.")

def _stop_container(container):
    name = container.params['name']

    if "RUNNING" in commands.getoutput('sudo lxc-info -n '+name):
       os.system("sudo lxc-stop -n "+name)
       container.exit_json(changed=True, msg="Container "+name+" stopped.")
    else:
        container.exit_json(changed=False, msg="Container already stopped.")

def _destroy_container(container):
    name = container.params['name']
    os.system("sudo lxc-destroy -n "+name)
    container.exit_json(changed=True, msg="Container "+name+" destroyed.")

def _create_container(container):
    name = container.params['name']
    config_file=container.params['config_file']
    template=container.params['template']
    backing_store=container.params['backing_store']
    template_options=container.params['template_options']

    cmd = "sudo lxc-create -n "+name
    if config_file is not None:
        cmd = cmd + " -f "+config_file
    if template is not None:
        cmd = cmd + " -t "+template
    if backing_store is not None:
        cmd = cmd + " -B "+backing_store
    if template_options is not None:
        cmd = cmd + " -- "+template_options

    os.system(cmd)
    container.exit_json(changed=True, msg="Container "+name+" created.")

def main():
    container = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
            action = dict(required=True, choices=['start', 'stop', 'create', 'destroy']),
            config_file = dict(required=False),
            template = dict(required=False),
            backing_store = dict(required=False),
            template_options = dict(required=False)
        ),
    )

    name = container.params['name']
    if "doesn't exist" not in commands.getoutput('sudo lxc-info -n '+name):
        if container.params['action'] == 'start':
            _start_container(container)

        if container.params['action'] == 'stop':
            _stop_container(container)

        if container.params['action'] == 'destroy':
            _destroy_container(container)

        if container.params['action'] == 'create':
            container.exit_json(changed=False, msg="The specified container ("+name+") already exists and can not be created again.")
    else:
        if container.params['action'] == 'create':
            _create_container(container)
        else: 
            container.exit_json(changed=False, msg="The specified container ("+name+") does not exist. Create it first.")

# import module snippets
from ansible.module_utils.basic import *
main()
