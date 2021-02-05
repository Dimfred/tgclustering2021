from config import config
import utils

import sys


def convert_to_lang(raw_label):
    idx, *rest = raw_label.split(",")

    # if empty insert NA
    if not rest[0]:
        return idx, "NA"

    # was labeled successfully can hence only be "en"
    if len(rest) >= 2:
        return idx, "en"

    # sometimes during an exception we cannot determine the language, probably
    # because not enough words were provided also return "NA"
    if rest[0] == "None":
        return idx, "NA"

    # else return the 2 letter lang code
    return idx, rest[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("./labels_to_lang.py <DATASET-NUMBER>")
        sys.exit()

    label_num = sys.argv[1]

    raw_path = utils.make_raw_path(label_num)
    lang_path = utils.make_lang_path(label_num)

    with open(raw_path, "r") as f:
        labels = f.readlines()
    labels = [l.strip() for l in labels]
    labels = [convert_to_lang(l) for l in labels]

    with open(lang_path, "w") as f:
        for idx, lang in labels:
            write = f"{idx},{lang}"
            print(write, file=f)
