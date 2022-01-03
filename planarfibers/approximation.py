#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import mechkit
import mechmean
import planarfibers


###########################################################
# Convenient wrapper of homogenization schemes


def calc_MTOA(N4, inp=None):

    if inp is None:
        inp = planarfibers.inp_material_parameters()

    inclusion = mechkit.material.Isotropic(
        E=inp["E_f"],
        nu=inp["nu_f"],
    )

    matrix = mechkit.material.Isotropic(
        E=inp["E_m"],
        nu=inp["nu_m"],
    )

    averager = mechmean.orientation_averager.AdvaniTucker(N4=np.array(N4))

    inp_MT = {
        "phases": {
            "inclusion": {
                "volume_fraction": inp["c_f"],
                "material": inclusion,
                "hill_polarization": mechmean.hill_polarization.Castaneda().needle(
                    matrix=matrix
                ),
            },
            "matrix": {"material": matrix},
        },
        "averaging_func": averager.average,
    }

    MTOA = mechmean.approximation.MoriTanakaOrientationAveraged(**inp_MT)

    return MTOA.calc_C_eff()


def calc_HS2Step(N4, k1, k2, inp=None):

    if inp is None:
        inp = planarfibers.inp_material_parameters()

    inclusion = mechkit.material.Isotropic(
        E=inp["E_f"],
        nu=inp["nu_f"],
    )

    matrix = mechkit.material.Isotropic(
        E=inp["E_m"],
        nu=inp["nu_m"],
    )

    averager = mechmean.orientation_averager.AdvaniTucker(N4=np.array(N4))

    inp_HS = {
        "phases": {
            "inclusion": {"material": inclusion, "volume_fraction": inp["c_f"]},
            "matrix": {"material": matrix},
        },
        "k1": k1,
        "k2": k2,
        "averaging_func": averager.average,
    }

    Ceff = mechmean.approximation.HSW2StepInterpolatedReferenceMaterial(
        **inp_HS,
    ).calc_C_eff()

    return Ceff


def calc_MT_UD(inp=None):

    if inp is None:
        inp = planarfibers.inp_material_parameters()

    inclusion = mechkit.material.Isotropic(
        E=inp["E_f"],
        nu=inp["nu_f"],
    )

    matrix = mechkit.material.Isotropic(
        E=inp["E_m"],
        nu=inp["nu_m"],
    )

    Pud_func = mechmean.hill_polarization.Castaneda().needle

    P_ud = Pud_func(matrix=matrix)

    mtoa = mechmean.approximation.MoriTanaka(
        phases={
            "inclusion": {
                "material": inclusion,
                "hill_polarization": P_ud,
                "volume_fraction": inp["c_f"],
            },
            "matrix": {"material": matrix},
        },
    )

    C_ud = mtoa.calc_C_eff()

    return C_ud


def calc_MT_linear_in_orientations(N4, inp=None):

    C_ud = calc_MT_UD(inp=inp)

    averager = mechmean.orientation_averager.AdvaniTucker(N4=np.array(N4))

    C_eff = averager.average(C_ud)

    return C_eff


def calc_MT_linear_in_orientations_compliance(N4, inp=None):

    C_ud = calc_MT_UD(inp=inp)

    S_ud = np.linalg.inv(C_ud)

    averager = mechmean.orientation_averager.AdvaniTucker(N4=np.array(N4))

    S_eff = averager.average(S_ud)

    C_eff = np.linalg.inv(S_eff)

    return C_eff
