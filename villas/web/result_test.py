import pandas
from villas.web.result import Result

if __name__ == '__main__':

    r = Result(7, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Mywicm9sZSI6IkFkbWluIiwiZXhwIjoxNjIyMDMyMzM1LCJpYXQiOjE2MjE0Mjc1MzUsImlzcyI6Imh0dHA6Ly93ZWIudmlsbGFzLmZlaW4tYWFjaGVuLm9yZy8ifQ.LW0N8sWjs7F9zYX70wucvbHYTs19rA3ppORa9C4k1a4')

    # Show some info about the result dataset
    print(r)
    print(r.files)

    # Open the first CSV file and load it
    data = r.load_csv()

    print(data)

    # Open a raw text file
    rf = r.get_file_by_name('testfile')
    print(rf)

    with rf.open() as f:
        content = f.read()

        print(content)

    # Load a CSV file with Pandas
    rf2 = r.get_files_by_type('text/csv')[0]

    with rf2.open() as f:
        data = pandas.read_csv(f)

        print(data)

    # Open a CSV file from a Zip archive
    rf3 = r.get_file_by_name('testdata.zip')

    with rf3.open_zip('testdata.csv') as f:
        data = pandas.read_csv(f)

        print(data)

    # Download file to disk
    rf2.download()
