import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from urllib.parse import urljoin
import os
 
 
#parameters
url = ""
download_dir = "download"
file_extension = ""





ua = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
reqs = requests.get(url, headers=ua)
soup = BeautifulSoup(reqs.text, 'lxml')


script_dir = os.path.dirname(os.path.realpath(__file__))

download_dir = os.path.join(script_dir, download_dir)

if(not os.path.exists(download_dir)):
    os.makedirs(download_dir)

 
download_list = []
downloaded_count = 0


def get_filename_from_url(url=None):
    if url is None:
        return None
    urlpath = urlsplit(url).path
    return os.path.basename(urlpath)



for link in soup.find_all('a'):
    href = str(link.get('href'))
    filename = get_filename_from_url(href)

    if len(filename) == 0 or str.isspace(filename):
        continue

    if filename.endswith(file_extension):
        download_list.append(href)



for href in download_list:
    if href.endswith(file_extension):
        downloaded_count += 1
        filename = get_filename_from_url(href)

        if len(filename) == 0 or str.isspace(filename):
            continue

        msg = "downloading (" + str(downloaded_count) + '/' + str(len(download_list)) + "):" + filename + " (" + href + ")"
        print(msg)

        try:
            response = requests.get(urljoin(url, href))
            fo = open(os.path.join(download_dir, filename), "wb")
            fo.write(response.content)
            fo.close()
        except:
            print("cannot download: " + filename + " (" + href + ")")