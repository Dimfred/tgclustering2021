from config import config

with open(config.porn_websites, "r") as f:
    porn_websites = f.readlines()
    porn_websites = [l.strip() for l in porn_websites]
    porn_websites = [l for l in porn_websites if l]
