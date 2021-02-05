    # TODO
    # title = psg.Text("INIT")
    # description = psg.Text("INIT")
    # text = psg.Text("INIT")

    # layout = [
    #     [psg.Text("Title:"), title],
    #     [psg.Text("Description:"), description],
    #     [psg.Text("Text:"), text],
    # ]

    # window = psg.Window("labeler", layout, no_titlebar=True)

    # while True:
    #     # print("updating")
    #     # title.update(value="bla")

    #     event, values = window.read()
    #     if event == psg.WIN_CLOSED or event == "exit":
    #         break

    #     title.update("TEXT")




import utils
from config import config
import math
from tabulate import tabulate


def has_label(labels):
    return len(labels) >= 3


def concat_text(ds):
    s = " ".join(ds["recent_posts"])
    return s


def print_topics(topics, pack=3):
    packs = math.ceil(len(topics) / pack)

    topics = sorted(topics.items())
    pretty = []
    for i in range(packs):
        tpack = topics[i * pack : (i + 1) * pack]
        tpack = utils.flatten(tpack)

        pretty += [tpack]

    print(tabulate(pretty))

def write_topic(path, idx, topic):
    with open(path, "a") as f:
        line = f"{idx},{topic}"
        print(line, file=f)

def clear(path):
    with open(path, "w") as f:
        pass

def last_topic_idx(path):
    try:
        with open(path, "r") as f:
            lines = f.readlines()

        last_idx = int(lines[-1].split(",")[0])
        return last_idx
    except:
        return 0





if __name__ == "__main__":
    dataset_num = 0

    data = utils.load_data(dataset_num)
    raw = utils.load_raw(dataset_num)
    topic_path = utils.make_topic_path(dataset_num)


    topics = utils.mapped_topics
    print_topics(topics)

    last_idx = last_topic_idx(topic_path)
    start_idx = last_idx + 1

    raw = raw[start_idx:]
    data = data[start_idx:]

    for label, data in zip(raw, data):
        if not has_label(label):
            write_topic(topic_path, *label)
            continue

        print("--------------------------------------------------------------------")
        print("--------------------------------------------------------------------")
        print("--------------------------------------------------------------------")
        print("--------------------------------------------------------------------")
        print("--------------------------------------------------------------------")
        print(concat_text(data))
        print("")
        print("DESC:", data["description"])
        print("TITLE:", data["title"])
        print("GOOGLE:", *label[1:])

        # print_topics(topics)

        while True:
            shortcuts = input("Input shortcut:")
            shortcuts = shortcuts.split(",")

            all_correct = True
            for sc in shortcuts:
                if sc not in topics:
                    all_correct = False

            if not all_correct:
                print("Try again.")
                continue


        topic = topics[shortcut]
        idx = label[0]

        write_topic(topic_path, idx, topic)
