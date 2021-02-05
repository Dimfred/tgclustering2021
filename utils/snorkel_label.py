import utils
from utils import Topics
from config import config


import snorkel_defaults as sdf
from snorkel.labeling import PandasLFApplier, LFAnalysis
from snorkel.labeling.model import LabelModel
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
    x = x["text"]
    crypto_words = search_crypto_words.findall(x)
    if len(crypto_words) > 3:
        return Topics.Cryptocurrencies.value

    return Topics.NONE.value


#################
# invest
#################

invest_words = ["forex", "pips", "investment plan", "#invest"]

search_invest_words = r"({})".format("|".join(invest_words))
search_invest_words = re.compile(search_invest_words)


@lf()
def investments(x):
    x = x["text"]
    invest_words = search_invest_words.findall(x)
    if invest_words:
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
    label = x["google_label"]
    if label is not None and label.contains("Travel", config.snorkel_conf_thresh):
        return Topics.TravelTourism.value

    return Topics.NONE.value


#################
# tech & internet
#################


@lf()
def tech_and_internet(x):
    label = x["google_label"]
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


@lf()
def politics(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/News/Politics", config.snorkel_conf_thresh):
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


@lf()
def offer(x):
    text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Shopping", config.snorkel_conf_thresh):
            return Topics.OffersPromotions.value

        is_sensitive = label.contains("/Sensitive", config.snorkel_conf_thresh)
        is_drugs = len(search_drugs.findall(text)) > 3
        if is_sensitive and is_drugs:
            return Topics.OffersPromotions.value

        has_currency = search_currency.findall(text)
        if label.contains("Video Games") and len(has_currency) > 3:
            return Topics.OffersPromotions.value

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
    # text = x["text"]
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


@lf()
def job(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        # TODO check Jobs/Resumes & Portfolios
        if label.contains("Jobs/Job Listings", config.snorkel_conf_thresh):
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
    # text = x["text"]
    label = x["google_label"]

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
    # text = x["text"]
    label = x["google_label"]

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


@lf()
def directories_of_channels_and_bots(x):
    text = x["text"]
    label = x["google_label"]

    # TODO doesnt work properly
    has_payment_bot = search_payment_bot.findall(text)
    if has_payment_bot:
        return Topics.DirectoriesofChannelsBots.value

    has_bot_name = search_bot_names.findall(text)
    # TODO look at the match and check whether the same name appears that often
    count_bot_names = Counter(has_bot_name)
    if count_bot_names and max(count_bot_names.values()) > 3:
        print(has_bot_name)
        print(text)

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
# other
#################


@lf()
def other(x):
    # text = x["text"]
    label = x["google_label"]

    if label is not None:
        if label.contains("/Pets & Animals/Wildlife", config.snorkel_conf_thresh):
            return Topics.Other.value

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
    other,
]
print(len(lfs))


def print_initial_coverage(df, labels):
    n_samples = len(df)

    where_label = labels != Topics.NONE.value
    where_label = where_label.sum(axis=1) > 0
    n_labeled = where_label.sum()

    pretty = [["n_samples", n_samples]]
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


def main():
    data = utils.load_cleansed_data(0)
    raw = utils.load_raw(0)

    combined_data = []
    for idx, text in data:
        r = raw[idx]

        google_labels = r[1:]
        # has google labels
        if len(r) > 2:
            glabel = GoogleLabel(google_labels)
            combined_data.append((idx, text.lower(), glabel))
        else:
            combined_data.append((idx, text.lower(), None))

    df_train = pd.DataFrame(combined_data, columns=["idx", "text", "google_label"])

    applier = PandasLFApplier(lfs=lfs)
    label_train = applier.apply(df=df_train)
    analysis = LFAnalysis(L=label_train, lfs=lfs).lf_summary()
    print(analysis)

    where_label = print_initial_coverage(df_train, label_train)

    # cardinality = 42
    label_model = LabelModel(cardinality=42, verbose=True)
    label_model.fit(label_train, n_epochs=500, log_freq=50, seed=1337)
    df_train["label"] = label_model.predict(L=label_train, tie_break_policy="abstain")

    print_model_coverage(df_train)


if __name__ == "__main__":
    main()
