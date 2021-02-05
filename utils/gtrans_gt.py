from google_trans_new import google_translator
import concurrent.futures
import time
import json
import re

detector = google_translator()

"""
def translate(line):
    line_old = line
    print (line_old)
    line = line.replace('title', '')
    line = line.replace('"description"', '')
    line = line.replace('"recent_posts"', '')
    print(detector.detect(line_old))

    print(line_old)
    return line_old


with open(".\\dc0130-input\\dc0130-input.txt", 'r', encoding="utf8") as inputfile:
    with open (".\\output.txt", 'w+', encoding="utf-8") as outputfile:
        with concurrent.futures.ThreadPoolExecutor(max_workers=18) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(translate, line): line for line in inputfile}
            for future in concurrent.futures.as_completed(future_to_url):
                res = future_to_url[future]
                outputfile.write(res)

"""


with open("./data/tg/data0.txt", 'r', encoding="utf8") as inputfile:
    lines = inputfile.readlines()

with open("./output.txt", "r", encoding="utf8") as f:
    olines = f.readlines()
    offset = len(olines)


for line in lines[25001+offset:]:
    newline = line
    if len(line) > 3800:
        newline = line[0:3800]

    det = str(detector.detect(newline)[0])
    with open("output.txt", 'a', encoding="utf-8") as outputfile:
        outputfile.write(det + ";" + line)






