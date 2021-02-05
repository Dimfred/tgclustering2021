import re


text = "textxvideos.com www.google.com nudevista.com https://www.xvideos.com www.xvideos.com https://xvideos.com https://"

pattern = r"((https://|www.|http://|https://www.|http://www.)(xvideos.com|nudevista.com|clip4sale.com))"

matcher = re.compile(pattern)

matches = matcher.findall(text)

print(matches)
