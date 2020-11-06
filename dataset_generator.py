import github
from github.PaginatedList import PaginatedList
from RepositoryClass import Repository
from IssueClass import Issue

import datetime 
import time
from github import RateLimitExceededException

import requests


class DatasetGenerator:
    def __init__(self, token, repository, loadFromFile=False):
        self.g = github.Github(token)
        self.repository = repository
        self.repository_connection = self.g.get_repo(repository.url)

        self.idx = 0
        self.tokens_list = [

        ]

        if(loadFromFile):
            self.filtered_issues = self.read_csv()
            
        else:
            self.all_issues = self.repository_connection.get_issues(state='all')
            self.filtered_issues = self.apply_filters()


    def read_csv(self):
        filtered_issues = []
        with open(self.repository.dataset_file, 'r') as file:
            file.readline() # jump csv header line

            for issue in file:
                issue_data = issue.strip().split(',')
                filtered_issues.append(Issue(*issue_data))

        return filtered_issues


    def is_valid(self, issue):
        all_labels = set()

        for label in issue.labels:
            all_labels.add(label.name)
            if(label.name in self.repository.blocklist_labels):
                return False
            
        for label in self.repository.must_have_labels:
            if(label not in all_labels):
                return False

        return True
    
    def apply_filters(self):
      
        filtered_issues = []

        with open(self.repository.dataset_file, 'w') as file:
            file.write('"id", "closed_at", "created_at", "state", "url"\n')

            for i, issue in enumerate(self.all_issues):

                remaining = self.g.get_rate_limit().core.remaining

                if(remaining < 10):
                    self.idx += 1
                    self.g._Github__requester._Requester__authorizationHeader = "token " + self.tokens_list[self.idx % 3]

                perc = f'{i / self.all_issues.totalCount:.2f}%'
                print(i, self.all_issues.totalCount, perc,  self.g.get_rate_limit())

                if(issue.pull_request):
                    continue

                if(self.is_valid(issue)):
                    filtered_issues.append(issue)
                    file.write((f"{issue.number}, {issue.closed_at}, {issue.created_at}, {issue.state}, {issue.url}\n"))

                    print(f'{issue.number} {issue.html_url} is valid\n')
                else:
                    print(f'{issue.number} {issue.html_url} is invalid\n')
        
        print('%s issues válidas' % len(filtered_issues))
        return filtered_issues


    def get_issue_months(self):
        dates = []
        for issue in self.filtered_issues:
            date = issue.created_at.replace(day=1, hour=0, minute=0, second=0)
            dates.append(date)

        dates = sorted(dates)

        months = []
        prev_date = None
        years_counter = 0

        for date in dates:
            if(prev_date):
                years_counter += (date.year - prev_date.year)
            
            prev_date = date

            month = years_counter * 12 + date.month
            months.append(month)
        
        return months

