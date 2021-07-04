import os

import pandas as pd

import openfile

df = pd.read_csv('dataconvert.csv', encoding="utf8")
bag = openfile.readtxt(fpath="dataset_sequences.txt")
save = False
count = 1
for text in bag:
    text = text.strip().lower()
    print(text)
    textbag = text.split(" ")
    tagbag = []
    tagsentences = []
    for s in textbag:
        if s == textbag[0]:
            tagsen = "Sentence:{}".format(count)
        else:
            tagsen = ""
        tag = input("Nhap tag cho {}:".format(s))
        tagbag.append(tag)
        tagsentences.append(tagsen)
    for s, t in zip(textbag, tagbag):
        print("{:10} : {}".format(s, t))
    df = df.append(pd.DataFrame({"Sentence #": tagsentences,
                                 "Word": textbag,
                                 "Tag": tagbag}))
    count += 1
    os.system("cls")
print(df)
openfile.save_empty('dataset_sequences.txt')
if os.path.exists("dataconvert.csv"):
    os.remove("dataconvert.csv")
df.to_csv('dataconvert.csv', index=False)
print("Đã lưu")
# dataset= {"sentence":,
#           "word":textbag,
#           "tag":tagbag
#           }
# print(dataset)
