#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def inp_material_parameters():
    return {
        "E_f": 73.0,
        "E_m": 3.4,
        # "N4": np.array(N4),
        "c_f": 0.256,
        "nu_f": 0.22,
        "nu_m": 0.385,
    }


from . import discretization
from . import approximation
from . import notation
from . import utils
from . import averager
