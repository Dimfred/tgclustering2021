import time

from config import config
import json
import enum


def seed(*args):
    if "tf" in args:
        import tensorflow as tf

        tf.random.set_seed(1337)

    if "np" in args:
        import numpy as np

        np.random.seed(42)


def stopwatch(name):
    def _stopwatch(f):
        def _deco(*args, **kwargs):
            start = time.perf_counter()
            ret = f(*args, **kwargs)
            end = time.perf_counter()
            print("{}::took:{:.3f}s".format(name, end - start))

            return ret

        return _deco

    return _stopwatch


def make_raw_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-raw.txt"


def make_lang_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-lang.txt"


def make_topic_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-topic.txt"


def make_data_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-data.txt"


def make_cleansed_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-cleansed.txt"


def make_cleansed_data_path(num):
    return config.tg_ds / f"{str(num).zfill(2)}-cleansed-data.txt"


def load_raw(num):
    path = make_raw_path(num)
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [l.strip().split(",") for l in lines]
    return lines


def load_data(num):
    path = make_data_path(num)
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [json.loads(l.strip()) for l in lines]
    return lines


def load_lang(num):
    path = make_lang_path(num)
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [l.strip().split(",") for l in lines]
    return lines


def load_topics():
    path = config.topics
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]
    return lines


def load_cleansed(num):
    path = make_cleansed_path(num)
    with open(path, "r") as f:
        lines = f.readlines()

    # filter empty lines out
    lines = [l.strip() for l in lines if len(l.split(" ", 1)) > 1]

    # split by id, data
    lines = [l.split(" ", 1) for l in lines]

    def to_idx(s):
        s = s.replace("__doc_ind_", "")
        s = s.replace(":", "")
        return int(s)

    # convert id to idx
    lines = [(to_idx(id_), text) for id_, text in lines]

    return lines


def load_cleansed_data(num):
    path = make_cleansed_data_path(num)
    with open(path, "r") as f:
        lines = f.readlines()

    lines = [l.strip().split(",", 1) for l in lines]
    lines = [(int(idx), text) for idx, text in lines]
    return lines


def flatten(list_of_lists):
    flattened = []
    for l in list_of_lists:
        flattened.extend(l)

    return flattened


topics = [
    "Art & Design",
    "Bets & Gambling",
    "Books",
    "Business & Entrepreneurship",
    "Cars & Other Vehicles",
    "Celebrities & Lifestyle",
    "Cryptocurrencies",
    "Culture & Events",
    "Curious Facts",
    "Directories of Channels & Bots",
    "Economy & Finance",
    "Education",
    "Erotic Content",
    "Fashion & Beauty",
    "Fitness",
    "Food & Cooking",
    "Foreign Languages",
    "Health & Medicine",
    "History",
    "Hobbies & Activities",
    "Home & Architecture",
    "Humor & Memes",
    "Investments",
    "Job Listings",
    "Kids & Parenting",
    "Marketing & PR",
    "Motivation & Self-Development",
    "Movies",
    "Music",
    "Offers & Promotions",
    "Pets",
    "Politics & Incidents",
    "Psychology & Relationships",
    "Real Estate",
    "Recreation & Entertainment",
    "Religion & Spirituality",
    "Science",
    "Sports",
    "Technology & Internet",
    "Travel & Tourism",
    "Video Games",
    "Other",
]

class Topics(enum.Enum):
    NONE = -1
    ArtDesign = 0 # DONE
    BetsGambling = 1 # DONE
    Books = 2 # DONE
    BusinessEntrepreneurship = 3
    CarsOtherVehicles = 4 # DONE
    CelebritiesLifestyle = 5
    Cryptocurrencies = 6 # TODO problems with invest
    CultureEvents = 7
    CuriousFacts = 8
    DirectoriesofChannelsBots = 9 # DONE
    EconomyFinance = 10
    Education = 11 # DONE
    EroticContent = 12 # DONE
    FashionBeauty = 13 # DONE
    Fitness = 14 # DONE
    FoodCooking = 15 # DONE
    ForeignLanguages = 16
    HealthMedicine = 17 # DONE
    History = 18
    HobbiesActivities = 19
    HomeArchitecture = 20 # DONE
    HumorMemes = 21 # DONE
    Investments = 22 # TODO problems with crypto
    JobListings = 23 # DONE
    KidsParenting = 24
    MarketingPR = 25
    MotivationSelfDevelopment = 26
    Movies = 27 # DONE
    Music = 28 # DONE
    OffersPromotions = 29
    Pets = 30 # DONE
    PoliticsIncidents = 31 # DONE
    PsychologyRelationships = 32 # Relationship at least
    RealEstate = 33 # DONE
    RecreationEntertainment = 34
    ReligionSpirituality = 35 # DONE
    Science = 36 # DONE
    Sports = 37 # DONE
    TechnologyInternet = 38 # DONE
    TravelTourism = 39 # DONE
    VideoGames = 40 # TODO interference with crypto
    Other = 41

    # TODO look at /Law & Government


mapped_topics = {
    "art": "Art & Design",
    "bet": "Bets & Gambling",
    "book": "Books",
    "busi": "Business & Entrepreneurship",
    "car": "Cars & Other Vehicles",
    "cel": "Celebrities & Lifestyle",
    "cry": "Cryptocurrencies",
    "cule": "Culture & Events",
    "fac": "Curious Facts",
    "bot": "Directories of Channels & Bots",
    "eco": "Economy & Finance",
    "edu": "Education",
    "ero": "Erotic Content",
    "fas": "Fashion & Beauty",
    "fit": "Fitness",
    "food": "Food & Cooking",
    "lang": "Foreign Languages",
    "hlt": "Health & Medicine",
    "hist": "History",
    "hob": "Hobbies & Activities",
    "home": "Home & Architecture",
    "meme": "Humor & Memes",
    "inv": "Investments",
    "job": "Job Listings",
    "kid": "Kids & Parenting",
    "pr": "Marketing & PR",
    "moti": "Motivation & Self-Development",
    "mov": "Movies",
    "mus": "Music",
    "of": "Offers & Promotions",
    "pet": "Pets",
    "pol": "Politics & Incidents",
    "psy": "Psychology & Relationships",
    "re": "Real Estate",
    "enter": "Recreation & Entertainment",
    "reli": "Religion & Spirituality",
    "sci": "Science",
    "spo": "Sports",
    "tec": "Technology & Internet",
    "trav": "Travel & Tourism",
    "gm": "Video Games",
    "ot": "Other",
    # "no": "NOTENGLISH",
}

# nlp_cloud_to_tg_map = {
#     "/Adult": "ero",
#     "/Arts & Entertainment":
#     "/Arts & Entertainment/Comics & Animation/Anime & Manga":
#     "/Arts & Entertainment/Fun & Trivia":
#     "/Arts & Entertainment/Fun & Trivia/Fun Tests & Silly Surveys":
#     "/Arts & Entertainment/Humor":
#     "/Arts & Entertainment/Humor/Funny Pictures & Videos":
#     "/Arts & Entertainment/Movies": "mov",
#     "/Arts & Entertainment/Music & Audio": "mus",
#     "/Arts & Entertainment/Music & Audio/Music Equipment & Technology": "mus",
#     "/Arts & Entertainment/Music & Audio/Radio": "mus",
#     "/Arts & Entertainment/Music & Audio/Religious Music": "mus",
#     "/Arts & Entertainment/Music & Audio/Rock Music": "mus",
#     "/Arts & Entertainment/Music & Audio/Urban & Hip-Hop": "mus",
#     "/Arts & Entertainment/Music & Audio/World Music": "mus",
#     "/Arts & Entertainment/Online Media":
#     "/Arts & Entertainment/Online Media/Online Image Galleries":
#     "/Arts & Entertainment/TV & Video":
#     "/Arts & Entertainment/TV & Video/Online Video":
#     "/Arts & Entertainment/TV & Video/TV Shows & Programs":
#     "/Arts & Entertainment/Visual Art & Design":
#     "/Arts & Entertainment/Visual Art & Design/Architecture":
#     "/Arts & Entertainment/Visual Art & Design/Photographic & Digital Arts":
#     "/Autos & Vehicles": "car",
#     "/Autos & Vehicles/Motor Vehicles (By Type)": "car",
#     "/Autos & Vehicles/Vehicle Parts & Services/Vehicle Parts & Accessories": "car"
#     "/Beauty & Fitness":
#     "/Beauty & Fitness/Body Art": "fas",
#     "/Beauty & Fitness/Face & Body Care": "fas",
#     "/Beauty & Fitness/Face & Body Care/Hygiene & Toiletries": "fas",
#     "/Beauty & Fitness/Face & Body Care/Perfumes & Fragrances": "fas",
#     "/Beauty & Fitness/Face & Body Care/Skin & Nail Care": "fas",
#     "/Beauty & Fitness/Fashion & Style": "fas",
#     "/Beauty & Fitness/Fashion & Style/Fashion Designers & Collections": "fas",
#     "/Beauty & Fitness/Fitness": "fit",
#     "/Beauty & Fitness/Hair Care": "fac",
#     "/Books & Literature": "book",
#     "/Books & Literature/Fan Fiction": "book",
#     "/Business & Industrial":
#     "/Business & Industrial/Aerospace & Defense/Space Technology":
#     "/Business & Industrial/Agriculture & Forestry":
#     "/Business & Industrial/Business Operations":
#     "/Business & Industrial/Business Services":
#     "/Business & Industrial/Business Services/E-Commerce Services":
#     "/Business & Industrial/Business Services/Office Supplies":
#     "/Business & Industrial/Chemicals Industry":
#     "/Business & Industrial/Chemicals Industry/Plastics & Polymers":
#     "/Business & Industrial/Construction & Maintenance/Building Materials & Supplies":
#     "/Business & Industrial/Pharmaceuticals & Biotech":
#     "/Business & Industrial/Small Business/MLM & Business Opportunities":
#     "/Computers & Electronics":
#     "/Computers & Electronics/Computer Hardware":
#     "/Computers & Electronics/Computer Hardware/Computer Components":
#     "/Computers & Electronics/Computer Hardware/Computer Peripherals":
#     "/Computers & Electronics/Computer Hardware/Laptops & Notebooks":
#     "/Computers & Electronics/Computer Security":
#     "/Computers & Electronics/Computer Security/Hacking & Cracking":
#     "/Computers & Electronics/Consumer Electronics":
#     "/Computers & Electronics/Consumer Electronics/Game Systems & Consoles":
#     "/Computers & Electronics/Enterprise Technology":
#     "/Computers & Electronics/Networking/VPN & Remote Access":
#     "/Computers & Electronics/Programming":
#     "/Computers & Electronics/Programming/Java (Programming Language)":
#     "/Computers & Electronics/Software":
#     "/Computers & Electronics/Software/Business & Productivity Software":
#     "/Computers & Electronics/Software/Internet Software":
#     "/Computers & Electronics/Software/Multimedia Software":
#     "/Finance":
#     "/Finance/Accounting & Auditing":
#     "/Finance/Accounting & Auditing/Tax Preparation & Planning":
#     "/Finance/Banking":
#     "/Finance/Credit & Lending":
#     "/Finance/Credit & Lending/Credit Reporting & Monitoring":
#     "/Finance/Credit & Lending/Loans":
#     "/Finance/Insurance":
#     "/Finance/Investing":
#     "/Finance/Investing/Commodities & Futures Trading":
#     "/Finance/Investing/Currencies & Foreign Exchange":
#     "/Finance/Investing/Stocks & Bonds":
#     "/Food & Drink":
#     "/Food & Drink/Cooking & Recipes":
#     "/Food & Drink/Food/Snack Foods":
#     "/Food & Drink/Restaurants":
#     "/Food & Drink/Restaurants/Fast Food":
#     "/Food & Drink/Restaurants/Pizzerias":
#     "/Games":
#     "/Games/Card Games/Poker & Casino Games":
#     "/Games/Computer & Video Games":
#     "/Games/Computer & Video Games/Casual Games":
#     "/Games/Computer & Video Games/Fighting Games":
#     "/Games/Computer & Video Games/Sandbox Games":
#     "/Games/Computer & Video Games/Shooter Games":
#     "/Games/Computer & Video Games/Sports Games":
#     "/Games/Gambling":
#     "/Games/Gambling/Lottery":
#     "/Games/Online Games/Massively Multiplayer Games":
#     "/Games/Roleplaying Games":
#     "/Games/Table Games":
#     "/Health":
#     "/Health/Health Conditions":
#     "/Health/Health Conditions/Infectious Diseases":
#     "/Health/Health Education & Medical Training":
#     "/Health/Medical Facilities & Services/Medical Procedures":
#     "/Health/Oral & Dental Care":
#     "/Health/Pharmacy/Drugs & Medications":
#     "/Health/Public Health":
#     "/Health/Substance Abuse/Steroids & Performance-Enhancing Drugs":
#     "/Health/Vision Care":
#     "/Hobbies & Leisure":
#     "/Hobbies & Leisure/Special Occasions/Holidays & Seasonal Events":
#     "/Home & Garden":
#     "/Home & Garden/Bed & Bath":
#     "/Home & Garden/Home Appliances":
#     "/Home & Garden/Home Furnishings":
#     "/Home & Garden/Home Improvement/Flooring":
#     "/Home & Garden/Kitchen & Dining/Small Kitchen Appliances":
#     "/Internet & Telecom":
#     "/Internet & Telecom/Mobile & Wireless":
#     "/Internet & Telecom/Mobile & Wireless/Mobile Apps & Add-Ons":
#     "/Internet & Telecom/Mobile & Wireless/Mobile Phones":
#     "/Internet & Telecom/Service Providers":
#     "/Internet & Telecom/Web Services":
#     "/Internet & Telecom/Web Services/Web Design & Development":
#     "/Jobs & Education":
#     "/Jobs & Education/Education":
#     "/Jobs & Education/Education/Colleges & Universities":
#     "/Jobs & Education/Education/Primary & Secondary Schooling (K-12)":
#     "/Jobs & Education/Education/Standardized & Admissions Tests":
#     "/Jobs & Education/Education/Teaching & Classroom Resources":
#     "/Jobs & Education/Jobs/Job Listings":
#     "/Jobs & Education/Jobs/Resumes & Portfolios":
#     "/Law & Government/Government":
#     "/Law & Government/Government/Visa & Immigration":
#     "/Law & Government/Legal":
#     "/Law & Government/Legal/Legal Education":
#     "/Law & Government/Military":
#     "/Law & Government/Public Safety":
#     "/Law & Government/Public Safety/Law Enforcement":
#     "/Law & Government/Social Services":
#     "/News":
#     "/News/Business News":
#     "/News/Politics":
#     "/News/Sports News":
#     "/News/Weather":
#     "/Online Communities":
#     "/Online Communities/Blogging Resources & Services":
#     "/Online Communities/Dating & Personals":
#     "/Online Communities/Dating & Personals/Matrimonial Services":
#     "/Online Communities/File Sharing & Hosting":
#     "/Online Communities/Photo & Video Sharing":
#     "/Online Communities/Photo & Video Sharing/Photo & Image Sharing":
#     "/Online Communities/Social Networks":
#     "/Online Communities/Virtual Worlds":
#     "/People & Society":
#     "/People & Society/Family & Relationships/Family":
#     "/People & Society/Religion & Belief":
#     "/People & Society/Social Issues & Advocacy":
#     "/People & Society/Social Issues & Advocacy/Work & Labor Issues":
#     "/People & Society/Social Sciences/Political Science":
#     "/Pets & Animals/Pets/Dogs":
#     "/Pets & Animals/Wildlife":
#     "/Reference/General Reference/Biographies & Quotations":
#     "/Reference/General Reference/Dictionaries & Encyclopedias":
#     "/Reference/Language Resources":
#     "/Reference/Language Resources/Foreign Language Resources":
#     "/Science":
#     "/Science/Astronomy":
#     "/Science/Biological Sciences":
#     "/Science/Chemistry":
#     "/Science/Computer Science":
#     "/Science/Engineering & Technology":
#     "/Science/Mathematics":
#     "/Science/Physics":
#     "/Sensitive Subjects":
#     "/Shopping":
#     "/Shopping/Apparel":
#     "/Shopping/Apparel/Athletic Apparel":
#     "/Shopping/Apparel/Casual Apparel":
#     "/Shopping/Apparel/Children's Clothing":
#     "/Shopping/Apparel/Clothing Accessories":
#     "/Shopping/Apparel/Eyewear":
#     "/Shopping/Apparel/Footwear":
#     "/Shopping/Apparel/Women's Clothing":
#     "/Shopping/Auctions":
#     "/Shopping/Consumer Resources/Coupons & Discount Offers":
#     "/Sports":
#     "/Sports/Animal Sports":
#     "/Sports/Combat Sports/Wrestling":
#     "/Sports/Fantasy Sports":
#     "/Sports/Individual Sports":
#     "/Sports/Individual Sports/Racquet Sports":
#     "/Sports/Motor Sports":
#     "/Sports/Team Sports":
#     "/Sports/Team Sports/American Football":
#     "/Sports/Team Sports/Baseball":
#     "/Sports/Team Sports/Basketball":
#     "/Sports/Team Sports/Cricket":
#     "/Sports/Team Sports/Hockey":
#     "/Sports/Team Sports/Soccer":
#     "/Travel":
#     "/Travel/Air Travel":
#     "/Travel/Bus & Rail":
#     "/Travel/Hotels & Accommodations":
# }
