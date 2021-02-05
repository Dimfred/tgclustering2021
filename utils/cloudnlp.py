from google.cloud import language_v1 as lv1

import json
import re

from config import config


def load_tg_dataset(idx):
    with open(config.tg_ds / f"{str(idx).zfill(2)}-data.txt", encoding="utf8") as f:
        lines = f.readlines()

    dataset = [json.loads(line) for line in lines]
    return dataset


def concat_ds_item(ds):
    s = ds["title"]
    s += ds["description"]
    s += " ".join(ds["recent_posts"])
    return s

def strip_lang_from_exception(e):
    match_lang_code = r"language (.*) is not supported"
    match = re.search(match_lang_code, str(e))
    if match is None:
        print("-------------------------------------------")
        print("Match was none some other exception occured")
        print(str(e))
        return None

    lang_code = match.group(1)
    return lang_code

def write_result(file, idx, res):
    with open(file, "a") as f:
        line = f"{idx},{res}"
        print(line, file=f)


if __name__ == "__main__":
    # import sys
    # sys.exit()

    labels_out = "00-raw.txt"

    client = lv1.LanguageServiceClient()

    ds = load_tg_dataset(0)
    for idx, item in enumerate(ds):
        text = concat_ds_item(item)
        # text = concat_ds_item(ds[14])
        doc = lv1.Document(content=text, type_=lv1.Document.Type.PLAIN_TEXT)

        try:
            res = client.classify_text(request={"document": doc})
            categories = res.categories

            res_line = []
            for category in categories:
                res_line.append(category.name)
                res_line.append(category.confidence)

            label_to_write = ",".join((str(r) for r in res_line))

        except Exception as e:
            lang_code = strip_lang_from_exception(e)
            label_to_write = lang_code

        print(idx, label_to_write)
        # break
        write_result(labels_out, idx, label_to_write)
