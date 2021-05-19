import requests
import pandas
from dateutil.parser import parse

from villas.web.file import File

class Result:

    def __init__(self, id, token, endpoint='https://villas.k8s.eonerc.rwth-aachen.de'):
        self.id = id
        self.token = token
        self.endpoint = endpoint

        data = self._fetch()

        self.description = data.get('description')
        self.scenario_id = data.get('scenarioID')
        self.created_at = parse(data.get('createdAt'))
        self.updated_at = parse(data.get('updatedAt'))

        files = self._fetch_files()

        self.files = [File(f, self.token, self.endpoint) for f in files if f.get('id') in data.get('resultFileIDs', [])]

    def __repr__(self):
        return f'<villas.web.result.Result id={self.id} description={self.description} scenario_id={self.scenario_id}>'

    def _fetch(self):
        resp = requests.request('GET',
            url=f'{self.endpoint}/api/v2/results/{self.id}',
            headers={
                'Authorization': 'Bearer ' + self.token
            })
        resp.raise_for_status()

        return resp.json().get('result')

    def _fetch_files(self):
        resp = requests.request('GET',
            url=f'{self.endpoint}/api/v2/files?scenarioID={self.scenario_id}',
            headers={
                'Authorization': 'Bearer ' + self.token
            })
        resp.raise_for_status()

        return resp.json().get('files')

    def get_file_by_name(self, fn):
        files = [f for f in self.files if f.name == fn]

        if len(files) == 1:
            return files[0]
        else:
            return None

    def get_files_by_type(self, type):
        return [f for f in self.files if f.type == type]

    def load_csv(self, fn=None):
        if fn:
            f = self.get_file_by_name(fn)
        else:
            fs = self.get_files_by_type('text/csv')

            if len(fs) >= 1:
                f = fs[0]
            else:
                return None

        with f.open() as rf:
            return pandas.read_csv(rf)

