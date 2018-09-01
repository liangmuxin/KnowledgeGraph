import json
import os
import random
import copy
import ujson

ARTWORK_MANDATORY = "mandatory_artworks.txt"
ARTIST_MANDATORY = "mandatory_artists.txt"

ARTWORK_REQ = 3000
ARTIST_REQ = 5000


class jl_transfer():
    def __init__(self, name, input_file):
        self.name = name
        self.input_file = input_file
        self.checklist = []
        self.alljl = {}
        self.out = []
        self.rm = []

    def get_mandatory(self):
        if self.name == "artist":
            filename = ARTIST_MANDATORY
        else:
            filename = ARTWORK_MANDATORY
        with open(filename, "r") as f:
            for line in f:
                self.checklist.append(line.split("/")[-1].strip())
        self.checklist = list(set(self.checklist))

    def read_inputfile(self):
        with open(self.input_file, "r") as f:
            for line in f:
                # if json.loads(line)["url"]=="https://americanart.si.edu/artwork/summerscene-provincetown-8580":
                #     import pdb
                #     pdb.set_trace()
                self.alljl[json.loads(line)["url"].split("/")[-1]] = line[:-1]
        # import pdb
        # pdb.set_trace()

    def put_mandatory(self):
        checker = copy.copy(self.alljl)
        print(len(checker))
        print(len(self.alljl))
        for m in self.checklist:
            if m in checker:
                self.out.append(checker[m])
                self.rm.append(m)
                # del checker[m]
                # try:
                #     del self.alljl[m]
                # except:
                #     import pdb
                #     pdb.set_trace()
                #     print("???")
            else:
                print(m, "does not crawled")
            # try:
            #     del self.alljl[m]
            # except:
            #     print(m,"wtf")
        # self.alljl = checker
        for rrr in self.rm:
            # import pdb
            # pdb.set_trace()
            # print("a")
            try:
                # print("caonima")
                self.alljl.pop(rrr)
                # print("cao")
            except:
                # import pdb
                # pdb.set_trace()
                print("a")

    def execution(self):
        with open(self.input_file, "r") as f:
            count = 0
            for line in f:
                if count < 1000:
                    self.rm[json.loads(line)["url"].split("/")[-1]] = line[:-1]
                self.alljl[json.loads(line)["url"].split("/")[-1]] = line[:-1]
                count += 1

    def put_other(self):
        print("length for mandatory", len(self.out))
        if self.name == "artist":
            remain_length = ARTIST_REQ - len(self.out)
        else:
            remain_length = ARTWORK_REQ - len(self.out)
        selected_keys = random.sample(self.alljl.keys(), remain_length)
        for k in selected_keys:
            self.out.append(self.alljl[k])
        print("the length of output is", len(self.out))

    def shuffle_output(self):
        random.shuffle(self.out)
        print("shuffle finished")

    def generate_output(self, outputfile):
        with open(outputfile, "w") as o:
            for v in self.out:
                # import pdb
                # pdb.set_trace()
                # ujson.dump(v, o)
                o.write(v)
                o.write("\n")
        print("output has been generated to", outputfile)

        # TODO randomly pick numbers of remain_lenth summerscene-provincetown-8580keys from self.alljl, then store the value into self.out
        # Then shuffle self.out
        # Then output new jl from shuffled self.out


arti = jl_transfer("artist", "artist_ache.jl")
arti.get_mandatory()
arti.read_inputfile()
arti.put_mandatory()
arti.put_other()
arti.shuffle_output()
arti.generate_output("Muxin_Liang_artist_ache_cdr.jl")

# import pdb
# pdb.set_trace()

artw = jl_transfer("artwork", "artwork_scrapy.jl")
artw.get_mandatory()
# pdb.set_trace()
artw.read_inputfile()
# pdb.set_trace()
artw.put_mandatory()
artw.put_other()
artw.shuffle_output()
artw.generate_output("Muxin_Liang_artwork_ache_cdr.jl")


# print("finished")