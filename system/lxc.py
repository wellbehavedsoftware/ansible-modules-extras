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
# starts lxc-name linux container
- lxc: name=lxc-name action=start

# stops lxc-name linux container
- lxc: name=lxc-name action=stop

'''

import lxc

def _start_container(container):
    name = container.params['name']

    if name in lxc.stopped():
       lxc.start(name)
    else:
        print "UNCHANGED. Container already running."

def _stop_container(container):
    name = container.params['name']

    if name in lxc.running():
       lxc.stop(name)
    else:
        print "UNCHANGED. Container already stopped."

def _destroy_container(container):
    name = container.params['name']
    lxc.destroy(name)

def _create_container(container):
    name = container.params['name']
    config_file=container.params['config_file']
    template=container.params['template']
    backing_store=container.params['backing_store']
    template_options=container.params['template_options']

    lxc.create(name, config_file, template, backing_store, template_options)

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
    if lxc.exists(name):
        if container.params['action'] == 'start':
            _start_container(container)

        if container.params['action'] == 'stop':
            _stop_container(container)

        if container.params['action'] == 'destroy':
            _destroy_container(container)

        if container.params['action'] == 'create':
            print "The specified container already exists."
    else:
        if container.params['action'] == 'create':
            _create_container(container)
        else: 
            print "The specified container does not exist."

# import module snippets
from ansible.module_utils.basic import *
main()
