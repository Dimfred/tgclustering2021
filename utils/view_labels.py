import utils
from config import config

import sys

from snorkel_label import GoogleLabel

if __name__ == "__main__":
    dataset_num = int(sys.argv[1])

    labels_to_view = ["/Sensitive Subjects"]

    data = utils.load_cleansed_data(dataset_num)
    raw = utils.load_raw(dataset_num)

    for d in data:
        idx = d[0]
        r = raw[idx]

        if len(r) <= 2:
            continue

        glabel = GoogleLabel(r[1:])
        # label = "/Business"
        # conf = 0.8

        # label = "/Sensitive"
        # conf = 0.8

        # label = "/Real Estate"
        # conf = 0.3

        # label = "Video Games"
        # conf = 0.8

        # label = "/Finance/Credit"
        # conf = 0.8

        # label = "Kids"
        # conf = 0.8

        label = "Autos & Vehicles"
        conf = 0.8

        if glabel.contains(label, conf):
            print(d)
            print(r)
            input()
