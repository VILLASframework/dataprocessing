import requests
from zipfile import ZipFile 

class Result:

    def __init__(self, file_id, token, endpoint='https://villas.k8s.eonerc.rwth-aachen.de'):
        self.file_id = file_id
        self.token = token
        self.endpoint = endpoint

    def open(self):
        resp = requests.request('GET',
            url=f'{self.endpoint}/api/v2/files/{self.file_id}',
            headers={
                'Authorization': 'Bearer ' + self.token
            },
            stream=True)

        resp.raise_for_status()

        return resp.raw

    def open_zip(self, filename):
        f = self.open()

        zf = ZipFile(f)
        
        return zf.open(filename)
