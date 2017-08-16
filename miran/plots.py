import os.path
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# THIS ARE BASIC PLOTTING SETTINGS TO HOMOGENEIZE THE GRAPHS WITH THE STYLE OF THE THESIS
mpl.rc('font',**{'family':'serif','serif':['Times']})
mpl.rc('xtick', labelsize=8)
mpl.rc('ytick', labelsize=8)
mpl.rc('axes', labelsize=9)
mpl.rc('text', usetex=True)

# DISCARDED OPTIONS
#plt.rc('font', family='sans-serif', serif='Avant Garde')
#plt.rc('xtick', labelsize=6)
#plt.rc('ytick', labelsize=7)
#plt.rc('axes', labelsize=9)

key_templates = {

    'bgate': np.array([[1., 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.77, 0.00, 0.38, 0.21, 0.30],
                       [1., 0.00, 0.36, 0.39, 0.00, 0.38, 0.00, 0.74, 0.27, 0.00, 0.42, 0.23]]),

    # almost identical to bgate. kept for backwards compatibility
    'bmtg3': np.array([[1.00, 0.00, 0.42, 0.00, 0.53, 0.37, 0.00, 0.76, 0.00, 0.38, 0.21, 0.30],
                       [1.00, 0.00, 0.36, 0.39, 0.10, 0.37, 0.00, 0.76, 0.27, 0.00, 0.42, 0.23]]),

    'bmtg2': np.array([[1.00, 0.10, 0.42, 0.10, 0.53, 0.37, 0.10, 0.77, 0.10, 0.38, 0.21, 0.30],
                       [1.00, 0.10, 0.36, 0.39, 0.29, 0.38, 0.10, 0.74, 0.27, 0.10, 0.42, 0.23]]),

    # was originally bmtg1
    'braw': np.array([[1., 0.1573, 0.4200, 0.1570, 0.5296, 0.3669, 0.1632, 0.7711, 0.1676, 0.3827, 0.2113, 0.2965],
                      [1., 0.2330, 0.3615, 0.3905, 0.2925, 0.3777, 0.1961, 0.7425, 0.2701, 0.2161, 0.4228, 0.2272]]),

    'diatonic': np.array([[1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
                          [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1]]),

    'monotonic': np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]),

    'triads': np.array([[1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0]]),

    'edma_ecir': np.array(
        [[0.16519551, 0.04749026, 0.08293076, 0.06687112, 0.09994645, 0.09274123, 0.05294487, 0.13159476, 0.05218986,
          0.07443653, 0.06940723, 0.0642515],
         [0.17235348, 0.05336489, 0.0761009, 0.10043649, 0.05621498, 0.08527853, 0.0497915, 0.13451001, 0.07458916,
          0.05003023,
          0.09187879, 0.05545106]]),

    'edmm_ecir': np.array([[0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083, 0.083],
                           [0.17235348, 0.04, 0.0761009, 0.12, 0.05621498, 0.08527853, 0.0497915, 0.13451001,
                            0.07458916, 0.05003023, 0.09187879,
                            0.05545106]]),

    'edma': np.array([[1., 0.2875, 0.5020, 0.4048, 0.6050, 0.5614, 0.3205, 0.7966, 0.3159, 0.4506, 0.4202, 0.3889],
                      [1., 0.3096, 0.4415, 0.5827, 0.3262, 0.4948, 0.2889, 0.7804, 0.4328, 0.2903, 0.5331, 0.3217]]),

    'edmm': np.array([[1., 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000],
                      [1., 0.2321, 0.4415, 0.6962, 0.3262, 0.4948, 0.2889, 0.7804, 0.4328, 0.2903, 0.5331, 0.3217]]),

    'krumhansl': np.array([[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                           [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]]),

    'temperley99': np.array([[5.0, 2.0, 3.5, 2.0, 4.5, 4.0, 2.0, 4.5, 2.0, 3.5, 1.5, 4.0],
                             [5.0, 2.0, 3.5, 4.5, 2.0, 4.0, 2.0, 4.5, 3.5, 2.0, 1.5, 4.0]]),

    'temperley05': np.array([[0.748, 0.060, 0.488, 0.082, 0.67, 0.46, 0.096, 0.715, 0.104, 0.366, 0.057, 0.4],
                             [0.712, 0.084, 0.474, 0.618, 0.049, 0.46, 0.105, 0.747, 0.404, 0.067, 0.133, 0.33]]),

    'temperley-essen': np.array([[0.184, 0.001, 0.155, 0.003, 0.191, 0.109, 0.005, 0.214, 0.001, 0.078, 0.004, 0.055],
                                 [0.192, 0.005, 0.149, 0.179, 0.002, 0.144, 0.002, 0.201, 0.038, 0.012, 0.053, 0.022]]),

    'thpcp': np.array(
        [[0.95162, 0.20742, 0.71758, 0.22007, 0.71341, 0.48841, 0.31431, 1.00000, 0.20957, 0.53657, 0.22585, 0.55363],
         [0.94409, 0.21742, 0.64525, 0.63229, 0.27897, 0.57709, 0.26428, 1.0000, 0.26428, 0.30633, 0.45924, 0.35929]]),

    'shaath': np.array([[6.6, 2.0, 3.5, 2.3, 4.6, 4.0, 2.5, 5.2, 2.4, 3.7, 2.3, 3.4],
                        [6.5, 2.7, 3.5, 5.4, 2.6, 3.5, 2.5, 5.2, 4.0, 2.7, 4.3, 3.2]]),

    'gomez': np.array([[0.82, 0.00, 0.55, 0.00, 0.53, 0.30, 0.08, 1.00, 0.00, 0.38, 0.00, 0.47],
                       [0.81, 0.00, 0.53, 0.54, 0.00, 0.27, 0.07, 1.00, 0.27, 0.07, 0.10, 0.36]]),

    'faraldo': np.array([[7.0, 2.0, 3.8, 2.3, 4.7, 4.1, 2.5, 5.2, 2.0, 3.7, 3.0, 3.4],
                         [7.0, 3.0, 3.8, 4.5, 2.6, 3.5, 2.5, 5.2, 4.0, 2.5, 4.5, 3.0]]),

    'pentatonic': np.array([[1.0, 0.1, 0.25, 0.1, 0.5, 0.7, 0.1, 0.8, 0.1, 0.25, 0.1, 0.5],
                            [1.0, 0.2, 0.25, 0.5, 0.1, 0.7, 0.1, 0.8, 0.3, 0.2, 0.6, 0.2]]),

    'noland': np.array([[0.0629, 0.0146, 0.061, 0.0121, 0.0623, 0.0414, 0.0248, 0.0631, 0.015, 0.0521, 0.0142, 0.0478],
                        [0.0682, 0.0138, 0.0543, 0.0519, 0.0234, 0.0544, 0.0176, 0.067, 0.0349, 0.0297, 0.0401, 0.027]])
}

def plot_chroma(chromagram, name="untitled", sr=44100, hl=2048,
                output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures"):

    from librosa.display import specshow

    if chromagram.shape[0] == 12:
        plt.figure(figsize=(5.16, 2), dpi=150)
        plt.yticks((0.5, 2.5, 4.5, 5.5, 7.5, 9.5, 11.5), ('c', 'd', 'e', 'f', 'g', 'a', 'b'))

    elif chromagram.shape[0] == 36:
        plt.figure(figsize=(5.16, 2.5), dpi=150)
        plt.yticks((0.5, 3.5, 6.5, 9.5, 12.5, 15.5, 18.5, 21.5, 24.5, 27.5, 30.5, 33.5),
                   ('c', r'c$\sharp$', 'd', r'e$\flat$', 'e', 'f', r'f$\sharp$', 'g', r'a$\flat$', 'a', r'b$\flat$', 'b'))

    specshow(chromagram, x_axis='time', sr=sr, hop_length=hl)
    plt.xlabel('time (secs.)')
    plt.ylabel('pitch classes')
    plt.tight_layout()
    # plt.colorbar()
    plt.savefig(os.path.join(output_dir, name + '.pdf'), format="pdf", dpi=1200)
    plt.show()


def plot_profiles(profile_name, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures",
                  yr=None, yt=None, loc=None):

    sns.set_style('darkgrid')
    plt.figure(figsize=(5.16, 2), dpi=150)
    plt.plot(key_templates[profile_name][0], '-o', linewidth=1, markersize=4, label="major")
    plt.plot(key_templates[profile_name][1], '--s', linewidth=1, markersize=4, label="minor")
    plt.xlabel('relative scale degrees')
    plt.ylabel('weigths')
    if yr:
        plt.ylim(yr)
    if yt:
        plt.yticks(yt)
    plt.xticks(range(12), (r'\^{1}', r'$\sharp$\^{1}/$\flat$\^{2}', r'\^{2}', r'$\sharp$\^{2}/$\flat$\^{3}', r'\^{3}',
                           r'\^{4}', r'$\sharp$\^{4}/$\flat$\^{5}', r'\^{5}', r'$\sharp$\^{5}/$\flat$\^{6}', r'\^{6}',
                           r'$\sharp$\^{6}/$\flat$\^{7}', r'\^{7}'))
    if not loc:
        plt.legend(fontsize=8)
    else:
        plt.legend(fontsize=8,loc=loc) # typically some (0.8,0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, profile_name + '_profiles.pdf'), format="pdf", dpi=1200)
    plt.show()


def plot_single_profile(data, output_dir="/Users/angel/Dropbox/Apps/Texpad/Thesis/figures",
                  yr=None, yt=None, loc=None, label=""):

    sns.set_style('darkgrid')
    plt.figure(figsize=(5.16, 2), dpi=150)
    plt.plot(data, '-gp', linewidth=1, markersize=4, label=label)
    plt.xlabel('relative scale degrees')
    plt.ylabel('weigths')
    if yr:
        plt.ylim(yr)
    if yt:
        plt.yticks(yt)
    plt.xticks(range(12), (r'\^{1}', r'$\sharp$\^{1}/$\flat$\^{2}', r'\^{2}', r'$\sharp$\^{2}/$\flat$\^{3}', r'\^{3}',
                           r'\^{4}', r'$\sharp$\^{4}/$\flat$\^{5}', r'\^{5}', r'$\sharp$\^{5}/$\flat$\^{6}', r'\^{6}',
                           r'$\sharp$\^{6}/$\flat$\^{7}', r'\^{7}'))
    if not loc:
        plt.legend(fontsize=8)
    else:
        plt.legend(fontsize=8,loc=loc) # typically some (0.8,0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, label + '_single_profile.pdf'), format="pdf", dpi=1200)
    plt.show()