import numpy as np
import scipy.ndimage.filters as filters

import matplotlib.pyplot as plt

""" IDEAS
-Could have key points set and interpolate between OR smooth between
"""

#-----------SETTINGS ------------------

width = 400
height = 400
# blank = np.zeros((height, width))

# Variables to show
altitude = 1
temperature = 0

# ---------------- FUNCTIONS --------------------

def temperatureFromLatitude(latitude, degree):
    """ Estimate typical average temperature for a given latitude given earth values
    When picking example values I tried to ignore things like the warm atlantic current
    or the tibeten plateau

    :param latitude: float, latitude north or south
    :return: temperature: float, in degrees celcius
    """

    latitude = np.abs(latitude)

    lat = [0, 15, 24, 27, 35, 40, 50, 65, 90]
    temp = [32, 31, 28, 22, 16, 10, 0, -10, -20]

    coeffs = np.polyfit(lat, temp, degree)

    out=0
    for i, a in enumerate(coeffs):
        out += a * latitude ** (degree-i)

    out[out>32]=32
    out[out<-20]=-20
    return out

def plotSingleVariable(x, colormap):
    img = plt.imshow(x, colormap)
    plt.plot([-.5, width - 0.5], [height / 2 - 0.5, height / 2 - 0.5],
             color='k', linestyle='--', linewidth=1)
    bar = plt.colorbar(img)
    bar.set_label('Temperature Celcius')
    plt.axis('off')
    plt.show()

def addSmoothedPoint(input, x, y, peak, sd):

    blank = np.zeros((height, width))
    blank[x, y] = peak
    addition = filters.gaussian_filter(blank, sd, 0, mode='wrap') * sd * 50

    return input + addition

# ----------------- CORE ----------------------
master = {}
latitude = np.array([np.arange(90., -90., -180./height) for _ in xrange(width)]).transpose()
longitude = np.array([np.arange(-180., 180., 360./width) for _ in xrange(height)])


# ---------------- TEMP -----------------
if temperature:
    temp = temperatureFromLatitude(latitude, 3)
    plotSingleVariable(temp, 'plasma')


# ------------- ALTITUDE ----------------
if altitude:
    alt = -np.ones((height, width))

    # plotSingleVariable(alt, 'binary')

    # alt = addSmoothedPoint(alt, 35, 264, peak=100, sd=3)
    # plotSingleVariable(alt, 'binary')

    alt = addSmoothedPoint(alt, 342, 135, peak=100, sd=20)
    plotSingleVariable(alt, 'binary')

#-------------- PRINT -----------------




