package ape006;

/**
 * Funciones estadisticas equivalentes a las de Python.
 *
 * Chi-cuadrado: Q(a, x) mediante serie y fraccion continua de la gamma
 * incompleta regularizada (misma implementacion en ambos lenguajes).
 *
 * Kolmogorov-Smirnov: distribucion asintotica de Kolmogorov con correccion
 * de Stephens (1970). Se documenta como aproximacion.
 */
public final class StatisticalFunctions {
    private static final double EPS = 3.0e-14;
    private static final double FPMIN = 1.0e-300;
    private static final int MAX_ITER = 1000;

    private static final double[] LANCZOS = {
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    };

    private StatisticalFunctions() {
    }

    public static double logGamma(double z) {
        if (z < 0.5) {
            return Math.log(Math.PI / Math.sin(Math.PI * z)) - logGamma(1.0 - z);
        }
        z -= 1.0;
        double x = 0.99999999999980993;
        for (int i = 0; i < LANCZOS.length; i++) {
            x += LANCZOS[i] / (z + i + 1.0);
        }
        double t = z + 7.5;
        return 0.5 * Math.log(2.0 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }

    private static double gammaSeries(double a, double x) {
        if (x <= 0.0) {
            return 0.0;
        }
        double ap = a;
        double total = 1.0 / a;
        double delta = total;
        for (int i = 0; i < MAX_ITER; i++) {
            ap += 1.0;
            delta *= x / ap;
            total += delta;
            if (Math.abs(delta) < Math.abs(total) * EPS) {
                break;
            }
        }
        return total * Math.exp(-x + a * Math.log(x) - logGamma(a));
    }

    private static double gammaContinuedFraction(double a, double x) {
        double b = x + 1.0 - a;
        double c = 1.0 / FPMIN;
        double d = Math.abs(b) > FPMIN ? 1.0 / b : 1.0 / FPMIN;
        double h = d;
        for (int i = 1; i <= MAX_ITER; i++) {
            double an = -i * (i - a);
            b += 2.0;
            d = an * d + b;
            if (Math.abs(d) < FPMIN) {
                d = FPMIN;
            }
            c = b + an / c;
            if (Math.abs(c) < FPMIN) {
                c = FPMIN;
            }
            d = 1.0 / d;
            double delta = d * c;
            h *= delta;
            if (Math.abs(delta - 1.0) < EPS) {
                break;
            }
        }
        return Math.exp(-x + a * Math.log(x) - logGamma(a)) * h;
    }

    public static double regularizedGammaQ(double a, double x) {
        if (a <= 0.0) {
            throw new IllegalArgumentException("El parametro a debe ser positivo.");
        }
        if (x < 0.0) {
            throw new IllegalArgumentException("El parametro x debe ser no negativo.");
        }
        if (x == 0.0) {
            return 1.0;
        }
        double result;
        if (x < a + 1.0) {
            result = 1.0 - gammaSeries(a, x);
        } else {
            result = gammaContinuedFraction(a, x);
        }
        return Math.max(0.0, Math.min(1.0, result));
    }

    public static double chiSquareSurvival(double statistic, int degreesOfFreedom) {
        if (degreesOfFreedom <= 0) {
            throw new IllegalArgumentException("Los grados de libertad deben ser positivos.");
        }
        if (statistic <= 0.0) {
            return 1.0;
        }
        return regularizedGammaQ(degreesOfFreedom / 2.0, statistic / 2.0);
    }

    public static double kolmogorovSmirnovPValue(double d, int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("El tamano de muestra debe ser positivo.");
        }
        if (d <= 0.0) {
            return 1.0;
        }
        if (d >= 1.0) {
            return 0.0;
        }

        double sqrtN = Math.sqrt(n);
        double lambda = (sqrtN + 0.12 + 0.11 / sqrtN) * d;
        if (lambda < 1.0e-12) {
            return 1.0;
        }

        if (lambda < 0.82) {
            double factor = Math.sqrt(2.0 * Math.PI) / lambda;
            double total = 0.0;
            for (int k = 1; k < 200; k++) {
                double odd = 2.0 * k - 1.0;
                double exponent = -(odd * odd) * Math.PI * Math.PI
                        / (8.0 * lambda * lambda);
                double term = exponent > -745.0 ? factor * Math.exp(exponent) : 0.0;
                total += term;
                if (term < 1.0e-16) {
                    break;
                }
            }
            return Math.max(0.0, Math.min(1.0, 1.0 - total));
        }

        double total = 0.0;
        for (int k = 1; k < 200; k++) {
            double sign = (k % 2 == 1) ? 1.0 : -1.0;
            double term = 2.0 * sign * Math.exp(-2.0 * k * k * lambda * lambda);
            total += term;
            if (Math.abs(term) < 1.0e-16) {
                break;
            }
        }
        return Math.max(0.0, Math.min(1.0, total));
    }

    public static String decisionText(double pValue, double alpha, boolean reject) {
        return reject
                ? String.format(java.util.Locale.US,
                        "Se rechaza H0 (p = %.6g < alpha = %s).", pValue, formatAlpha(alpha))
                : String.format(java.util.Locale.US,
                        "No se rechaza H0 (p = %.6g >= alpha = %s).", pValue, formatAlpha(alpha));
    }

    private static String formatAlpha(double alpha) {
        if (alpha == Math.rint(alpha)) {
            return String.valueOf((long) alpha);
        }
        return String.valueOf(alpha);
    }
}
