package ape006;

import java.util.Arrays;

/**
 * Pruebas controladas de los algoritmos Java.
 *
 * Ejecutar con:
 *   java -cp Java/out ape006.ValidationTests
 */
public final class ValidationTests {
    private static int passed = 0;

    private ValidationTests() {
    }

    public static void main(String[] args) {
        testLcg();
        testChiSquare();
        testKolmogorovSmirnov();
        System.out.println("OK: " + passed + " pruebas controladas superadas.");
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError("FALLA: " + message);
        }
        passed++;
    }

    private static void checkClose(double actual, double expected, double tolerance,
                                   String message) {
        check(Math.abs(actual - expected) <= tolerance,
                message + " (actual=" + actual + ", esperado=" + expected + ")");
    }

    private static void testLcg() {
        Lcg generator = new Lcg();
        double[] values = generator.generate(10_000);
        check(values.length == 10_000, "LCG genera 10000 valores");
        boolean inRange = true;
        for (double value : values) {
            inRange &= value >= 0.0 && value < 1.0;
        }
        check(inRange, "Todos los valores estan en [0,1)");

        Lcg second = new Lcg();
        long[] states = second.generateStates(10_000);
        check(ExportUtils.sha256States(states)
                        .equals("23f2d027746be27c5723900296c8d6dd058da69f6fb8ebbf65c1822819dbd696"),
                "SHA-256 esperado para 10000 estados");
        checkClose(values[0], 0.020402685739, 1.0e-12, "Primer valor");
        checkClose(values[1], 0.016547848238, 1.0e-12, "Segundo valor");
        checkClose(values[2], 0.543155794498, 1.0e-12, "Tercer valor");
    }

    private static void testChiSquare() {
        double[] values = new double[1000];
        for (int i = 0; i < values.length; i++) {
            values[i] = ((i % 10) + 0.5) / 10.0;
        }
        ChiSquareTest.Result result = ChiSquareTest.run(values, 10, 0.05);
        for (int i = 0; i < 10; i++) {
            check(result.observed[i] == 100, "Frecuencia perfecta en intervalo " + i);
        }
        checkClose(result.statistic, 0.0, 1.0e-12, "Chi2 cero para frecuencias perfectas");
        checkClose(result.pValue, 1.0, 1.0e-12, "p = 1 para chi2 = 0");
        check(result.degreesOfFreedom == 9, "Grados de libertad = 9");
        check(!result.rejectH0, "No se rechaza H0 en caso perfecto");

        double[] boundaries = {
            0.0,
            0.09999999999999999,
            0.1,
            0.19999999999999998,
            0.9,
            0.9999999999999999
        };
        ChiSquareTest.Result boundaryResult = ChiSquareTest.run(boundaries, 10, 0.05);
        int[] expected = {2, 2, 0, 0, 0, 0, 0, 0, 0, 2};
        check(Arrays.equals(boundaryResult.observed, expected),
                "Limites de intervalos Chi-cuadrado");

        checkClose(StatisticalFunctions.chiSquareSurvival(16.919, 9), 0.05, 1.0e-5,
                "Valor critico chi2 0.05");
        checkClose(StatisticalFunctions.chiSquareSurvival(14.6837, 9), 0.10, 1.0e-5,
                "Valor critico chi2 0.10");
        checkClose(StatisticalFunctions.chiSquareSurvival(21.666, 9), 0.01, 1.0e-5,
                "Valor critico chi2 0.01");

        boolean rejected = false;
        try {
            ChiSquareTest.run(new double[]{1.0}, 10, 0.05);
        } catch (IllegalArgumentException exception) {
            rejected = true;
        }
        check(rejected, "Valor 1.0 fuera de [0,1) es rechazado");
    }

    private static void testKolmogorovSmirnov() {
        KolmogorovSmirnovTest.Result first =
                KolmogorovSmirnovTest.run(new double[]{0.0, 0.25, 0.5, 0.75});
        checkClose(first.dPlus, 0.25, 1.0e-12, "D+ controlado");
        checkClose(first.dMinus, 0.0, 1.0e-12, "D- controlado");
        checkClose(first.statisticD, 0.25, 1.0e-12, "D controlado");

        KolmogorovSmirnovTest.Result second =
                KolmogorovSmirnovTest.run(new double[]{0.1, 0.2, 0.3, 0.4});
        checkClose(second.dPlus, 0.6, 1.0e-12, "D+ valores bajos");
        checkClose(second.dMinus, 0.1, 1.0e-12, "D- valores bajos");
        checkClose(second.statisticD, 0.6, 1.0e-12, "D valores bajos");

        double[] values = {0.02, 0.11, 0.33, 0.41, 0.57, 0.68, 0.74, 0.89, 0.93, 0.99};
        double[] ordered = values.clone();
        Arrays.sort(ordered);
        int n = ordered.length;
        double expectedPlus = Double.NEGATIVE_INFINITY;
        double expectedMinus = Double.NEGATIVE_INFINITY;
        for (int i = 1; i <= n; i++) {
            expectedPlus = Math.max(expectedPlus, (double) i / n - ordered[i - 1]);
            expectedMinus = Math.max(expectedMinus, ordered[i - 1] - (double) (i - 1) / n);
        }
        KolmogorovSmirnovTest.Result third = KolmogorovSmirnovTest.run(values);
        checkClose(third.dPlus, expectedPlus, 1.0e-12, "D+ es el maximo correcto");
        checkClose(third.dMinus, expectedMinus, 1.0e-12, "D- es el maximo correcto");
        checkClose(third.statisticD, Math.max(expectedPlus, expectedMinus), 1.0e-12,
                "D = max(D+, D-)");

        double p = StatisticalFunctions.kolmogorovSmirnovPValue(0.0136, 10000);
        checkClose(p, 0.049, 0.01, "Aproximacion conocida del valor p KS");
        check(p >= 0.0 && p <= 1.0, "Valor p KS en [0,1]");
        checkClose(StatisticalFunctions.kolmogorovSmirnovPValue(0.0, 100), 1.0, 1.0e-15,
                "D = 0 produce p = 1");
    }
}
