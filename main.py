SOFTWARE = 'ANGULAR'

if(SOFTWARE == 'VUE'):
    DATASET_FILE = 'datasets/vue_dataset.txt'
    GRAPH_NAME = 'graph/vuejs.png'
    REPO_NAME = 'vuejs/vue'
    filters = {
        'labels': ['bug']
    }

elif(SOFTWARE=='ANGULAR'):
    DATASET_FILE = 'datasets/angularjs_dataset.txt'
    GRAPH_NAME = 'graph/angularjs.png'
    REPO_NAME = 'angular/angular.js'
    filters = {
        'labels': ['type: bug']
    }

else:
    DATASET_FILE = 'datasets/react_dataset.txt'
    GRAPH_NAME = 'graph/react.png'
    REPO_NAME = 'facebook/react'
    filters = {
        'labels': ['Type: Bug']
    }

GITHUB_TOKEN = '82a7cc5ab498b5ca86ea05eeefad40b3ed5398aa'

def main():
    from dataset_generator import DatasetGenerator
    from graph_generator import GraphGenerator
    
    # ds = DatasetGenerator(token=GITHUB_TOKEN, repo_name=REPO_NAME, issues_filters=filters)
    # ds.export_dataset(DATASET_FILE)
    
    GraphGenerator.export_graphs(
        dataset_file=DATASET_FILE, 
        image_name=GRAPH_NAME, 
        title='Padrão de chegada de issues de Bug do Repositório %s' % (REPO_NAME)
    )

main()