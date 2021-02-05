import transformers as trf

import utils
from config import config
from tabulate import tabulate


def main():
    # cfg = trf.RobertaConfig()
    # print(cfg)
    # model = trf.RobertaForSequenceClassification(cfg)
    # model = trf.RobertaForSequenceClassification(cfg)
    # tokenizer = trf.RobertaTokenizer.from_pretrained("roberta-base")

    data = utils.load_cleansed_data(0)
    classifier = trf.pipeline(
        "zero-shot-classification", model="roberta-base" #, device=0
    )

    candidate_labels = [topic.split("&") for topic in utils.topics]
    candidate_labels = utils.flatten(candidate_labels)

    for idx, text in data:
        res = classifier(text, candidate_labels, multi_class=True)

        labels_and_scores = zip(res["labels"], res["scores"])
        by_score = lambda t: t[1]
        labels_and_scores = sorted(labels_and_scores, key=by_score, reverse=True)

        print(res["sequence"])
        print(tabulate(labels_and_scores))
        input()


if __name__ == "__main__":
    main()
