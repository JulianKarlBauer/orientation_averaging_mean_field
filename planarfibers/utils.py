#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import sympy as sp
import mechkit
import planarfibers

phi, theta = sp.symbols("phi theta")


class PlanarStiffnesProjector:
    def __init__(self):
        # Planar

        self.converter = mechkit.notation.Converter()

        vec = sp.Array(
            [sp.sin(theta) * sp.cos(phi), sp.sin(theta) * sp.sin(phi), sp.cos(theta)]
        ).subs({theta: sp.sympify("pi/2")})

        second_moment_tensor = sp.tensorproduct(vec, vec)
        fourth_moment_tensor = sp.tensorproduct(
            second_moment_tensor, second_moment_tensor
        )

        second_moment = planarfibers.notation.second_to_mandel6(second_moment_tensor)
        fourth_moment = planarfibers.notation.fourth_to_mandel6(fourth_moment_tensor)

        self.get_second = sp.lambdify([phi], second_moment)
        self.get_fourth = sp.lambdify([phi], fourth_moment)
        self.identity_2 = self.converter.to_mandel6(mechkit.tensors.Basic().I2)

    def get_planar_E_K(self, stiffness, angles):
        compliance = np.linalg.inv(self.converter.to_mandel6(stiffness))

        fourth_moments = np.array(list(map(self.get_fourth, angles)))
        E_modules = 1.0 / np.einsum("ij, ...ij->...", compliance, fourth_moments)

        second_moments = np.einsum("...ij,j->...i", fourth_moments, self.identity_2)
        # second_moments_alternative = np.array(list(map(self.get_second, angles)))
        # assert np.allclose(second_moments, second_moments_alternative)

        K_modules = (
            1.0
            / np.einsum("i, ij, ...j->...", self.identity_2, compliance, second_moments)
            / 3.0
        )
        return E_modules, K_modules


if __name__ == "__main__":
    ###############################
    # Get points
    import planarfibers

    df = planarfibers.discretization.get_points_on_slices()
    ###############################
    # Get stiffness

    ###############################
    # Project

    series = df.iloc[0]
    stiffness = series["stiffness_mtoa"]

    angles = np.radians(np.linspace(0, 360, 361))

    projector = PlanarStiffnesProjector()
    E, K = projector.get_planar_E_K(stiffness=stiffness, angles=angles)
