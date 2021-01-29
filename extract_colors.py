import os
import json
from  matplotlib import image
import numpy as np

import matplotlib.pyplot as plt


def rgb_to_hex(rgb):
    rgb = np.round(rgb).astype(int)
    hx = '#'
    for v in rgb:
        hx += '{:02X}'.format(v)
    return hx

def load_colors(fname='colors_plain.json'):
    with open(fname) as file:
        colors = json.load(file)
    return colors

img_dir = 'color_samples/'
img_names = sorted(os.listdir(img_dir))

colors = load_colors(fname='colors_plain.json')

for iname in img_names:
    print('Extracting from {}...'.format(iname))
    img = np.array(image.imread('{}{}'.format(img_dir, iname)))
    nx = img.shape[1]
    cols = []
    dx = 100
    for i in range(3):
        # Sample the different intensities
        # col = np.mean(img[:, i*nx//3:(i+1)*nx//3], axis=1)
        col = np.mean(img[:, int((i+0.5)*nx/3 - dx/2):int((i+0.5)*nx/3 + dx/2)], axis=1)
        col = np.mean(col, axis=0)
        # print(col)
        cols.append(col)
    for i in range(3):
        # x = int(i*nx/3 + nx/6)
        x = int(i*nx/3)
        img[1:65, x+1:x+nx//6] = cols[i]
        img[65, x+1:x+nx//6] = (nx//6 - 1)*[[0, 0, 0]]
        img[1:65, x+nx//6] = (65 - 1)*[[0, 0, 0]]
        if i > 0:
            img[:, int(i*nx/3)] = img.shape[0]*[[0, 0, 0]]
    cols = [rgb_to_hex(col) for col in cols]
    ccode = iname[:-4]
    cname = colors[ccode][1]
    colors[ccode] = [0, 0, 0, 0]
    for i in range(3):
        colors[ccode][i] = cols[i]
    colors[ccode][3] = cname
    image.imsave("samples_annotated/{}".format(iname), img)
    # plt.imshow(img)
    # plt.show()

with open('colors_auto.json', 'w') as file:
    json.dump(colors, file, sort_keys=True, indent='    ')
