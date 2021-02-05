
import utils
from config import config


def is_single_label(label):
    return len(label) == 3

if __name__ == "__main__":
    dataset_num = 0

    raw = utils.load_raw(dataset_num)
    data = utils.load_data(dataset_num)

    for label, data in zip(raw, data):
        if not is_single_label(label):
            continue

        print(data)
        print("GOOLE:", label)
        input()
