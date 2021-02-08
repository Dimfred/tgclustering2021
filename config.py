from easydict import EasyDict as edict

from pathlib import Path
import os


config = edict()


############
# general
############

config.misc = Path("misc")
config.google_cloud_creds = config.misc / "TGClustering-secret.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(config.google_cloud_creds)


############
# datasets
############

config.data_dir = Path("data")
config.topics = config.data_dir / "topics.txt"

config.tg_ds = config.data_dir / "tg"
config.langdetect_ds = config.data_dir / "langdetect_tatoeba/sentences.csv"

config.roberta_dir = config.tg_ds / "roberta"
config.ruberta_dir = config.tg_ds / "ruberta"

config.ru_dir = config.data_dir / "ru"
config.fact_ru = config.ru_dir / "factRuEval-2016-master"

##############
# langdetect
##############

config.langdetect = edict()
config.langdetect.epochs = 10
config.langdetect.optim = "adam"

config.langdetect.min_sentence_len = 20
config.langdetect.max_sentence_len = 200
config.langdetect.n_samples_per_lang = 50_000
config.langdetect.n_trigram_features = 200

############
# snorkel
############

config.snorkel_dir =  config.data_dir / "snorkel"
config.porn_websites = config.snorkel_dir / "porn_websites.txt"
config.snorkel_conf_thresh = 0.6
