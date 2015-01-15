# Copyright (c) 2014 Red Hat Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import json
import UserDict


def from_flask(app, version):
    '''return a Swagger from a Flask App.
   
    :param app: The Flask App object
    :param version: The version string
    :return: A populated Swagger object

    '''
    info = Info(title=app.name,
                version=version)
    paths = Paths()
    for rule in app.url_map.iter_rules():
        pathitem = PathItem()
        for method in rule.methods:
            pathitem.add_operation(method)
        paths.add(rule.rule, pathitem)
    swagger = Swagger(info, paths)
    return swagger


class Info(collections.OrderedDict):
    def __init__(self, title, version):
        super(Info, self).__init__()
        self['title'] = title
        self['version'] = version


class Operation(collections.OrderedDict):
    def __init__(self):
        super(Operation, self).__init__()


class PathItem(collections.OrderedDict):
    valid_operations = ( 'get',
                         'put',
                         'post',
                         'delete',
                         'options',
                         'head',
                         'patch')
    def __init__(self):
        super(PathItem, self).__init__()

    def add_operation(self, operation):
        if operation.lower() not in self.valid_operations:
            raise Exception('operation {} not valid'.format(operation))
        self[operation.lower()] = Operation()

class Paths(collections.OrderedDict):
    def __init__(self):
        super(Paths, self).__init__()

    def add(self, route, pathitem):
        self[route] = pathitem

class Swagger(collections.OrderedDict):
    def __init__(self, info, paths):
        super(Swagger, self).__init__()
        self['swagger'] = '2.0'
        self['info'] = info
        self['paths'] = paths
