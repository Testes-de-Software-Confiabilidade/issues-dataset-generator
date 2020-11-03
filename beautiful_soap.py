import requests
from bs4 import BeautifulSoup

issues_ids = []

for i in range(1, 1000):
	page = requests.get("https://github.com/vuejs/vue/issues?page=%s&q=label:bug+is:closed" % (i))

	print('page ' + str(i) + ' status ' + page.headers['status'][:3])

	soup = BeautifulSoup(page.content, 'html.parser')
	matches = soup.findAll("div", {"class": "js-issue-row"})

	if(matches == []):
		break

	issues_ids += [a.attrs['id'] for a in matches]


print(issues_ids)
