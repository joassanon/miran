# -*- coding: UTF-8 -*-

import numpy as np


def crosscorrelation(v, u):
    """
    Calculate the normalized cross-correlation between two vectors.
    Returns the Pearson correlation coefficient.

    """
    from scipy.stats import pearsonr

    return (pearsonr(v, u))[0]



def distance(v, u, dist='euclidean'):
    """
    Return the dist between two vectors of equal length.
    Possible distances are shown below.

    Function	    Description
    ========        ===========
    braycurtis	    the Bray-Curtis dist.
    canberra	    the Canberra dist.
    chebyshev	    the Chebyshev dist.
    cityblock	    the Manhattan dist.
    correlation	    the Correlation dist.
    cosine	        the Cosine dist.
    dice	        the Dice dissimilarity (boolean).
    euclidean	    the Euclidean dist.
    hamming	        the Hamming dist (boolean).
    jaccard	        the Jaccard dist (boolean).
    kulsinski	    the Kulsinski dist (boolean).
    mahalanobis	    the Mahalanobis dist.
    matching	    the matching dissimilarity (boolean).
    minkowski	    the Minkowski dist.
    rogerstanimoto	the Rogers-Tanimoto dissimilarity (boolean).
    russellrao	    the Russell-Rao dissimilarity (boolean).
    seuclidean	    the normalized Euclidean dist.
    sokalmichener	the Sokal-Michener dissimilarity (boolean).
    sokalsneath	    the Sokal-Sneath dissimilarity (boolean).
    sqeuclidean	    the squared Euclidean dist.
    yule	        the Yule dissimilarity (boolean).

    """
    import scipy.spatial.distance as ssd

    return eval('ssd.' + dist)(v, u)



def norm_area(v):
    """
    Normalize a vector so that the sum of its content is 1,
    outputting a vector with up to 3 decimal points.

    """
    return np.divide(v, np.sum(v))



def norm_peak(v, max_val=1.):
    """
    Normalize a vector so that the maximum value equals 'max_val'.

    """
    return np.multiply(v, (max_val / np.max(v)))



def resize_vector(v, new_size=36, interpolation='linear'):
    """
    Resize a vector to a vector of new_size.
    Interpolation patterns can be chosen from the following:

    ‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’

    """
    from scipy.interpolate import interp1d

    in_len = len(v)

    x = np.linspace(0, in_len, num=(in_len + 1), endpoint=True)
    z = np.linspace(0, in_len, num=(new_size + 1), endpoint=True)
    f = interp1d(x, np.hstack([v, v[0]]), kind=interpolation)

    return f(z)[:-1]



def standard_score(v):
    """
    Return a vector normalized to zero mean and unit standard deviation.
    This is normally referred to as standardazing.

    """
    return np.divide(np.subtract(v, np.mean(v)), np.std(v))



def unit_vector(v, order=2):
    """
    Scale input vectors individually to unit norm (vector length = 1)
    The most commonly encountered vector norm is the L2-norm
    (sometimes called the magnitude of a vector)

     The unit vector obtained by normalizing the normal vector
     (i.e., dividing a nonzero normal vector by its vector norm)
      is the unit normal vector, often known simply as the "unit normal."

      Care should be taken to not confuse the terms "vector norm" (length of vector),
     "normal vector" (perpendicular vector) and "normalized v" (unit-length vector).

    """
    vector_norm = np.linalg.norm(v, ord=order)  # L2-Norm
    if vector_norm == 0:
        return v
    return v / vector_norm



def vector_threshold(pcp, threshold):
    """
    Zero vector elements with values under a certain threshold.
    """
    for i in range(len(pcp)):
        if pcp[i] < threshold:
            pcp[i] = 0
    return pcp



def sort_vector(v, output='values', sort='ascending'):
    """
    Return a new vector with sorted indexes of the incoming pcp vector.

    """
    u = np.sort(v)
    if sort == 'descending':
        u = u[::-1]
    elif sort != 'ascending':
        raise ValueError("sort options are 'ascending' or 'descending'.")

    if output == 'values':
        return u

    elif output == 'indexes':
        idx = []
        for i in u:
            idx.append(v.tolist().index(i))
        return np.array(idx)
    else:
        raise ValueError("output options are 'values' or 'indexes'.")



def find_mode_flat(mode_array):
    """
    Calculate the closest diatonic mode to a given vector.

    """

    modes = {'ionian':     np.array([1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0., 1.]),
             'dorian':     np.array([1., 0., 1., 1., 0., 1., 0., 1., 0., 1., 1., 0.]),
             'phrygian':   np.array([1., 1., 0., 1., 0., 1., 0., 1., 1., 0., 1., 0.]),
             'lydian':     np.array([1., 0., 1., 0., 1., 0., 1., 1., 0., 1., 0., 1.]),
             'mixolydian': np.array([1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 1., 0.]),
             'aeolian':    np.array([1., 0., 1., 1., 0., 1., 0., 1., 1., 0., 1., 0.]),
             'harmonic':   np.array([1., 0., 1., 1., 0., 1., 0., 1., 1., 0., 0., 1.]),
             'locrian':    np.array([1., 1., 0., 1., 0., 1., 1., 0., 1., 0., 1., 0.]),
             'pentamaj':   np.array([1., 0., 1., 0., 1., 0., 0., 1., 0., 1., 0., 0.]),
             'pentamin':   np.array([1., 0., 0., 1., 0., 1., 0., 1., 0., 0., 1., 0.])}

    rank = []
    for mode in modes.keys():
        dis = distance(modes[mode], mode_array, dist='cityblock')
        rank.append((dis,mode))
    rank.sort(key=lambda tup: tup[0])
    return rank
