"""Pruebas controladas de validacion de los algoritmos.

Ejecutar con:
    py Python/tests_validacion.py
"""

from __future__ import annotations

import hashlib
import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chi_square import run_chi_square
from kolmogorov_smirnov import run_ks
from lcg import Lcg, LcgParameters
from statistics_utils import chi_square_survival, kolmogorov_smirnov_p_value


class TestLcg(unittest.TestCase):
    def test_sequence_in_unit_interval(self) -> None:
        values = Lcg().generate(10000)
        self.assertEqual(len(values), 10000)
        self.assertTrue(all(0.0 <= value < 1.0 for value in values))

    def test_known_hash_and_first_values(self) -> None:
        states = Lcg().generate_states(10000)
        digest = hashlib.sha256()
        for state in states:
            digest.update(state.to_bytes(4, "little"))
        self.assertEqual(
            digest.hexdigest(),
            "23f2d027746be27c5723900296c8d6dd058da69f6fb8ebbf65c1822819dbd696",
        )
        values = [state / LcgParameters().m for state in states[:3]]
        self.assertAlmostEqual(values[0], 0.020402685739, places=12)
        self.assertAlmostEqual(values[1], 0.016547848238, places=12)
        self.assertAlmostEqual(values[2], 0.543155794498, places=12)

    def test_same_seed_same_sequence(self) -> None:
        self.assertEqual(Lcg().generate(100), Lcg().generate(100))


class TestChiSquare(unittest.TestCase):
    def test_perfect_uniform_frequencies(self) -> None:
        values = [((i % 10) + 0.5) / 10.0 for i in range(1000)]
        result = run_chi_square(values, bins=10)
        self.assertEqual(result["frecuencias_observadas"], [100] * 10)
        self.assertAlmostEqual(result["estadistico"], 0.0, places=12)
        self.assertAlmostEqual(result["valor_p"], 1.0, places=12)
        self.assertEqual(result["grados_libertad"], 9)
        self.assertFalse(result["rechazar_h0"])

    def test_interval_boundaries(self) -> None:
        values = [
            0.0,
            0.09999999999999999,
            0.1,
            0.19999999999999998,
            0.9,
            0.9999999999999999,
        ]
        result = run_chi_square(values, bins=10)
        self.assertEqual(
            result["frecuencias_observadas"],
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 2],
        )

    def test_known_critical_values(self) -> None:
        self.assertAlmostEqual(chi_square_survival(16.919, 9), 0.05, places=5)
        self.assertAlmostEqual(chi_square_survival(14.6837, 9), 0.10, places=5)
        self.assertAlmostEqual(chi_square_survival(21.666, 9), 0.01, places=5)

    def test_invalid_value_rejected(self) -> None:
        with self.assertRaises(ValueError):
            run_chi_square([1.0], bins=10)


class TestKolmogorovSmirnov(unittest.TestCase):
    def test_controlled_equally_spaced_values(self) -> None:
        result = run_ks([0.0, 0.25, 0.5, 0.75])
        self.assertAlmostEqual(result["d_mas"], 0.25, places=12)
        self.assertAlmostEqual(result["d_menos"], 0.0, places=12)
        self.assertAlmostEqual(result["estadistico_d"], 0.25, places=12)

    def test_controlled_low_values(self) -> None:
        result = run_ks([0.1, 0.2, 0.3, 0.4])
        self.assertAlmostEqual(result["d_mas"], 0.6, places=12)
        self.assertAlmostEqual(result["d_menos"], 0.1, places=12)
        self.assertAlmostEqual(result["estadistico_d"], 0.6, places=12)

    def test_d_plus_and_d_minus_are_maxima(self) -> None:
        values = [0.02, 0.11, 0.33, 0.41, 0.57, 0.68, 0.74, 0.89, 0.93, 0.99]
        n = len(values)
        ordered = sorted(values)
        expected_plus = max((i / n) - x for i, x in enumerate(ordered, start=1))
        expected_minus = max(x - ((i - 1) / n) for i, x in enumerate(ordered, start=1))
        result = run_ks(values)
        self.assertAlmostEqual(result["d_mas"], expected_plus, places=12)
        self.assertAlmostEqual(result["d_menos"], expected_minus, places=12)
        self.assertAlmostEqual(
            result["estadistico_d"], max(expected_plus, expected_minus), places=12
        )

    def test_p_value_range_and_known_approximation(self) -> None:
        p = kolmogorov_smirnov_p_value(0.0136, 10000)
        self.assertAlmostEqual(p, 0.049, places=2)
        self.assertTrue(0.0 <= p <= 1.0)
        self.assertTrue(math.isclose(kolmogorov_smirnov_p_value(0.0, 100), 1.0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
