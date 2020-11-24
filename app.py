from flask import (Flask, render_template, send_file, request, jsonify, make_response, url_for)

from RepositoryClass import Repository
from dataset_generator import DatasetGenerator
from graph_generator import GraphGenerator

from firebase import Firebase
from redis import Redis
from rq import get_current_job, use_connection
import rq
from rq.job import Job
import os
from dotenv import load_dotenv
from worker import conn

load_dotenv()
app = Flask(__name__)

config = {
    "apiKey": os.environ.get("apiKey", None),
    "authDomain": os.environ.get("authDomain", None),
    "databaseURL": os.environ.get("databaseURL", None),
    "projectId": os.environ.get("projectId", None),
    "storageBucket": os.environ.get("storageBucket", None),
    "messagingSenderId": os.environ.get("messagingSenderId", None),
    "appId": os.environ.get("appId", None)
}

firebase = Firebase(config)
db = firebase.database()
queue = rq.Queue('reliability-tasks', connection=conn)

# Landing page
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/processing_status', methods=['GET'])
def processing_status():
    token = request.args.get('status_token')

    if not token:
        return make_response(
            jsonify({"message": "Token not defined"}),
            404
        )

    job = queue.fetch_job(token)
    if not job:
        erase_token(token)
        return make_response(
            jsonify({"message": "This token is not valid"}),
            404
        )

    if(job.meta.get('progress', None) == 100):
        image_url = erase_token(token)
        base_url = url_for("root", _external=True)
        return make_response(
            jsonify({
                "message": ("The issues in this repository have been "
                            "completely processed. Access the "
                            "following link to see the "
                            "resulting image."),
                "link": f'{base_url}get_image?image_url={image_url}',
            }),
            404
        )

    if(job.meta.get('progress', None) == "ERROR"):
        erase_token(token)
        return make_response(
            jsonify({
                "message": ("After applying the filters to the chosen "
                    "repository, it was not possible to select the "
                    "minimum number of bug issues necessary to perform "
                    "the non-linear regression (200 issues)"),
            }),
            409
        )

    return make_response(
        jsonify({
            "message": "This repository is still being processed",
            "status": job.meta,
        }),
        200
    )


@app.route('/get_image', methods=['GET'])
def get_image():
    image_url = request.args.get('image_url')
    if not image_url:
        return make_response(jsonify({"message": "Required image not defined"}), 404)
    return send_file(image_url, mimetype='image/png')


        
def erase_token(token):
    image_url = None
    repo_name = None
    for repo in db.child("processing_urls").get().each():
        for k, v in repo.val().items():
            if(k == 'image_url'):
                image_url = k
            if(k == 'status_token' and v == token):
                repo_name = repo.key()
        if(repo_name):
            db.child("processing_urls").child(repo_name).child('status_token').remove()
    return image_url

# @app.route('/firebase', methods=['POST'])
# def testing_firebase():
#     db.child("processing_urls").child("aspnetcore").update({"name":"Durval"})
#     return make_response(jsonify({"message": "OK"}), 200)


def get_status_token(url):
    name = get_name(url)
    data = db.child("processing_urls").child(name).get().val()
    if not data:
        return None
    return data.get('status_token', None)


@app.route('/reliability', methods=['POST'])
def reliability():
    post_data = request.get_json()

    url = clean_url(post_data['github_url'])
    image_url = fetch_image(url)

    if image_url:
        base_url = url_for("root", _external=True)
        return make_response(
            jsonify({
                "message": ("This repository already been "
                            "completely processed. Access the "
                            "following link to see the "
                            "resulting image."),
                "link": f'{base_url}get_image?image_url={image_url}',
            }),
            303
        )


    # check if this repo is already on processing queue
    status_token = get_status_token(post_data['github_url'])

    if status_token:
        base_url = url_for("root", _external=True)
        return make_response(
            jsonify({
                "message": ("This repository is already being "
                            "processed in the background, use the " 
                            "'/processing_status' route, "
                            "using the status token."
                           ),
                "link": f'{base_url}processing_status?status_token={status_token}'
            }),
            303
        )

    # add to the processing queue
    job = queue.enqueue('app.async_processing', post_data, job_timeout='1h')
    status_token = post_data['status_token'] = job.get_id()


    url = clean_url(post_data['github_url'])
    name = get_name(url)

    # saving on firebase
    db.child("processing_urls").child(name).set({
        'github_url': post_data['github_url'],
        'status_token': post_data['status_token'],
        'must_have': post_data['must_have'],
        'blocklist_labels': post_data['blocklist_labels'],
    })

    base_url = url_for("root", _external=True)
    return make_response(   
        jsonify({
            "message": ("The repository has been successfully added to "
                        "the processing queue! Check the "
                        "'/processing_status' route, using the status token."
                       ),
            "link": f'{base_url}processing_status?status_token={status_token}'
        }),
        201
    )


def get_name(url):
    return url.split('/')[-1]

def clean_url(url):
    url = url.replace('https://github.com/', '')
    if(url[-1] == '/'):
        url = url[:-1]
    return url


def fetch_image(url):
    name = get_name(url)
    data = db.child("processing_urls").child(name).get().val()
    if not data:
        return None
    return data.get('image_url', None)


def save_image(repository):
    name = get_name(repository.url)
    image_url = repository.chart_name
    db.child("processing_urls").child(name).update({"image_url": image_url})


def save_error(repository, error_message):
    name = get_name(repository.url)
    image_url = repository.chart_name
    db.child("processing_urls").child(name).update({"error": error_message})


def async_processing(post_data):
    job = get_current_job()
    
    url = post_data['github_url']
    url = clean_url(url)
    
    filters_rules = {
        'labels': {
            'must_have': post_data['must_have'],
            'blocklist_labels': post_data['blocklist_labels']
        }
    }
    
    dg = DatasetGenerator(
        token=post_data['github_token'], 
        repository=Repository(url, filters_rules), 
        loadFromFile=False
    )

    # SAVE ERROR ON DATABASE and reset progess status
    if(len(dg.filtered_issues) < 200):
        save_error(dg.repository, 
            "This repository has less than 200 issues after applying the bug filters")
        job.meta['progress'] = 'ERROR'
        job.meta['error'] = "This repository has less than 200 issues after applying the bug filters"
        job.save_meta()
        return

    gg = GraphGenerator(dg)
    gg.weibull()

    save_image(dg.repository)
    job.meta['progress'] = 100
    job.save_meta()



























if __name__ == '__main__':
    app.run()