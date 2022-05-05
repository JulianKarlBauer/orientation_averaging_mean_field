# # Integrate random planar FODF with numerical averager

import planarfibers
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 100)
pd.set_option("display.width", 1000)
np.set_printoptions(linewidth=400)


# Select random FODF: choose exact closre FODF, see equation (77) in "Fiber orientation distributions based on planar fiber orientation tensors of fourth order. Math. Mech. Solids (to appear 2022)"".
la1 = 5 / 6
odf_func = lambda phi: ((1.0 - la1) * la1) / (
    2.0 * np.pi * (la1**2 + (1.0 - 2.0 * la1) * np.cos(phi) ** 2)
)

# Select quantity which is to be averaged
quantity = planarfibers.approximation.calc_MT_UD()
print(quantity)

# Average
averager = planarfibers.averager.AveragerPlanar(odf_planar=odf_func)
average = averager.average(quantity)
print(average)
