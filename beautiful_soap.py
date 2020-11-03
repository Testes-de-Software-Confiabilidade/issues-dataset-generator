import requests
from bs4 import BeautifulSoup
from datetime import datetime

issues_ids = []

def get_posix_date(id):
	issue_page = requests.get('https://api.github.com/repos/vuejs/vue/issues/%s/events' % id)
	created_at = issue_page.json()[0]['created_at']

	created_at = created_at.split('T')
	created_at = created_at[0] + ' ' + created_at[-1].replace('Z','')
	created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
	posix_date = int((created_at - datetime(1970,1,1)).total_seconds())

	return posix_date


for i in range(1, 1000):
	page = requests.get("https://github.com/vuejs/vue/issues?page=%s&q=label:bug+is:closed" % (i))

	soup = BeautifulSoup(page.content, 'html.parser')
	matches = soup.findAll("div", {"class": "js-issue-row"})

	if(matches == []):
		break

	for issue in matches:
		id = issue.attrs['id'].replace('issue_', '')

		print(id, end=', ')
		print(get_posix_date(id))
		issues_ids += (id, get_posix_date(id))
		# print(id, get_posix_date(id))

# for issue_id, posix_date in issues_ids:
# 	print(issue_id, posix_date)

