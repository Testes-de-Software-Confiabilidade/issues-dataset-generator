# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_render_template]
import datetime
from flask import (Flask, render_template, send_file, request, jsonify, make_response)

from RepositoryClass import Repository
from dataset_generator import DatasetGenerator
from graph_generator import GraphGenerator


app = Flask(__name__)


@app.route('/')
def root():
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    # TODO: get data -> /reliability
    # get_data()

    return render_template('index.html', times=dummy_times)



# TODO: async task
# def process_reliability():
    
@app.route('/reliability', methods=['POST'])
def reliability():

    post_data = request.get_json()

    print('\n')
    print('post_data', post_data)
    print('\n')

    url = post_data['github_url'].replace('https://github.com/', '')
    if(url[-1] == '/'):
        url = url[:-1]

    already_processed = False
    if url in ('spring-projects/spring-framework', 'angular/angular.js', 
        'angular/angular', 'dotnet/aspnetcore'):
        already_processed = True
    
    filters_rules = {
        'labels': {
            'must_have': post_data['must_have'],
            'blocklist_labels': post_data['blocklist_labels']
        }
    }

    r = Repository(url, filters_rules)
    
    dg = DatasetGenerator(
        token=post_data['github_token'], 
        repository=r, 
        loadFromFile=already_processed
    )

    if(len(dg.filtered_issues) < 200):
        return make_response(
            jsonify({"message": "This repository has less than 200 issues after applying the bug filters"}),
            400,
        )

    gg = GraphGenerator(dg)

    gg.weibull()

    return send_file(r.chart_name, mimetype='image/png')




























if __name__ == '__main__':
    app.run()
