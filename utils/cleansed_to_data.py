from config import config
import utils

import sys
from tabulate import tabulate


def has_raw_label(l):
    return len(l) > 2


if __name__ == "__main__":
    dataset_num = sys.argv[1]

    cleansed = utils.load_cleansed(dataset_num)
    raw = utils.load_raw(dataset_num)
    cleansed_data_path = utils.make_cleansed_data_path(dataset_num)

    with open(cleansed_data_path, "w") as f:
        for idx, text in cleansed:
            raw_data = raw[idx]

            if not has_raw_label(raw_data):
                continue

            print(f"{idx},{text}", file=f)

    with open(cleansed_data_path, "r") as f:
        lines = f.readlines()

    # stat
    pretty = [["Len raw:", len([l for l in raw if has_raw_label(l)])]]
    pretty += [["Len cleansed:", len(cleansed)]]
    pretty += [["Len cleansed data:", len(lines)]]

    print(tabulate(pretty))
