#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sympy as sp
import pandas as pd

two = sp.S(2)
zero = sp.S(0)
base = sp.sympify("-4 / 35")
pi = sp.pi


def radius_circle_d8_d1_plane(la1):
    return (la1 - la1 ** sp.S(2)) / sp.S(2)


def r_max(la1):
    return radius_circle_d8_d1_plane(la1)


def get_d_1(radius_factor, beta, la1):
    radius = radius_circle_d8_d1_plane(la1)
    return radius_factor * radius * sp.sin(beta) + radius + base


def get_d_8(radius_factor, beta, la1):
    radius = radius_circle_d8_d1_plane(la1)
    return radius_factor * radius * sp.cos(beta)


def d1_hat_by_la1_d1(la1, d1):
    return d1 - base - radius_circle_d8_d1_plane(la1)


def r_by_la1_d1_d8(la1, d1, d8):
    d1_hat = d1_hat_by_la1_d1(la1=la1, d1=d1)
    return sp.sqrt(d1_hat ** sp.S(2) + d8 ** sp.S(2))


def beta_by_la1_d1_d8(la1, d1, d8):
    return sp.atan2(d1_hat_by_la1_d1(la1=la1, d1=d1), d8)


def points_view00(la1s, radius_almost):
    angle_upper = pi / two
    angle_mid = zero
    angle_lower = -pi / two

    one_is_on_board = sp.S(1) in la1s

    nbr_la1s = len(la1s)
    if one_is_on_board:
        nbr_la1s -= 1
    tmp = {
        **{
            f"v00-upper-{index}": {
                "la1": la1s[index],
                "radius_factor": radius_almost,
                "beta": angle_upper,
            }
            for index in range(nbr_la1s)
        },
        **{
            f"v00-mid-{index}": {
                "la1": la1s[index],
                "radius_factor": zero,
                "beta": angle_mid,
            }
            for index in range(nbr_la1s)
        },
        **{
            f"v00-lower-{index}": {
                "la1": la1s[index],
                "radius_factor": radius_almost,
                "beta": angle_lower,
            }
            for index in range(nbr_la1s)
        },
    }
    if one_is_on_board:
        tmp[f"v00-mid-{nbr_la1s}"] = {
            "la1": la1s[-1],
            "radius_factor": zero,
            "beta": zero,
        }
    return tmp


def points_view_shaped_half_circle(la1, angles, angles_names, radii, key_extension=""):
    points = {
        "vshc-central": {
            "la1": la1,
            "radius_factor": zero,
            "beta": zero,
        },
        **{
            f"vshc-{angles_names[index_angle]}-{index_radius}": {
                "la1": la1,
                "radius_factor": radius,
                "beta": angles[index_angle],
            }
            for index_angle in range(len(angles))
            for index_radius, radius in enumerate(radii[1:])
        },
    }
    return {key + key_extension: val for key, val in points.items()}


def get_points_on_slices(
    radii=["0", "1/2", "9/10"], la1s=["1/2", "4/6", "5/6", "1"], numeric=False
):

    la1s = list(map(sp.sympify, la1s))
    radii = list(map(sp.sympify, radii))

    angles_raw = ["-90", "-45", "0", "45", "90"]
    angles = list(map(sp.rad, map(sp.sympify, angles_raw)))
    angles_names = list(map(lambda x: x.replace("-", "m"), angles_raw))

    radius_almost = radii[-1]

    points = points_view00(la1s=la1s, radius_almost=radius_almost)
    for index, la1 in enumerate(la1s[:-1]):
        points = {
            **points,
            **points_view_shaped_half_circle(
                la1=la1,
                angles=angles,
                angles_names=angles_names,
                radii=radii,
                key_extension=f"-la1-{index}",
            ),
        }

    df = pd.DataFrame(points).T

    df["r"] = df.apply(
        lambda row: sp.simplify(row["radius_factor"] * r_max(la1=row["la1"])),
        axis=1,
    )

    df["d_1"] = df.apply(
        lambda row: sp.simplify(
            get_d_1(
                radius_factor=row["radius_factor"], beta=row["beta"], la1=row["la1"]
            )
        ),
        axis=1,
    )

    df["d_8"] = df.apply(
        lambda row: sp.simplify(
            get_d_8(
                radius_factor=row["radius_factor"], beta=row["beta"], la1=row["la1"]
            )
        ),
        axis=1,
    )

    # if False:
    #     df_sorted = df.sort_values(
    #         by=["la1", "beta", "r"], ascending=(True, True, True)
    #     )

    if numeric:
        return df.applymap(lambda x: float(sp.N(x)))
    return df
