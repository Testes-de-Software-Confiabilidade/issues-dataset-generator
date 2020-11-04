SOFTWARE = 'SPRING'

if(SOFTWARE == 'VUE'):
    DATASET_FILE = 'datasets/vue_dataset.txt'
    GRAPH_NAME = 'graph/vuejs.png'
    REPO_NAME = 'vuejs/vue'
    filters = {
        'labels': ['bug']
    }

elif(SOFTWARE=='ANGULARJS'):
    DATASET_FILE = 'datasets/angularjs_dataset.txt'
    GRAPH_NAME = 'graph/angularjs.png'
    REPO_NAME = 'angular/angular.js'
    filters = {
        'labels': ['type: bug']
    }

elif(SOFTWARE=='ANGULAR'):
    DATASET_FILE = 'datasets/angular_dataset.txt'
    GRAPH_NAME = 'graph/angular.png'
    REPO_NAME = 'angular/angular'
    filters = {
        'labels': ['type: bug/fix']
    }

elif(SOFTWARE == 'SPRING'):
    DATASET_FILE = 'datasets/spring_dataset.txt'
    GRAPH_NAME = 'graph/spring.png'
    REPO_NAME = 'spring-projects/spring-framework'
    filters = {
        'labels': ['type: bug']
    }

elif(SOFTWARE == 'ASPNETCORE'):
    DATASET_FILE = 'datasets/aspnetcore_dataset.txt'
    GRAPH_NAME = 'graph/aspnetcore.png'
    REPO_NAME = 'dotnet/aspnetcore'
    filters = {
        'labels': ['bug']
    }


else:
    DATASET_FILE = 'datasets/react_dataset.txt'
    GRAPH_NAME = 'graph/react.png'
    REPO_NAME = 'facebook/react'
    filters = {
        'labels': ['Type: Bug']
    }

GITHUB_TOKEN = '355de9b38dc2ea0279dfa4d44cd82120ea71794e'

def main():
    from dataset_generator import DatasetGenerator
    from graph_generator import GraphGenerator
    
    # ds = DatasetGenerator(token=GITHUB_TOKEN, repo_name=REPO_NAME, issues_filters=filters)
    # ds.export_dataset(DATASET_FILE)

    gg = GraphGenerator(dataset_file=DATASET_FILE)

    gg.export_graphs(
        image_name=GRAPH_NAME, 
        title='Padrão de chegada de issues de\nBug do Repositório %s' % (REPO_NAME)
    )

main()