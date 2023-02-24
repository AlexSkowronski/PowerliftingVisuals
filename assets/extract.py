from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen

def extract_dataset(url):
    try:
        response = urlopen(url)
        zipfile = ZipFile(BytesIO(response.read()))
        file_name = [x for x in zipfile.namelist() if '.csv' in x]
        return zipfile.open(file_name[0])
    except Exception as e:
        print(e)