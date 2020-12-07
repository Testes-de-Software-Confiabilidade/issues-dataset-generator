SOFTWARE = 'VUE'

from RepositoryClass import Repository

# YOU CAN CREATE ANOTHER REPO RULES
if(SOFTWARE == 'VUE'):
    filters_rules = {
        'labels': {
            'must_have': ['bug'],
            'blocklist_labels': []
        }
    }

    r = Repository('vuejs/vue', filters_rules)

elif(SOFTWARE=='ANGULARJS'):
    filters_rules = {
        'labels': {
            'must_have': ['type: bug'],

            'blocklist_labels': [
                'resolution: invalid',
                "resolution: can't reproduce",
                'resolution: duplicate',
                'Known Issue'
            ]
        }
    }

    r = Repository('angular/angular.js', filters_rules)

elif(SOFTWARE=='ANGULAR'):
    filters_rules = {
        'labels': {
            'must_have': ['type: bug/fix'],
            'blocklist_labels': ['needs reproduction', 'needs clarification']
        }
    }

    r = Repository('angular/angular', filters_rules)

elif(SOFTWARE == 'SPRING'):
    filters_rules = {
        'labels': {
            'must_have': ['type: bug'],
            'blocklist_labels': [
                'status: duplicate',
                'status: superseded',
                'status: waiting-for-triage',
                'status: invalid'
            ]
        }
    }

    r = Repository('spring-projects/spring-framework', filters_rules)

elif(SOFTWARE == 'ASPNETCORE'):
    filters_rules = {
        'labels': {
            'must_have': ['bug'],
            'blocklist_labels': []
        }
    }

    r = Repository('dotnet/aspnetcore', filters_rules)


else:
    filters = {
        'labels': {
            'must_have': ['Type: Bug'],
            'blocklist_labels': []
        }
    }

    r = Repository('dotnet/aspnetcore', filters_rules)


GITHUB_TOKEN = '<YOUR GITHUB TOKEN HERE>'

from dataset_generator import DatasetGenerator
from graph_generator import GraphGenerator

from collections import Counter

def main():

    # change loadFromFile to True if you have dataset file
    dg = DatasetGenerator(token=GITHUB_TOKEN, repository=r, loadFromFile=True)

    gg = GraphGenerator(dg)
    gg.weibull()

main()
