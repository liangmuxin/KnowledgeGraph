from bs4 import BeautifulSoup
import json
import os
import sys


ARTISTS_INFO = ["artist_url", "artist_name", "birth_date", "death_date", "nationalities"]
ARTWORKS_INFO = ["artwork_url", "title", "artist_url", "object_number", "date"]


class Extractor():
    def __init__(self, name):
        self.name = name
        self.artist_path = "Homework 2/saam.required.artists.jl"
        self.artwork_path = "Homework 2/saam.required.artworks.jl"
        self.out = []

    def get_pretty_print(self):
        with open(self.artist_path, "r") as a:
            tmp = json.loads(a.readline())
            soup = BeautifulSoup(tmp["raw_content"])
            with open("sample_artist.html", "w") as oa:
                oa.write(soup.prettify())

        with open(self.artwork_path, "r") as a:
            tmp = json.loads(a.readline())
            soup = BeautifulSoup(tmp["raw_content"])
            with open("sample_artwork.html", "w") as oa:
                oa.write(soup.prettify())

    def readjl(self):
        if self.name == "artwork":
            path = self.artwork_path
            with open(path, "r") as f:
                for line in f:
                    collection = json.loads(line)
                    url = collection["url"]
                    content = collection["raw_content"]
                    soup = BeautifulSoup(content, "html.parser")
                    tmp = soup.find_all(class_="attributes dl-horizontal")[0]
                    labels = tmp.find_all("dt")
                    labelslist = list(map(lambda x: x.get_text().strip(), labels))
                    items = tmp.find_all("dd")
                    itemslist = list(map(lambda x: x.get_text().strip(), items))
                    information = dict(zip(labelslist, itemslist))
                    name = information["Title"]
                    artist_url = "https://americanart.si.edu" + items[1].a["href"]
                    object_number = information["Object Number"]
                    date = information["Date"]
                    obj = [url, name, artist_url, object_number, date]
                    self.out.append(obj)

        else:
            path = self.artist_path
            with open(path, "r") as f:
                for line in f:
                    collection = json.loads(line)
                    url = collection["url"]
                    content = collection["raw_content"]
                    soup = BeautifulSoup(content, "html.parser")
                    tmp = soup.find_all(class_="attributes dl-horizontal")[0]
                    labels = tmp.find_all("dt")
                    labelslist = list(map(lambda x: x.get_text().strip(), labels))
                    items = tmp.find_all("dd")
                    itemslist = list(map(lambda x: x.get_text().strip(), items))
                    information = dict(zip(labelslist, itemslist))
                    name = information["Name"]
                    born = information["Born"].split("\n")[-1].strip()
                    try:
                        death = information["Died"].split("\n")[-1].strip()
                    except:
                        death = "living"
                    try:
                        nationalities = information["Nationalities"]
                    except:
                        nationalities = "Unknown"
                    obj = [url, name, born, death, nationalities]
                    self.out.append(obj)

    def generate_output(self):
        output = []
        if self.name == "artwork":
            for o in self.out:
                tmp  = {}
                for i, v in enumerate(ARTWORKS_INFO):
                    tmp[v] = o[i]
                output.append(tmp)
            with open("artwork_info.json", "w") as f:
                json.dump(output, f)
        else:
            for o in self.out:
                tmp  = {}
                for i, v in enumerate(ARTISTS_INFO):
                    tmp[v] = o[i]
                output.append(tmp)
            with open("artist_info.json", "w") as f:
                json.dump(output, f)

a = Extractor("artist")
a.readjl()
a.generate_output()
