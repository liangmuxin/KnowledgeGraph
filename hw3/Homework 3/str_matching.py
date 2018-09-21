
import numpy as np
import os
import json


def Levenshtein(x: str, y: str): # Levenshtein Similarity Measure
    if len(x) == 0 and len(y) == 0:
        return 1.0
    d = np.zeros((len(x)+1, len(y)+1))
    for i in range(1, len(x)+1):
        d[i, 0] = i
    for j in range(1, len(y)+1):
        d[0, j] = j
    for j in range(1, len(y)+1):
        for i in range(1,len(x)+1):
            if x[i-1] == y[j-1]:
                cost = 0
            else:
                cost = 1
            d[i, j] = min(d[i-1, j]+1, d[i, j-1]+1, d[i-1, j-1]+cost)
    return 1 - d[len(x), len(y)] / max(len(x), len(y))


def Jaro(x: str, y: str): # Jaro Similarity Measure
    if len(x) == 0 and len(y) == 0:
        return 1.0
    mx = np.zeros((len(x), 1))
    my = np.zeros((len(y), 1))
    max_distance = max(len(x), len(y)) // 2 - 1
    t = 0

    # for i in range(len(x)): # calculate match
    #     for j in range(len(y)):
    #         if y[j] == x[i] and abs(i-j) <= max_distance:
    #             mx[i] = 1
    #             my[j] = 1
    # matches = np.sum(mx)
    # calculating matches
    for i in range(len(x)):
        for j in range(max(0, i - max_distance), min(i + max_distance + 1, len(y))):
            if my[j] == 1:
                continue
            if x[i] != y[j]:
                continue
            mx[i] = 1
            my[j] = 1
    matches = np.sum(mx)
    # calculationg transpose
    j = 0
    for i in range(len(mx)):
        if mx[i] != 1:
            continue
        while my[j] != 1:
            j += 1
        if mx[i] != my[j]:
            t += 1
        j += 1
    transpose = t//2
    return ((matches / len(x) + matches / len(y) + (matches - transpose) / matches)) / 3

# print(Levenshtein('DIXON', 'DICKSONX'))
# print(Jaro('DIXON', 'DICKSONX'))

# for birth date, using Levenshtrein distance, if it is not equals to 1, disgard
# for name, use Jaro with an accuracy of > 0.9, preproscessing
path = "/Users/muxin/Desktop/KnowledgeGraph/KnowledgeGraph/hw3/Homework 3"
SAAM = os.path.join(path, "saam_artists.json")
ULAN = os.path.join(path, "ulan_artists.json")
TRAIN = os.path.join(path, "train.json")
GROUND = os.path.join(path, "saam_ulan.dev.json")
SAAM_2 = os.path.join(path, "saam.test.json")
TEST = os.path.join(path, "saam_ulan.test.json") 


def change_ulan(name: str): # changes to structure "Firstname Lastname"
    out = name.split(", ")
    return out[-1] + " " + out[0]

def matching(source: str, target: str, output: str):
    with open(source, "r") as s:
        source_json = json.load(s)
    with open(target, "r") as t:
        target_json = json.load(t)
    out = []
    for sample in source_json:
        tmp = {}
        tmp["saam_artist"] = sample["url"]
        tmp["ulan_artist"] = None
        for t in target_json:
            try:
                birth_score = Levenshtein(t["birth_date"], sample["birth_year"]) # not same birth date then not match
            except:
                birth_score = 1 # year may be null
            if birth_score == 1 and Jaro(sample["name"], change_ulan(t["name"])) >= 0.8:
                tmp["ulan_artist"] = t["uri"]

        out.append(tmp)
    try:
        o = open(output, "w")
        json.dump(out, o)
        o.close()
    except:
        print("something wrong")

# matching(SAAM, ULAN, TRAIN)
# matching(SAAM, ULAN, TEST)

def score(): # score train result
    with open(TRAIN, "r") as t:
        predict = json.load(t)
        correct = 0
        with open(GROUND, "r") as g:
            ground_truth = json.load(g)
            ground_truth_dict = {}
            for m in ground_truth:
                ground_truth_dict[m["saam_artist"]] = m["ulan_artist"]
            checker = {}
            for v in predict:
                checker[v["saam_artist"]] = v["ulan_artist"]
            for k in ground_truth_dict.keys():
                if checker[k] == ground_truth_dict[k]:
                    correct+=1

    return correct/len(ground_truth)
# print(score()) #0.914
def generate_prediction():
    with open(TRAIN, "r") as t:
        all_result = json.load(t)
        result_mapper = {}
        for m in all_result:
            result_mapper[m["saam_artist"]] = m["ulan_artist"]
        with open(SAAM_2, "r") as s:
            output = []
            all_index = json.load(s)
            for a in all_index:
                tmp = {}
                tmp["saam_artist"] = a["saam_artist"]
                tmp["ulan_artist"] = result_mapper[a["saam_artist"]]
                output.append(tmp)
    with open(TEST, "w") as t:
        json.dump(output, t)

print(score())

generate_prediction()





