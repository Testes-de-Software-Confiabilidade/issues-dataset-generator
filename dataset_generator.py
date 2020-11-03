class DatasetGenerator:
	def __init__(self, token, repo_name, issues_filters):
		from github import Github
		g = Github(token)
		repo = g.get_repo(repo_name)
		self.closed_issues = repo.get_issues(**issues_filters)

	def export_dataset(self, filename):
		dates = []

		years_counter = 0
		month_prev = 0

		for issue in self.closed_issues:
			date = issue.created_at.replace(day=1, hour=0, minute=0, second=0)
			dates.append(date)

		self.months = []

		with open(filename, 'w+') as file:
			for date in sorted(dates):
				month = date.month

				if(month_prev > month):
					years_counter += 1

				month_prev = month
				month = years_counter * 12 + month

				file.write(str(month) + '\n')

				self.months.append(month)
		
		return self.months

