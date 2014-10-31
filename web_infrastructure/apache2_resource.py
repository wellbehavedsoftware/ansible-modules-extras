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
module: apache2_config
version_added: 1.8
short_description: enables/disables a resource (site or module) of the Apache2 webserver
description:
   - Enables or disables a specified resource (site or module) of the Apache2 webserver.
options:
   name:
     description:
        - name of the resource (site or module) to enable/disable
     required: true
   state:
     description:
        - indicate the desired state of the resource
     choices: ['present', 'absent']
     default: present
   resource_type:
     description:
        - indicate whether the resource is a site or a module
     choices: ['module', 'site']
     default: module

'''

EXAMPLES = '''
# enables the Apache2 site "000-default.conf"
- apache2_resouerce: state=present name=000-default.conf resource_type=site

# disables the Apache2 module "wsgi"
- apache2_resource: state=absent name=wsgi resource_type=module
'''

import re

def _disable_resource(resource, resource_type):
    name = resource.params['name']
    if resource_type == "site":
        a2dissite_binary = resource.get_bin_path("a2dissite")
        result, stdout, stderr = resource.run_command("%s %s" % (a2dissite_binary, name))

        if re.match(r'.*' + name + r' already disabled.*', stdout, re.S):
            resource.exit_json(changed = False, result = "Success")
        elif result != 0:
            resource.fail_json(msg="Failed to disable site %s: %s" % (name, stdout))
        else:
            resource.exit_json(changed = True, result = "Disabled")

    elif resource_type == "module":
        a2dismod_binary = resource.get_bin_path("a2dismod")
        result, stdout, stderr = resource.run_command("%s %s" % (a2dismod_binary, name))

        if re.match(r'.*' + name + r' already disabled.*', stdout, re.S):
            resource.exit_json(changed = False, result = "Success")
        elif result != 0:
            resource.fail_json(msg="Failed to disable module %s: %s" % (name, stdout))
        else:
            resource.exit_json(changed = True, result = "Disabled")


def _enable_resource(resource, resource_type):
    name = resource.params['name']

    if resource_type == "site":
        a2ensite_binary = resource.get_bin_path("a2ensite")
        result, stdout, stderr = resource.run_command("%s %s" % (a2ensite_binary, name))

        if re.match(r'.*' + name + r' already enabled.*', stdout, re.S):
            resource.exit_json(changed = False, result = "Success")
        elif result != 0:
            resource.fail_json(msg="Failed to enable site %s: %s" % (name, stdout))
        else:
            resource.exit_json(changed = True, result = "Enabled")

    elif resource_type == "module":
        a2enmod_binary = resource.get_bin_path("a2enmod")
        result, stdout, stderr = resource.run_command("%s %s" % (a2enmod_binary, name))

        if re.match(r'.*' + name + r' already enabled.*', stdout, re.S):
            resource.exit_json(changed = False, result = "Success")
        elif result != 0:
            resource.fail_json(msg="Failed to enable module %s: %s" % (name, stdout))
        else:
            resource.exit_json(changed = True, result = "Enabled")

def main():
    resource = AnsibleModule(
        argument_spec = dict(
            name  = dict(required=True),
            state = dict(default='present', choices=['absent', 'present']),
            resource_type = dict(default='module', choices=['module', 'site'])
        ),
    )

    resource_t = resource.params['resource_type']

    if resource.params['state'] == 'present':
        _enable_resource(resource, resource_t)

    if resource.params['state'] == 'absent':
        _disable_resource(resource, resource_t)

# import module snippets
from ansible.module_utils.basic import *
main()
