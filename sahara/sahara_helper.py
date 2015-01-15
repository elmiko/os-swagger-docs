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
import flask
from sahara.api import v10 as api_v10
from sahara.api import v11 as api_v11


def get_app():
    app = flask.Flask('sahara.api')

    @app.route('/', methods=['GET'])
    def version_list():
        context.set_ctx(None)
        return api_utils.render({
            "versions": [
                {"id": "v1.0", "status": "CURRENT"}
            ]
        })

    app.register_blueprint(api_v10.rest, url_prefix='/v1.0')
    app.register_blueprint(api_v10.rest, url_prefix='/v1.1')
    app.register_blueprint(api_v11.rest, url_prefix='/v1.1')

    return app
