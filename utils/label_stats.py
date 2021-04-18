from config import config
import utils

import sys
import math
from tabulate import tabulate
from collections import Counter
import numpy as np
import pandas as pd

def make_lang_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-lang.txt"


def count_labels_in(path):
    train_df = pd.read_csv(path)
    labels = train_df["labels"].apply(lambda x: np.array(eval(x)))


    counter = [0 for _ in range(42)]

    for label in labels:
        where_label = np.argwhere(label == 1)
        for idx in where_label:
            counter[idx[0]] += 1

    pretty = [["Label", "Count"], ["LabeledItems", len(train_df)]]
    for hr, c in zip(utils.topics, counter):
        pretty += [[hr, c]]

    print(tabulate(pretty))

if __name__ == "__main__":
    # dataset_num = sys.argv[1]

    count_labels_in("data/tg/train.csv")
    count_labels_in("data/tg/test.csv")



    # ### XX-lang.txt

    # labels = utils.load_lang(dataset_num)

    # langs = [lang for _, lang in labels]
    # lang_count = Counter(langs)

    # n_labels = len(labels)
    # n_langs = len(lang_count)

    # pretty = [["n_labels", n_labels]]
    # pretty += [["n_langs", n_langs]]
    # pretty += [[""]]

    # lang_count = sorted(list(lang_count.items()))

    # per_row = 5

    # header = [""]
    # for i in range(per_row):
    #     header.append("lang")
    #     header.append("samples")

    # pretty += [header]

    # for i in range(math.ceil(n_langs / per_row)):
    #     row = lang_count[i * per_row:(i+1)*per_row]
    #     pretty += [["", *utils.flatten(row)]]

    # print(tabulate(pretty))

    # ### XX-raw.txt
    # labels = utils.load_raw(dataset_num)

    # # filter unclassified samples
    # labels = [label for label in labels if len(label) >= 3]
    # # remove idx
    # labels = [label[1:] for label in labels]


    # categories = set()
    # for idx, label in enumerate(labels):
    #     for catconf in label:
    #         try:
    #             float(catconf)
    #         except:
    #             categories.add(catconf)


    # print("------------------------------------------------------")
    # print("------------------------------------------------------")
    # print("All categories")

    # per_row = 2
    # categories = sorted(list(categories))
    # pretty = [["Overall:", len(categories)]]
    # for i in range(math.ceil(len(categories) / per_row)):
    #     pretty += [categories[i * per_row: (i+1) * per_row]]

    # print(tabulate(pretty))

    print("------------------------------------------------------")
    print("------------------------------------------------------")
    print("High Probability")

    data = utils.load_data(dataset_num)
    labels = utils.load_raw(dataset_num)

    high_prob_labels = {}
    for idx, label in labels.items():
        for lidx, catconf in enumerate(label):
            try:
                conf = float(catconf)
                if conf > config.snorkel_conf_thresh:
                    high_prob_label = label[lidx - 1]

                    if high_prob_label not in  high_prob_labels:
                        high_prob_labels[high_prob_label] = 0

                    high_prob_labels[high_prob_label] += 1

                    print(data[labels[0]])
                    print(high_prob_label)
                    print(conf)
                    try:
                        print("INPUT")
                        in_ = input()
                    except KeyboardInterrupt:
                        sys.exit()

            except:
                pass

    print(sum(high_prob_labels.values()))
    print(len(high_prob_labels))
    for label, count in sorted(high_prob_labels.items()):
        print(label, count)
