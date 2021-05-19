import requests
from zipfile import ZipFile
from dateutil.parser import parse
import tempfile

class File:

    def __init__(self, data, token, endpoint='https://villas.k8s.eonerc.rwth-aachen.de'):
        self.id = data.get('id')
        self.token = token
        self.endpoint = endpoint


        self.name = data.get('name')
        self.scenario_id = data.get('scenarioID')
        self.created_at = parse(data.get('createdAt'))
        self.updated_at = parse(data.get('updatedAt'))

        self.type = data.get('type')
        self.key = data.get('key')
        self.size = data.get('size')
        self.url = f'{self.endpoint}/api/v2/files/{self.id}'

    def __repr__(self):
        return f'<villas.web.file.File id={self.id} name={self.name} size={self.size} type={self.type}>'

    def open(self, download=False):
        resp = requests.request('GET',
            url=f'{self.endpoint}/api/v2/files/{self.id}',
            headers={
                'Authorization': 'Bearer ' + self.token
            },
            stream=True)

        resp.raise_for_status()

        if download:
            tf = tempfile.NamedTemporaryFile()
            for chunk in resp.iter_content(chunk_size=8192): 
                tf.write(chunk)
            
            tf.seek(0)

            return tf
        else:
            return resp.raw

    def open_zip(self, filename):
        f = self.open(True)

        print(f)

        zf = ZipFile(f)
        
        return zf.open(filename)

    def download(self, dest=None):
        with self.open() as f:
            with open(dest or self.name, 'wb') as df:
                df.write(f.read())
