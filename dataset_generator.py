from datetime import datetime
from github import Github



g = Github("GERE UM TOKEN E COLOQUE AQUI")
repo = g.get_repo("vuejs/vue")



def get_closed_issues(labels):
	closed_issues = repo.get_issues(state='closed', labels=labels)
	return closed_issues

closed_issues = get_closed_issues(['bug'])
posix_dates = []
for issue in closed_issues:
	posix_date = int((issue.created_at - datetime(1970,1,1)).total_seconds())
	posix_dates.append(posix_date)

for date in sorted(posix_dates):
	print(date)
