import pandas
from villas.web.result import Result

if __name__ == '__main__':

    r = Result('https://l.0l.de/W3OQo', '')
    f = r.open_zip('Sample100.csv')

    df = pandas.read_csv(f)

    print(df)
