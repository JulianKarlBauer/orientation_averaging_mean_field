#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import scipy
import mechkit

ORDER = 180


class IntegrationSchemeCircle:
    def __init__(self, order=ORDER):
        self.length = 2.0 * np.pi * 1.0
        self.angles = self.length * np.arange(order) / order
        self.weights = np.full(order, 1.0 / order)
        self.weights_incl_length = self.length * self.weights


class AveragerPlanar:
    def __init__(self, odf_planar, order=ORDER):

        scheme = IntegrationSchemeCircle(order=order)
        self.length = scheme.length
        self.angles = scheme.angles
        self.weights_incl_length = odf_planar(self.angles) * scheme.weights_incl_length

        self.converter = mechkit.notation.Converter()

    def _average(self, inp_vector):
        return np.tensordot(inp_vector, self.weights_incl_length, 1)

    def _get_rotation(self, angles):
        return scipy.spatial.transform.Rotation.from_euler(
            "z", angles, degrees=False
        ).as_matrix()

    def _rotate(self, quantity, rotations):
        order = len(quantity.shape)
        if order == 4:
            rotated = np.einsum(
                "...it, ...ju, ...kv, ...lw, tuvw->ijkl...",
                rotations,
                rotations,
                rotations,
                rotations,
                quantity,
            )
        else:
            raise Exception("Tensor order not supported")
        return rotated

    def average(self, inp):
        rotations = self._get_rotation(angles=self.angles)
        tensor = converter.to_tensor(inp)
        rotated = self._rotate(quantity=tensor, rotations=rotations)
        averaged = self._average(rotated)
        mandel = converter.to_mandel6(averaged)
        return mandel
