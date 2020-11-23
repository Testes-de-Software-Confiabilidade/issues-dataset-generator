class Repository:
    def __init__(self, url, filters_rules):
        
        self.url = url

        labels_rules = filters_rules['labels']
        
        self.must_have_labels = set(labels_rules['must_have'])
        self.blocklist_labels = set(labels_rules['blocklist_labels'])

        self.name = url.split('/')[1].replace('.', '')
        self.dataset_file = 'datasets/' + self.name + '.csv'
        self.chart_name = 'graph/' + self.name + '.png'
        self.chart_name_linear = 'graph/' + self.name + 'linear_regression' + '.png'