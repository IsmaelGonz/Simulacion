package ape006;

import java.util.Arrays;
import java.util.Locale;

/**
 * Prueba Kolmogorov-Smirnov de una muestra contra U(0,1).
 *
 * D+ = max_i ( i/n - x_(i) )
 * D- = max_i ( x_(i) - (i-1)/n )
 * D  = max(D+, D-)
 */
public final class KolmogorovSmirnovTest {

    public static final class Result {
        public final int n;
        public final double dPlus;
        public final double dMinus;
        public final double statisticD;
        public final int dPlusIndex;
        public final int dMinusIndex;
        public final double pValue;
        public final double alpha;
        public final boolean rejectH0;
        public final String decision;
        public final String interpretation;

        Result(int n, double dPlus, double dMinus, double statisticD,
               int dPlusIndex, int dMinusIndex, double pValue, double alpha,
               boolean rejectH0, String decision, String interpretation) {
            this.n = n;
            this.dPlus = dPlus;
            this.dMinus = dMinus;
            this.statisticD = statisticD;
            this.dPlusIndex = dPlusIndex;
            this.dMinusIndex = dMinusIndex;
            this.pValue = pValue;
            this.alpha = alpha;
            this.rejectH0 = rejectH0;
            this.decision = decision;
            this.interpretation = interpretation;
        }
    }

    private KolmogorovSmirnovTest() {
    }

    public static Result run(double[] values) {
        return run(values, 0.05);
    }

    public static Result run(double[] values, double alpha) {
        if (values == null || values.length == 0) {
            throw new IllegalArgumentException("La secuencia no puede estar vacia.");
        }
        if (alpha <= 0.0 || alpha >= 1.0) {
            throw new IllegalArgumentException("alpha debe estar entre 0 y 1.");
        }
        for (double value : values) {
            if (value < 0.0 || value >= 1.0) {
                throw new IllegalArgumentException("Valor fuera del intervalo [0,1): " + value);
            }
        }

        int n = values.length;
        double[] ordered = values.clone();
        Arrays.sort(ordered);

        double dPlus = Double.NEGATIVE_INFINITY;
        double dMinus = Double.NEGATIVE_INFINITY;
        int dPlusIndex = 0;
        int dMinusIndex = 0;

        for (int i = 1; i <= n; i++) {
            double value = ordered[i - 1];
            double empiricalAfter = (double) i / n;
            double empiricalBefore = (double) (i - 1) / n;
            double positive = empiricalAfter - value;
            double negative = value - empiricalBefore;
            if (positive > dPlus) {
                dPlus = positive;
                dPlusIndex = i;
            }
            if (negative > dMinus) {
                dMinus = negative;
                dMinusIndex = i;
            }
        }

        double statistic = Math.max(dPlus, dMinus);
        double pValue = StatisticalFunctions.kolmogorovSmirnovPValue(statistic, n);
        boolean reject = pValue < alpha;
        String interpretation = reject
                ? "La distribucion empirica difiere significativamente de la "
                        + "distribucion uniforme U(0,1) al nivel de significancia indicado."
                : "No hay evidencia estadistica suficiente para afirmar que la "
                        + "distribucion empirica difiere de la uniforme U(0,1).";

        return new Result(n, dPlus, dMinus, statistic, dPlusIndex, dMinusIndex,
                pValue, alpha, reject,
                StatisticalFunctions.decisionText(pValue, alpha, reject), interpretation);
    }

    public static String formatReport(Result result) {
        StringBuilder sb = new StringBuilder();
        sb.append("PRUEBA KOLMOGOROV-SMIRNOV (una muestra, H0: U(0,1))\n");
        sb.append("--------------------------------------------------------------\n");
        sb.append(String.format(Locale.US, "Datos analizados       : %d%n", result.n));
        sb.append(String.format(Locale.US, "Estadistico D          : %.10f%n",
                result.statisticD));
        sb.append(String.format(Locale.US, "Diferencia positiva D+ : %.10f%n", result.dPlus));
        sb.append(String.format(Locale.US, "Diferencia negativa D- : %.10f%n", result.dMinus));
        sb.append(String.format(Locale.US, "Nivel de significancia : alpha = %.2f%n",
                result.alpha));
        sb.append(String.format(Locale.US, "Valor p                : %.10f%n", result.pValue));
        sb.append("Decision               : ").append(result.decision).append('\n');
        sb.append("Interpretacion         : ").append(result.interpretation).append('\n');
        return sb.toString();
    }
}
