import json
import os
import zipfile

import requests
from bs4 import BeautifulSoup


def collect_download_url():
    all_release_url = "https://github.com/CVEProject/cvelistV5/releases/expanded_assets/cve_2025-03-02_at_end_of_day"
    content = requests.get(all_release_url)
    html_text = content.text
    soup = BeautifulSoup(html_text, 'html.parser')
    download_url = soup.select_one("div > ul > li:nth-child(1) > div.d-flex.flex-justify-start.col-12.col-lg-9 > a")[
        'href']
    url = "https://github.com/" + download_url
    print(url)
    return url


def download_file(url):
    response = requests.get(url, stream=True)
    with open("cve.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):  # 分块写入文件
            file.write(chunk)


def decode_file(file_name):
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall("")


def read_data_and_format(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        json_data = json.load(file)
        return json_data


def walk_dirs(dir_name):
    files = []
    for item in os.listdir(dir_name):
        file_path = os.path.join(dir_name + item)
        files.append(file_path)
    return files


# download_file(collect_download_url())
# decode_file("cve.zip")
data = read_data_and_format("deltaCves/CVE-2022-42966.json")
# files = walk_dirs('deltaCves')
print(data['containers'])
