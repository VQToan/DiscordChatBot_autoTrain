import pickle

import numpy as np
from keras_preprocessing.sequence import pad_sequences

import model as md

with open("datalite.pkl", "rb") as f:
    data = pickle.load(f)
    word2idx, idx2tag, num_tag = data[0], data[1], data[2]
    f.close()
model = md.build_model(num_tag, len(word2idx))
model.load_weights("model.hdf5")
finish= False
while not finish:
    text = input("Nhập câu muốn phân tích: ")
    words = list(text.split(' '))
    bag = []
    end = True
    i = 0
    while end:
        text = "{}_{}".format(words[i], words[i + 1])
        # print(text)
        if text in word2idx:
            bag.append(text)
            i += 2
        else:
            if (i == (len(words) - 2)):
                bag.append(words[i])
                bag.append(words[i + 1])
                # print(i)
            else:
                bag.append(words[i])
            i += 1
        if i >= (len(words) - 1): end = False
    # print(bag)
    sqtext = []
    for item in bag:
        if item not in word2idx:
            sqtext.append(word2idx['UNK'])
        else:
            sqtext.append(word2idx[item])
    A = [sqtext]
    A = pad_sequences(maxlen=75, sequences=A, padding="post", value=word2idx["PAD"])
    # print(A)
    words =[]
    p = model.predict(np.array([A[0]]))
    p = np.argmax(p, axis=-1)
    #
    #
    print("{:15}||{}".format("Word", "Pred"))
    print(40 * "*")
    for w, pred in zip(bag, p[0]):
        if w != 0:
            print("{:15}: {}".format(w, idx2tag[pred]))
    Yconform= False
    while not Yconform:
        confirm = input("Bạn có muốn tiếp tục? (y/n)")
        if confirm.strip().lower() == 'y':
            finish = False
            Yconform = True
        if confirm.strip().lower() == 'n':
            finish = True
            Yconform= True
