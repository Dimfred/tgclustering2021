import re

import utils
import sys


used_lang = "en"

for dataset_num in [0, 1, 2]:
    data, lang = utils.load_data(dataset_num), utils.load_lang(dataset_num)

    outpath = utils.make_cleansed_data_path(dataset_num, used_lang)

    filtered = []
    for idx, text in data.items():
        if used_lang != lang[idx]:
            continue

        filtered.append((idx, text))

    with open(outpath, "w") as f:
        for idx, text in filtered:
            print(f"{idx},{text}", file=f)

sys.exit()
