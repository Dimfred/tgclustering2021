from numpy.lib.ufunclike import fix
import utils
from utils import Topics
from config import config


import snorkel_defaults as sdf
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel, MajorityLabelVoter
from snorkel.labeling import labeling_function as lf

import pandas as pd

import re
import numpy as np
from tabulate import tabulate
from collections import Counter


class GoogleLabel:
    def __init__(self, labels_and_confidences):
        self.data = []

        for label, confidence in zip(
            labels_and_confidences[::2], labels_and_confidences[1::2]
        ):
            try:
                # print(label, confidence)
                self.data.append((str(label), float(confidence)))
            except:
                # we have some errors in the google label where a label is
                # there without a confidence we still have a glabel then
                # but it does not have any data normally so fuck it
                pass

    def contains(self, string, conf_th=0.6):
        for label, confidence in self.data:
            if string in label and confidence > conf_th:
                return True

        return False


#################
# porn
#################

website_prefix = r"(\s|https://|http://|www.|https://www.|http://)"
search_porn = r"(({})({}))".format(website_prefix, "|".join(sdf.porn_websites))
search_porn = search_porn.replace("-", r"\-")
search_porn = search_porn.replace(".", r"\.")
search_porn = re.compile(search_porn)

common_porn_provider = r"(brazzers|bangbros|hdpornxxx)"
search_porn_provider = re.compile(common_porn_provider)

porn_channels = [
    "@teenporntop",
    "@hotshotsadultseries",
    "@adultwebseriescineplex",
    "@xvideos",
]
porn_channels = "|".join(porn_channels)
search_porn_channels = re.compile("({})".format(porn_channels))


@lf()
def porn(x):
    text, label = x["text"], x["google_label"]

    if label is not None and label.contains("Adult", config.snorkel_conf_thresh):
        return Topics.EroticContent.value

    porn_links = search_porn.findall(text)
    if porn_links:
        return Topics.EroticContent.value

    porn_provisders = search_porn_provider.findall(text)
    if porn_provisders:
        return Topics.EroticContent.value

    if "mia khalifa" in text:
        return Topics.EroticContent.value

    porn_channels = search_porn_channels.findall(text)
    if porn_channels:
        return Topics.EroticContent.value

    return Topics.NONE.value


#################
# crypto
#################

crypto_words = [
    # words
    "satoshi nakamoto",
    "defi",
    "cryptocurrency",
    "crytocurrencies",
    "blockchain",
    "newscrypto",
    "dex",
    # coins
    "bitcoin",
    "dogecoin",
    "ethereum",
    "sushiswap",
    # websites
    "coingeko.com" "cryptonomist.ch",
    "binance.com",
    "coindesk.com",
]

search_crypto_words = r"({})".format("|".join(crypto_words))
search_crypto_words = re.compile(search_crypto_words)


@lf()
def crypto(x):
    # TODO payment mothod: bitcoin ignore!

    x = x["text"]
    crypto_words = search_crypto_words.findall(x)
    if len(crypto_words) > 3:
        return Topics.Cryptocurrencies.value

    return Topics.NONE.value


#################
# invest
#################

invest_words = [
    "forex",
    "pips",
    "investment plan",
    "#invest",
    "take profit",
    "binary trade",
]
invest_words = "|".join(invest_words)

search_invest_words = r"({})".format(invest_words)
search_invest_words = re.compile(search_invest_words)


@lf()
def investments(x):
    text = x["text"]

    invest_words = search_invest_words.findall(text)
    if invest_words:
        return Topics.Investments.value

    if re.findall("binary signal", text):
        return Topics.Investments.value

    if "free signals" in text:
        return Topics.Investments.value

    if "gold signals" in text:
        return Topics.Investments.value

    return Topics.NONE.value


#################
# video games
#################


@lf()
def video_games(x):
    label = x["google_label"]
    if label is not None:
        if label.contains("Video Games", config.snorkel_conf_thresh):
            return Topics.VideoGames.value

        if label.contains("Online Games", config.snorkel_conf_thresh):
            return Topics.VideoGames.value

    return Topics.NONE.value


#################
# travel & tourism
#################


@lf()
def travel(x):
    text = x["text"]
    label = x["google_label"]
    if label is not None and label.contains("Travel", config.snorkel_conf_thresh):
        return Topics.TravelTourism.value

    if "travelblog" in text:
        return Topics.TravelTourism.value

    return Topics.NONE.value


#################
# tech & internet
#################

tech_words = ["proxy"]
tech_words = "|".join(tech_words)

search_tech_words = re.compile(r"({})".format(tech_words))

@lf()
def tech_and_internet(x):
    text = x["text"]
    label = x["google_label"]

    if len(search_tech_words.findall(text)) > 3:
        return Topics.TechnologyInternet.value

    if label is not None:
        if label.contains("Hacking & Cracking", config.snorkel_conf_thresh):
            return Topics.TechnologyInternet.value

        if label.contains("Hacking & Cracking", config.snorkel_conf_thresh):
            return Topics.TechnologyInternet.value

        if label.contains("/Internet & Telecom", config.snorkel_conf_thresh):
            return Topics.TechnologyInternet.value

        if label.contains(
            "/Computers & Electronics/Networking/VPN", config.snorkel_conf_thresh
        ):
            return Topics.TechnologyInternet.value

        if label.contains(
            "/Computers & Electronics/Programming", config.snorkel_conf_thresh
        ):
            return Topics.TechnologyInternet.value

        # Software ?
        # if label.contains("/Computers & Electronics/", config.snorkel_conf_thresh):
        #     return Topics.TechnologyInternet.value

    return Topics.NONE.value


###############
# science
###############


@lf()
def science(x):
    label = x["google_label"]
    if label is not None:
        if label.contains("Science", config.snorkel_conf_thresh):
            return Topics.Science.value

    return Topics.NONE.value


#################
# politics & incidents
#################

politicians = ["biden", "donald trump", "hilary clinton", "white house"]
politicians = "|".join(politicians)

search_politicians = re.compile(r"({})".format(politicians))


@lf()
def politics(x):
    text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/News/Politics", config.snorkel_conf_thresh):
            return Topics.PoliticsIncidents.value

    if search_politicians.findall(text):
        return Topics.PoliticsIncidents.value

    return Topics.NONE.value


#################
# sports
#################


@lf()
def sports(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Sports", config.snorkel_conf_thresh):
            return Topics.Sports.value

        if label.contains("/News/Sports", config.snorkel_conf_thresh):
            return Topics.Sports.value

    return Topics.NONE.value


#################
# cars & other vehicles
#################


@lf()
def cars(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Motor", config.snorkel_conf_thresh):
            return Topics.CarsOtherVehicles.value
        if label.contains("Autos & Vehicles", config.snorkel_conf_thresh):
            return Topics.CarsOtherVehicles.value

    return Topics.NONE.value


#################
# offer
#################

drug_words = [
    "coke",
    "crack",
    "thc",
    "weed",
    "cocaine",
    "crystal meth",
    "haze",
    "kush",
    "molly",
    "shroom",
    "pill",
    "lsd",
    "mdma",
    "drug",
    "skunk",
    "og kush",
    "silver haze"
    # TODO this is maybe more marketing
    # some are guns
    # "gun",
    # "glock"
]
drug_words = "|".join(drug_words)
# TODO improve here additionally with has numbers with units
search_drugs = re.compile(r"({})".format(drug_words))

currency_words = [
    "btc",
    r"\$",
    r"€",
    "💰",
    "price",
]
currency_words = "|".join(currency_words)
search_currency = re.compile(r"({})".format(currency_words))

offer_stuff = ["slashdeals.in", "amzn.to", "deals & offers"]
offer_stuff = "|".join(offer_stuff)
search_offer_stuff = re.compile(r"({})".format(offer_stuff))


@lf()
def offer(x):
    text = x["text"]
    label = x["google_label"]

    if len(search_offer_stuff.findall(text)) > 3:
        return Topics.OffersPromotions.value


    if label is not None:
        if label.contains("/Shopping", config.snorkel_conf_thresh):
            return Topics.OffersPromotions.value

        is_sensitive = label.contains("/Sensitive", config.snorkel_conf_thresh)
        is_drugs = len(search_drugs.findall(text)) > 3
        if is_sensitive and is_drugs:
            return Topics.OffersPromotions.value

        # has_currency = search_currency.findall(text)
        # if label.contains("Video Games") and len(has_currency) > 3:
        #     return Topics.OffersPromotions.value

        if label.contains(
            "Autos & Vehicles", config.snorkel_conf_thresh
        ) and label.contains("Shopping", 0.5):
            return Topics.OffersPromotions.value

    return Topics.NONE.value


#################
# religion
#################


@lf()
def religion(x):
    text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains(
            "/People & Society/Religion & Belief", config.snorkel_conf_thresh
        ):
            return Topics.ReligionSpirituality.value

    return Topics.NONE.value


#################
# education
#################


@lf()
def education(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Education/Education", config.snorkel_conf_thresh):
            return Topics.Education.value

        if label.contains("Health Education", config.snorkel_conf_thresh):
            return Topics.Education.value

    return Topics.NONE.value


#################
# job
#################

search_hour_rate = re.compile(r"[\d+][.]?\d+/h")


@lf()
def job(x):
    text = x["text"]
    label = x["google_label"]

    if label is not None:
        # TODO check Jobs/Resumes & Portfolios
        if label.contains("Jobs/Job Listings", config.snorkel_conf_thresh):
            return Topics.JobListings.value

    if search_hour_rate.findall(text):
        return Topics.JobListings.value

    return Topics.NONE.value


#################
# home & architecture
#################


@lf()
def home_architecture(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Home", config.snorkel_conf_thresh):
            return Topics.HomeArchitecture.value

    return Topics.NONE.value


##################
# health & medicine
##################


@lf()
def health_medcine(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Health", config.snorkel_conf_thresh):
            return Topics.HealthMedicine.value

    return Topics.NONE.value


#################
# Bets & Gambling
#################


@lf()
def bets_gambling(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Games/Gambling", config.snorkel_conf_thresh):
            return Topics.BetsGambling.value

        # if label.contains("")

    return Topics.NONE.value


#################
# foods cooking
#################


@lf()
def food_cooking(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains(
            "/Food & Drink/Cooking & Recipes", config.snorkel_conf_thresh
        ):
            return Topics.FoodCooking.value

    return Topics.NONE.value


#################
# music
#################


@lf()
def music(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Arts & Entertainment/Music", config.snorkel_conf_thresh):
            return Topics.Music.value

    return Topics.NONE.value


#################
# HumorMemes
#################


@lf()
def humor_memes(x):
    text = x["text"]
    label = x["google_label"]

    if "bullshit" in text and "meme" in text and "cat" in text:
        return Topics.HumorMemes.value

    if label is not None:
        if label.contains("/Arts & Entertainment/Fun", config.snorkel_conf_thresh):
            return Topics.HumorMemes.value

        if label.contains("/Arts & Entertainment/Humor", config.snorkel_conf_thresh):
            return Topics.HumorMemes.value

    return Topics.NONE.value


#################
# movies
#################


@lf()
def movies(x):
    text = x["text"]
    label = x["google_label"]

    if "mickey kelley" in text:
        return Topics.Movies.value

    if label is not None:
        if label.contains("/Arts & Entertainment/Movies", config.snorkel_conf_thresh):
            return Topics.Movies.value

    return Topics.NONE.value


#################
# pets
#################


@lf()
def pets(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Pets & Animals/Pets", config.snorkel_conf_thresh):
            return Topics.Pets.value

    return Topics.NONE.value


#################
# psychology & relationship
#################


@lf()
def psychology_relationship(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Online Communities/Dating", config.snorkel_conf_thresh):
            return Topics.PsychologyRelationships.value

    return Topics.NONE.value


#################
# art & design
#################


@lf()
def art_design(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Visual Art & Design", config.snorkel_conf_thresh):
            return Topics.ArtDesign.value

    return Topics.NONE.value


#################
# books
#################


@lf()
def books(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Books", config.snorkel_conf_thresh):
            return Topics.Books.value

    return Topics.NONE.value


#################
# fashion & beauty
#################


@lf()
def fashion_beauty(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Fitness/Body", config.snorkel_conf_thresh):
            return Topics.FashionBeauty.value

        if label.contains("Fitness/Face", config.snorkel_conf_thresh):
            return Topics.FashionBeauty.value

        if label.contains("Fitness/Fashion", config.snorkel_conf_thresh):
            return Topics.FashionBeauty.value

        if label.contains("Fitness/Hair", config.snorkel_conf_thresh):
            return Topics.FashionBeauty.value

    return Topics.NONE.value


#################
# fitness
#################


@lf()
def fitness(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Fitness/Fitness", config.snorkel_conf_thresh):
            return Topics.Fitness.value

    return Topics.NONE.value


#################
# business entrepreneuship
#################


# TODO
# @lf()
# def business_entrepreneurship(x):
#     # text = x["text"]
#     label = x["google_label"]

#     if label is not None:
#         if label.contains("Fitness/Fitness", config.snorkel_conf_thresh):
#             return Topics.Fitness.value

#     return Topics.NONE.value

#################
# directories of channels & bots
#################

payment_bot_channel = r"live paypal .* stats sent .* bot"
search_payment_bot = re.compile(payment_bot_channel)

bot_names = r"@[a-zA-Z0-9]+_bot"
search_bot_names = re.compile(bot_names)

search_registration_date = re.compile(r"registration date:")

fixed_names = ["@awsproxie"]
fixed_names = "|".join(fixed_names)

search_fixed_bot = re.compile("({})".format(fixed_names))

@lf()
def directories_of_channels_and_bots(x):
    text = x["text"]
    label = x["google_label"]

    # TODO doesnt work properly
    has_payment_bot = search_payment_bot.findall(text)
    if has_payment_bot:
        return Topics.DirectoriesofChannelsBots.value

    if search_fixed_bot.findall(text):
        return Topics.DirectoriesofChannelsBots.value


    has_bot_name = search_bot_names.findall(text)
    # TODO look at the match and check whether the same name appears that often
    count_bot_names = Counter(has_bot_name)
    if count_bot_names and max(count_bot_names.values()) > 3:
        # print(has_bot_name)
        # print(text)

        return Topics.DirectoriesofChannelsBots.value

    if "tiger trade" in text:
        return Topics.DirectoriesofChannelsBots.value

    if len(search_registration_date.findall(text)) > 3:
        return Topics.DirectoriesofChannelsBots.value

    return Topics.NONE.value


#################
# real estate
#################


@lf()
def real_estate(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Real Estate", config.snorkel_conf_thresh):
            return Topics.Fitness.value

    return Topics.NONE.value


#################
# celebrities
#################


@lf()
def celebrities(x):
    text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("Celebrities", config.snorkel_conf_thresh):
            return Topics.CelebritiesLifestyle.value

    if "Jürgen Klopp" in text:
        return Topics.CelebritiesLifestyle.value

    return Topics.NONE.value


#################
# other
#################

others_words = ["@cyka_blyat_army", "#wallpaper"]
others_words = "|".join(others_words)

search_others_words = re.compile(r"({})".format(others_words))

@lf()
def other(x):
    text = x["text"]
    label = x["google_label"]

    if len(search_others_words.findall(text)) > 3:
        return Topics.Other.value

    if len(re.findall(r"\d+k", text)) > 20:
        return Topics.Other.value

    if label is not None:

        if label.contains(
            "/Online Communities/Blogging Resources & Services",
            config.snorkel_conf_thresh,
        ):
            return Topics.Other.value

        # TODO look at all others
        if label.contains("/Online Communities/File", config.snorkel_conf_thresh):
            return Topics.Other.value

        if label.contains("/Online Communities/Photo", config.snorkel_conf_thresh):
            return Topics.Other.value

        if label.contains("/News Weather", config.snorkel_conf_thresh):
            return Topics.Other.value

    return Topics.NONE.value


#################
# all
#################


@lf()
def dummy1(x):
    return Topics.NONE.value


@lf()
def dummy2(x):
    return Topics.NONE.value


lfs = [
    porn,
    crypto,
    investments,
    video_games,
    travel,
    tech_and_internet,
    science,
    politics,
    sports,
    cars,
    offer,
    religion,
    education,
    job,
    home_architecture,
    health_medcine,
    bets_gambling,
    food_cooking,
    music,
    humor_memes,
    movies,
    pets,
    psychology_relationship,
    art_design,
    books,
    fashion_beauty,
    fitness,
    # business_entrepreneurship,
    directories_of_channels_and_bots,
    real_estate,
    celebrities,
    other,
]
print(len(lfs))


def print_initial_coverage(df, labels, name=""):
    n_samples = len(df)

    where_label = labels != Topics.NONE.value
    where_label = where_label.sum(axis=1) > 0
    n_labeled = where_label.sum()

    pretty = [["Name:", name]]
    pretty += [["n_samples", n_samples]]
    pretty += [["n_labeled", n_labeled]]
    pretty += [["coverage", "{:.2f}%".format(n_labeled / n_samples * 100)]]
    print(tabulate(pretty))

    return where_label


def print_model_coverage(df):
    n_samples = len(df)

    n_labeled = len(df[df["label"] != -1])

    pretty = [["n_samples", n_samples]]
    pretty += [["n_labeled", n_labeled]]
    pretty += [["coverage", "{:.2f}%".format(n_labeled / n_samples * 100)]]
    pretty += [[""]]

    for itopic in range(42):
        this_label = df[df["label"] == itopic]
        pretty += [[Topics(itopic).name, len(this_label)]]

    print(tabulate(pretty))


def look_through_labels(labeled):
    for i in range(len(labeled)):
        ele = labeled.iloc[i]
        print(ele["text"])
        print(Topics(ele["label"]).name)
        glabel = ele["google_label"]
        if glabel is not None:
            print(glabel.data)
        else:
            print(None)

        input()


def write_labels(df_train, labels):
    with open(utils.make_snorkel_out_path(), "w") as f:
        for lidx, label in enumerate(labels):
            has_label = np.any(label != -1)
            if not has_label:
                continue

            df_item = df_train.iloc[lidx]

            # original idx
            ds_idx = df_item["ds_idx"]
            text_idx = df_item["text_idx"]
            text = df_item["text"]
            label_row = ",".join([str(l) for l in label[label != -1]])

            formatted_row = f"{ds_idx};{text_idx};{label_row};{text}"
            print(formatted_row, file=f)


def print_specific_labels(label_df, *labels):
    for label in labels:
        print("FOR:", label)
        where_label = label_df[label_df["labels"] == label.value]
        print(
            *(
                (ds_idx, text_idx)
                for ds_idx, text_idx in zip(
                    where_label["ds_idx"], where_label["text_idx"]
                )
            )
        )

def main():

    lang_used = "en"
    dataset_nums = [0, 1, 2, 3]
    # dataset_nums = [0]  # , 1, 2]

    # datas = [utils.load_data(ds_num, concat=True) for ds_num in dataset_nums]
    all_datas = [utils.load_cleansed_data(ds_num, lang_used) for ds_num in dataset_nums]
    all_raws = [utils.load_raw(ds_num) for ds_num in dataset_nums]
    all_langs = [utils.load_lang(ds_num) for ds_num in dataset_nums]

    combined = []
    # for each tg dataset
    for ds_idx, (data, raw, lang) in enumerate(zip(all_datas, all_raws, all_langs)):
        # for each text in this dataset
        for text_idx, text in data.items():
            # ignore every language except for currently set
            if lang[text_idx] != lang_used:
                continue

            # no response from google previously not classified as english
            if text_idx not in raw:
                continue

            # has a prediction by google
            raw_item = raw[text_idx]
            if len(raw_item) > 2:
                google_labels = GoogleLabel(raw_item)
                combined.append((ds_idx, text_idx, text.lower(), google_labels))
            # has no predicition
            else:
                combined.append((ds_idx, text_idx, text.lower(), None))

    df_train = pd.DataFrame(
        combined, columns=["ds_idx", "text_idx", "text", "google_label"]
    )

    ######## MULTI LABEL
    # applier = PandasLFApplier(lfs=lfs)
    # label_train = applier.apply(df=df_train)

    # model = MajorityLabelVoter(cardinality=42, device="cuda")
    # preds = model.predict_proba(label_train)

    # counter = [0 for _ in range(42)]
    # for pred, (idx, df_item) in zip(preds, df_train.iterrows()):
    #     high_prob_idxs = np.argwhere(pred >= 0.33)
    #     # print(len(high_prob_idxs))
    #     if len(high_prob_idxs) == 0:
    #         continue

    #     hr_labels = [utils.topics[idx[0]] for idx in high_prob_idxs]
    #     print(df_item["text"])

    #     print(hr_labels)
    #     print([pred[idx[0]] for idx in high_prob_idxs])

    #     for idx in high_prob_idxs:
    #         counter[idx[0]] += 1

    #     input()

    # pretty = [["Label", "Count" ], ["Overall", sum(counter)]]
    # for idx, count in enumerate(counter):
    #     pretty += [[utils.topics(idx), count]]

    # print(tabulate(pretty))


    ######## BIN CLASSIFIER
    labeled_data = []
    for lf in lfs:
        used_lfs = [lf, dummy1, dummy2]

        applier = PandasLFApplier(lfs=used_lfs)
        label_train = applier.apply(df=df_train)

        # analysis = LFAnalysis(L=label_train, lfs=used_lfs).lf_summary()
        # print(analysis)
        where_label = print_initial_coverage(df_train, label_train, lf.name)

        # cardinality = 42
        label_model = LabelModel(cardinality=42, verbose=1, device="cuda")
        label_model.fit(label_train, n_epochs=500, log_freq=50, seed=1337)
        labeled = label_model.predict(L=label_train, tie_break_policy="abstain")

        labeled_data.append(labeled.reshape(-1, 1))

    labeled_data = np.hstack(labeled_data)
    print(labeled_data)

    write_labels(df_train, labeled_data)

    # print_model_coverage(df_train)
    # print_specific_labels(df_train, Topics.DirectoriesofChannelsBots)


if __name__ == "__main__":
    main()
