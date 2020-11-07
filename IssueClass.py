from datetime import datetime

class Issue:
    def __init__(self, id, closed_at, created_at, state, url):
        self._id = id.strip()
        if(not 'None' in closed_at):
            self._closed_at = datetime.strptime(closed_at.strip(), '%Y-%m-%d %H:%M:%S')

        self._created_at = datetime.strptime(created_at.strip(), '%Y-%m-%d %H:%M:%S')
        self._state = state.strip()
        self._url = url.strip()

    def __str__(self):
        return f'{self._id}, {self._closed_at}, {self._created_at}, {self._state}, {self._url}'

    @property
    def id(self):
        return self._id

    @property
    def closed_at(self):
        return self._closed_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def created_at(self):
        return self._created_at

    @property
    def state(self):
        return self._state

    @property
    def url(self):
        return self._url