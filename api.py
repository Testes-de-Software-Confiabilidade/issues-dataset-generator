# from flask import Flask
# from flask import send_file
# from flask import request
# from flask import jsonify
# from flask import make_response

# from RepositoryClass import Repository
# from dataset_generator import DatasetGenerator
# from graph_generator import GraphGenerator

# app = Flask(__name__)
    
# # TODO: async task
# # def process_reliability():
    


# @app.route('/', methods=['POST'])
# def reliability():

#     post_data = request.get_json()

#     print('\n')
#     print('post_data', post_data)
#     print('\n')

#     url = post_data['github_url'].replace('https://github.com/', '')
#     if(url[-1] == '/'):
#         url = url[:-1]

#     already_processed = False
#     if url in ('spring-projects/spring-framework', 'angular/angular.js', 
#         'angular/angular', 'dotnet/aspnetcore'):
#         already_processed = True
    
#     # //////////////////////////////////
#     already_processed = False
#     # //////////////////////////////////

#     filters_rules = {
#         'labels': {
#             'must_have': post_data['must_have'],
#             'blocklist_labels': post_data['blocklist_labels']
#         }
#     }

#     r = Repository(url, filters_rules)
    
#     dg = DatasetGenerator(
#         token=post_data['github_token'], 
#         repository=r, 
#         loadFromFile=already_processed
#     )

#     if(len(dg.filtered_issues) < 200):
#         return make_response(
#             jsonify({"message": "This repository has less than 200 issues after applying the bug filters"}),
#             400,
#         )

#     gg = GraphGenerator(dg)

#     gg.weibull()

#     return send_file(r.chart_name, mimetype='image/png')


# if __name__ == '__main__':
#     app.run()

