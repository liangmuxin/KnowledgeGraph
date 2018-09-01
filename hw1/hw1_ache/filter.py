import re
import os
import uuid
import datetime
import json

ARTIST_RE = str("https%3A%2F%2Famericanart.si.edu%2Fartist%2F.*")
ARTWORK_RE = str("https%3A%2F%2Famericanart.si.edu%2Fartwork%2F.*")


class filter():
    def __init__(self, reg, filedir):
        self.reg = reg
        self.filedir = filedir
    
    def filter(self):
        file_dir = os.path.join(self.filedir)
        print("the file_directory is", file_dir)
        all_files = os.listdir(file_dir)
        target_list = []
        for a in all_files:
            if re.search(ARTIST_RE, a):
                target_list.append(a)
        return target_list

    def writejl(self, targets, filename):
        output = os.path.join(self.filedir, filename)
        with open(output, "w") as f:
            for t in targets:
                file = os.path.join(self.filedir, t)
                with open(file, "r") as tmp:
                    out = {}
                    out["raw_content"] = str(tmp.read())
                    out["url"] = str(t.replace("%3A", ":").replace("%2F", "/"))
                    out["timestamp_crawl"] = int(datetime.datetime.now().timestamp())
                    out["doc_id"] = str(uuid.uuid4())
                    # json.dumps(out)
                    f.write(json.dumps(out))

artistfilter = filter(ARTIST_RE, "/Users/muxin/Desktop/KnowledgeGraph/KnowledgeGraph/hw1/hw1_ache/artists/outputs/default/data_pages/americanart.si.edu")
artistfilter.writejl(artistfilter.filter(), "artist_ache.jl")


artworkfilter = filter(ARTWORK_RE, "/Users/muxin/Desktop/KnowledgeGraph/KnowledgeGraph/hw1/hw1_ache/artworks/outputs/default/data_pages/americanart.si.edu")
artworkfilter.writejl(artworkfilter.filter(), "artwork_ache.jl")