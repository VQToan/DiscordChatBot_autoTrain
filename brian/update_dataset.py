import json
import os.path

import brian.NER.predict as prd


def get_tag(data):
    tag = ''
    if len(data) <= 3:
        for item in data:
            tag += item[0]
    else:
        for item in data:
            if (item[1] == 'V') or ('N' in item[1]):
                tag += item[0]
    return tag


def getpredict(text):
    pred = prd.predict()
    databag = pred.predicts(text)
    return get_tag(databag)


def read_text_raw(fpath: dir):
    f = open(fpath, 'r', encoding='utf-8')
    packs = f.read().strip().split('\n')
    data = []
    for pack in packs:
        pack = pack.strip().split('|=:=|')
        if pack != ['']:
            tag = pack[1].strip()
            tmp=pack[0].split('<=:=>')
            patterns = tmp[0].strip()
            responses = tmp[1].strip()
            data.append((tag, patterns, responses))
    return data


def read_dataset(fpath: dir):
    if not os.path.exists(fpath):
        file = open(fpath, 'w', encoding='utf-8')
        json.dump({"intents": [{"tag": "",
                                "patterns": [],
                                "response": []}]}, file)
        file.close()
    f = open(fpath, encoding='utf-8')
    data_file = f.read()
    intents = json.loads(data_file)
    datainside = intents['intents']
    f.close()
    return datainside


def save_dataset(fpath, datainside):
    if os.path.exists(fpath):
        os.remove(fpath)
    data = {'intents': datainside}
    file = open(fpath, 'w', encoding="utf-8")
    json.dump(data, file)
    file.close()
    print("Đã lưu")


def delete_text_raw(fpath):
    if os.path.exists(fpath):
        os.remove(fpath)


def create_text_review():
    data_file = open('brian/data/intents1.json', encoding='utf8')
    readdata = data_file.read()
    intents = json.loads(readdata)
    data_file.close()
    if os.path.exists('brian/data/textout.txt'):
        os.remove('brian/data/textout.txt')
    txtout = open('brian/data/textout.txt', 'a', encoding='UTF-8')
    for intent in intents['intents']:
        txtout.write("Tag :" + intent['tag'] + "\n")
        txtout.write("Pattern :" + "\n")
        for pattern in intent['patterns']:
            txtout.write('- ' + pattern + '\n')
        txtout.write("Response :" + "\n")
        for response in intent['responses']:
            txtout.write('- ' + response + '\n')
        txtout.write(40 * "*" + '\n')
    txtout.close()


def main(fpathtxt, fpathjson):
    datainside = read_dataset('brian/data/intents1.json')
    # print(datainside['tag'])
    data = read_text_raw(fpathtxt)
    tag=[]
    patterns=[]
    responses=[]
    if data != []:
        for item in data:
            if item[0] != 'None':
                tag.append(item[0])
                patterns.append(item[1])
                responses.append(item[2])
            else:
                tag.append(getpredict(item[1]))
                patterns.append(item[1])
                responses.append(item[2])

        # patterns = ["aaaaa", "hi"]
        # responses = ["aaaa", "hihih"]
        # tag = ["a", "hihihih"]
        # print(tag[0]==datainside[1]['tag'])
        for i in range(0, len(data)):
            passflag = False
            for j in range(0, len(datainside)):
                if tag[i] == datainside[j]['tag']:
                    if patterns[i] not in datainside[j]['patterns']:
                        datainside[j]['patterns'].append(patterns[i])
                    if responses[i] not in datainside[j]['responses']:
                        datainside[j]['responses'].append(responses[i])
                    passflag = True
                    break

            if passflag:
                continue
            datainside.append({"tag": tag[i],
                               "patterns": [patterns[i]],
                               "responses": [responses[i]]})

    save_dataset(fpathjson, datainside)
    print("Đã tạo file dataset")
    delete_text_raw(fpathtxt)
