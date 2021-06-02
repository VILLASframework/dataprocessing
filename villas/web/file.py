import requests
import pandas
import scipy.io.wavfile
import scipy.io
import numpy
import json
import os
import IPython.display as ipyd
import IPython.core.formatters as ipyf
import pygments.lexers as pygl
import pygments.util as pygu
import mimetypes

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

    def load(self, *args, **kwargs):
        with self.open(download=True) as f:
            if   self.type == 'text/csv':
                return pandas.read_csv(f)
            elif self.type == 'application/json':
                return json.load(f)
            elif self.type in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                return pandas.read_excel(f, *args, **kwargs)
            elif self.type == 'application/x-hdf5':
                return pandas.read_hdf(f, *args, **kwargs)
            elif self.type == 'application/x-matlab-data':
                mat = scipy.io.loadmat(f)
                mat = {k: v for k, v in mat.items() if k[0] != '_'}
                return pandas.DataFrame({k: numpy.array(v).flatten() for k, v in mat.items()})
            else:
                return f.read()

    def _repr_mimebundle_(self, include, exclude):
        data = self.load()

        if self.type == 'application/octet-stream':
            type, encoding = mimetypes.guess_type(self.name, strict=False)
            if type is None:
                fn, ext = os.path.splitext(self.name)

                if ext == '.md':
                    self.type = 'text/markdown'
            else:
                self.type = type

        if isinstance(data, pandas.DataFrame):
            fdata = data # DataFrame already can format itself
        elif self.type in ['image/png', 'image/gif', 'image/jpeg']:
            fdata = ipyd.Image(data=data)
        elif self.type == 'image/svg+xml':
            fdata = ipyd.SVG(data=data)
        elif self.type.startswith('audio/'):
            self.temp = tempfile.NamedTemporaryFile('wb+')
            self.temp.write(data)
            self.temp.flush()
            fdata = ipyd.Audio(self.temp.name)
        elif self.type == 'text/html':
            fdata = ipyd.HTML(data.decode('utf-8'))
        elif self.type == 'application/javascript':
            return ipyd.Javascript(data)
        elif self.type == 'application/json':
            fdata = ipyd.JSON(data)
        elif self.type == 'text/markdown':
            fdata = ipyd.Markdown(data.decode('utf-8'))
        elif self.type in ['application/x-latex', 'application/x-tex']:
            fdata = ipyd.Latex(data.decode('utf-8'))

        elif self.type in ['text/plain']:
            try:
                lexer = pygl.get_lexer_for_filename(self.name)
                print(lexer, lexer.aliases[0])
                fdata = ipyd.Code(data=data.decode('utf-8'), language=lexer.aliases[0])
            except pygu.ClassNotFound:
                if self.type == 'text/plain':
                    fdata = ipyd.TextDisplayObject(data)
                else:
                    fdata = data
        else:
            try:
                lexer = pygl.get_lexer_for_mimetype(self.type)
                fdata = ipyd.Code(data=data.decode('utf-8'), language=lexer.aliases[0])
            except pygu.ClassNotFound:
                fdata = data

        return ipyf.format_display_data(fdata)

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
