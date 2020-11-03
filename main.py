DATASET_FILE = 'TEST_react_dataset.txt'
GRAPG_NAME = 'react.png'
REPO_NAME = 'facebook/react'
GITHUB_TOKEN = '82a7cc5ab498b5ca86ea05eeefad40b3ed5398aa'

filters = {
    'state': 'closed', 
    'labels': ['Type: Bug',]
}


def main():
    from dataset_generator import DatasetGenerator
    from graph_generator import GraphGenerator
    
    ds = DatasetGenerator(token=GITHUB_TOKEN, repo_name=REPO_NAME, issues_filters=filters)
    ds.export_dataset(DATASET_FILE)

    GraphGenerator.export_graphs(dataset_file=DATASET_FILE, image_name=GRAPG_NAME)

main()

# from datetime import datetime
# from github import Github
# from graph_generator import generate_bugs_report



# g = Github(GITHUB_TOKEN)
# repo = g.get_repo(REPO_NAME)

# def get_closed_issues(labels):
# 	closed_issues = repo.get_issues(state='closed', labels=labels)
# 	return closed_issues


# dates = []
# for issue in get_closed_issues(ISSUE_LIST):
# 	date = issue.created_at.replace(day=1, hour=0, minute=0, second=0)
# 	dates.append(date)


# years_counter = 0
# month_prev = 0

# with open(DATASET_FILE, 'w+') as file:
#     for date in sorted(dates):
#         month = date.month

#         if(month_prev > month):
#             years_counter += 1

#         month_prev = month
#         month = years_counter * 12 + month

#         file.write(str(month) + '\n')

# generate_bugs_report(DATASET_FILE=DATASET_FILE, REPORT_FILE='vuejs_bugs_reports.png')