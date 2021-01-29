import json
import urllib.request

def load_colors(fname='colors.json'):
    with open(fname) as file:
        colors = json.load(file)
    return colors

colors = load_colors('colors_plain.json')
ccodes = colors.keys()

for i, ccode in enumerate(ccodes):
    print('Fetching color {} ({}/{})'.format(ccode, i, len(ccodes)))
    lname = 'https://copic.jp/images/color/Sample_{}@2x.jpg'.format(ccode)
    urllib.request.urlretrieve(
        lname,
        'color_samples/{}.jpg'.format(ccode))
