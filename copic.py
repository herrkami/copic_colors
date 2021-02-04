import json
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs

families_grays = [
    'C',
    'N',
    'T',
    'W',
    ]
families_color = [
    'B',
    'BV',
    'V',
    'RV',
    'R',
    'YR',
    'Y',
    'YG',
    'G',
    'BG',
    ]
families_flourescent = [
    'FB',
    'FV',
    'FRV',
    'FYR',
    'FY',
    'FYG',
    'FBG',
    ]
hue_parity = {
    'B': 1,
    'BV': 1,
    'V': 1,
    'RV': -1,
    'R': -1,
    'YR': 1,
    'Y': -1,
    'YG': -1,
    'G': -1,
    'BG': -1,
    }

def load_colors(fname='colors.json'):
    with open(fname) as file:
        colors = json.load(file)
    return colors

def get_families(colors):
    fams = []
    for ccode in colors.keys():
        fams.append(ccode.rstrip('0123456789'))
    fams = np.unique(fams)
    return fams

def get_blending_groups(colors, family, parity_correction=False):
    bgroups = []
    for ccode in colors.keys():
        if ccode.rstrip('0123456789-') == family:
            if '-' in ccode:
                # bgroups.append(ccode[len(family)+1:])
                bgroups.append('-')
            else:
                bgroups.append(ccode[len(family)])
    bgs = np.sort(np.unique(bgroups))
    if parity_correction:
        bgs = bgs[::hue_parity[family]]
    return bgs

def get_intensity(ccode):
    fam = ccode.rstrip('0123456789-')
    intensity = ccode[len(fam)+1:]
    return intensity

def get_pens(colors, ccode):
    pens = colors[ccode][4]
    return pens

def filter_by_family(colors, family):
    cols = {}
    for ccode in colors.keys():
        fam = ccode.rstrip('0123456789-')
        if fam == family:
            cols[ccode] = colors[ccode]
    return cols

def filter_by_intensity(colors, intensity):
    cols = {}
    for ccode in colors.keys():
        itst = get_intensity(ccode)
        if itst == intensity:
            cols[ccode] = colors[ccode]
    return cols

def filter_by_pen(colors, pen):
    cols = {}
    for ccode in colors.keys():
        pens = get_pens(colors, ccode)
        if pen in pens:
            cols[ccode] = colors[ccode]
    return cols

def get_hue_list(colors, parity_correction=False):
    fbgs = [[f, get_blending_groups(colors, f, parity_correction)] for f in families_color]
    hues = []
    for fbg in fbgs:
        for gb in fbg[1]:
            # hues.append('{}{}'.format(fbg[0], gb))
            hues.append([fbg[0], gb])
    return hues

def get_grays_list(colors):
    fbgs = [[f, get_blending_groups(colors, f, False)] for f in families_grays]
    hues = []
    for fbg in fbgs:
        for bg in fbg[1]:
            # hues.append('{}{}'.format(fbg[0], bg))
            hues.append([fbg[0], bg])
    return hues

def get_earth_list(colors):
    elist = [['E', bg] for bg in get_blending_groups(colors, 'E', False)]
    return elist

def get_intensity_list(colors, hue):
    '''
        hue : list like [<family name>, <blending group>]
    '''
    fcolors = filter_by_family(colors, hue[0])
    ilist = []
    for ccode in fcolors.keys():
        fc = ccode[len(hue[0]):]
        if fc.startswith(hue[1]):
            ilist.append(fc[1:])
    return ilist

def get_color_entry(colors, ccode):
    '''
        ccode : list like [<family name>, <blending group>, <intensity>] or str
    '''
    if type(ccode) == list:
        _ccode = ccode[0] + ccode[1] + ccode[2]
    return colors[_ccode]

def get_color_value(colors, ccode):
    '''
        ccode : list like [<family name>, <blending group>, <intensity>]
    '''
    entry = get_color_entry(colors, ccode)
    return entry[0]

def get_color_values(colors, ccode):
    '''
        ccode : list like [<family name>, <blending group>, <intensity>]
    '''
    entry = get_color_entry(colors, ccode)
    return entry[:3]

def get_color_name(colors, ccode):
    '''
        ccode : list like [<family name>, <blending group>, <intensity>]
    '''
    entry = get_color_entry(colors, ccode)
    return entry[1]

def get_luminosity(color):
    c = color
    rgb = [int(c[i:i+2], base=16)/255. for i in [1, 3, 5]]
    l = cs.rgb_to_hls(rgb[0], rgb[1], rgb[2])[1]
    return l

def plot_color_circle(ax, colors, pos=(0, 0), r=3, outer_color=None):
    hlist = get_hue_list(colors, parity_correction=True)
    nr_hues = len(hlist)
    for idx, hue in enumerate(hlist):
        phi = 2*np.pi*idx/nr_hues
        phi += np.pi
        xs = [s*r*np.cos(phi) + pos[0] for s in [0.65, 0.8, 1]]
        ys = [s*r*np.sin(phi) + pos[1] for s in [0.65, 0.8, 1]]
        ilist = np.unique(get_intensity_list(colors, hue))
        assert len(ilist) == 1
        intensity = ilist[0]
        cols = get_color_values(colors, [hue[0], hue[1], intensity])
        ccode = '{}{}{}'.format(hue[0], hue[1], intensity)
        for i in range(3):
            ms = 0.5*(1 + i/2)*20
            # if (outer_color is not None) and (i == 2):
            if i == 2:
                if 'classic' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.13*r*np.cos(phi),
                            ys[i] + 0.13*r*np.sin(phi),
                            marker=(4, 0, np.rad2deg(phi)+45), color='#000000',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.2*ms)
                if 'ciao' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.17*r*np.cos(phi),
                            ys[i] + 0.17*r*np.sin(phi),
                            'o', color='#FFFFFF',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.15*ms)
                if 'wide' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.21*r*np.cos(phi),
                            ys[i] + 0.21*r*np.sin(phi),
                            marker=(2, 0, np.rad2deg(phi)), color='#FFFFFF',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.17*ms)

            ax.plot(xs[i], ys[i], 'o', color=cols[i], ms=ms)
        if get_luminosity(cols[-1]) < 0.45:
            tcolor = 'white'
        else:
            tcolor = 'black'
        ax.text(xs[-1], ys[-1], ccode,
                fontsize=6, ha='center', va='center', color=tcolor)


def plot_earth_grays_circle(ax, colors, pos=(0, 0), r=3, outer_color=None):
    elist = get_earth_list(colors)
    glist = get_grays_list(colors)
    hlist = elist + glist
    nr_hues = len(hlist)
    for idx, hue in enumerate(hlist):
        phi = 2*np.pi*idx/nr_hues
        phi += np.pi
        xs = [s*r*np.cos(phi) + pos[0] for s in [0.65, 0.8, 1]]
        ys = [s*r*np.sin(phi) + pos[1] for s in [0.65, 0.8, 1]]
        ilist = np.unique(get_intensity_list(colors, hue))
        assert len(ilist) == 1
        intensity = ilist[0]
        cols = get_color_values(colors, [hue[0], hue[1], intensity])
        ccode = '{}{}{}'.format(hue[0], hue[1], intensity)
        for i in range(3):
            ms = 0.5*(1 + i/2)*20
            if i == 2:
                if 'classic' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.13*r*np.cos(phi),
                            ys[i] + 0.13*r*np.sin(phi),
                            marker=(4, 0, np.rad2deg(phi)+45), color='#000000',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.2*ms)
                if 'ciao' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.17*r*np.cos(phi),
                            ys[i] + 0.17*r*np.sin(phi),
                            'o', color='#FFFFFF',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.15*ms)
                if 'wide' in get_pens(colors, ccode):
                    ax.plot(xs[i] + 0.21*r*np.cos(phi),
                            ys[i] + 0.21*r*np.sin(phi),
                            marker=(2, 0, np.rad2deg(phi)), color='#FFFFFF',
                            markeredgecolor=outer_color,
                            markeredgewidth=0.5,
                            ms=0.17*ms)

            ax.plot(xs[i], ys[i], 'o', color=cols[i], ms=ms)
        if get_luminosity(cols[-1]) < 0.45:
            tcolor = 'white'
        else:
            tcolor = 'black'
        ax.text(xs[-1], ys[-1], '{}{}{}'.format(hue[0], hue[1], intensity),
                fontsize=6, ha='center', va='center', color=tcolor)

if __name__ == '__main__':
    _colors = load_colors('colors_auto.json')
    # _colors = filter_by_pen(_colors, 'classic')
    for i in ['000', '00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        plotname = 'copic_circles_intensity_{}'.format(i)
        print('Generating {}...'.format(plotname))
        colors = filter_by_intensity(_colors, i)
        aspect = 16/8
        fig = plt.figure(figsize=(10, 10/aspect))
        ax = fig.add_subplot(111)
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1/aspect])
        plot_color_circle(ax, colors, (.25, .5/aspect), r=.4/aspect, outer_color='k')
        plot_earth_grays_circle(ax, colors, (0.75, .5/aspect), r=.4/aspect, outer_color='k')
        ax.axis(False)
        plt.savefig('img/{}.svg'.format(plotname), bbox_inches='tight', pad_inches=-.0)
        # plt.show()

    # hlist = get_hue_list(colors, parity_correction=True)
    # for x, hue in enumerate(hlist):
    #     ilist = get_intensity_list(colors, hue)
    #     for i in ilist:
    #         col = get_color_value(colors, [hue[0], hue[1], i])
    #         if i == '000':
    #             y = -2
    #         elif i =='00':
    #             y = -1
    #         else:
    #             y = int(i)
    #         ax.plot(x, y, 'o', color=col, ms=20)
    #         ax.text(x, y, '{}{}{}'.format(hue[0], hue[1], i), fontsize=6, ha='center', va='center')
