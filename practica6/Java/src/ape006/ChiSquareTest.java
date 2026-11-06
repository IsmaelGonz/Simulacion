package ape006;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * Prueba Chi-cuadrado de bondad de ajuste a U(0,1).
 */
public final class ChiSquareTest {

    public static final class Result {
        public final int n;
        public final int bins;
        public final double amplitude;
        public final List<String> labels;
        public final int[] observed;
        public final double[] expected;
        public final double statistic;
        public final int degreesOfFreedom;
        public final double alpha;
        public final double pValue;
        public final boolean rejectH0;
        public final String decision;
        public final String interpretation;

        Result(int n, int bins, double amplitude, List<String> labels,
               int[] observed, double[] expected, double statistic,
               int degreesOfFreedom, double alpha, double pValue,
               boolean rejectH0, String decision, String interpretation) {
            this.n = n;
            this.bins = bins;
            this.amplitude = amplitude;
            this.labels = labels;
            this.observed = observed;
            this.expected = expected;
            this.statistic = statistic;
            this.degreesOfFreedom = degreesOfFreedom;
            this.alpha = alpha;
            this.pValue = pValue;
            this.rejectH0 = rejectH0;
            this.decision = decision;
            this.interpretation = interpretation;
        }
    }

    private ChiSquareTest() {
    }

    private static String intervalLabel(int index, int bins) {
        double lower = (double) index / bins;
        double upper = (double) (index + 1) / bins;
        if (index == bins - 1) {
            return String.format(Locale.US, "[%.1f, %.1f]", lower, upper);
        }
        return String.format(Locale.US, "[%.1f, %.1f)", lower, upper);
    }

    public static Result run(double[] values, int bins, double alpha) {
        if (bins <= 1) {
            throw new IllegalArgumentException("El numero de intervalos debe ser mayor que 1.");
        }
        if (values == null || values.length == 0) {
            throw new IllegalArgumentException("La secuencia no puede estar vacia.");
        }
        if (alpha <= 0.0 || alpha >= 1.0) {
            throw new IllegalArgumentException("alpha debe estar entre 0 y 1.");
        }

        int n = values.length;
        int[] observed = new int[bins];
        for (double value : values) {
            if (value < 0.0 || value >= 1.0) {
                throw new IllegalArgumentException("Valor fuera del intervalo [0,1): " + value);
            }
            int index = (int) (value * bins);
            if (index >= bins) {
                index = bins - 1;
            }
            observed[index]++;
        }

        double[] expected = new double[bins];
        double statistic = 0.0;
        for (int i = 0; i < bins; i++) {
            expected[i] = (double) n / bins;
            double difference = observed[i] - expected[i];
            statistic += difference * difference / expected[i];
        }

        int degreesOfFreedom = bins - 1;
        double pValue = StatisticalFunctions.chiSquareSurvival(statistic, degreesOfFreedom);
        boolean reject = pValue < alpha;
        String interpretation = reject
                ? "Las frecuencias observadas son incompatibles con una distribucion "
                        + "uniforme U(0,1) al nivel de significancia indicado."
                : "No hay evidencia estadistica suficiente para afirmar que las "
                        + "frecuencias observadas se apartan de una distribucion uniforme U(0,1).";

        List<String> labels = new ArrayList<>(bins);
        for (int i = 0; i < bins; i++) {
            labels.add(intervalLabel(i, bins));
        }

        return new Result(n, bins, 1.0 / bins, labels, observed, expected, statistic,
                degreesOfFreedom, alpha, pValue, reject,
                StatisticalFunctions.decisionText(pValue, alpha, reject), interpretation);
    }

    public static Result run(double[] values) {
        return run(values, 10, 0.05);
    }

    public static String formatReport(Result result) {
        StringBuilder sb = new StringBuilder();
        sb.append("PRUEBA CHI-CUADRADO (bondad de ajuste a U(0,1))\n");
        sb.append("--------------------------------------------------------------\n");
        sb.append(String.format(Locale.US, "Datos analizados      : %d%n", result.n));
        sb.append(String.format(Locale.US, "Intervalos            : %d (amplitud %.2f)%n",
                result.bins, result.amplitude));
        sb.append(String.format(Locale.US, "Grados de libertad    : %d%n",
                result.degreesOfFreedom));
        sb.append(String.format(Locale.US, "Nivel de significancia: alpha = %.2f%n", result.alpha));
        sb.append(String.format(Locale.US, "Estadistico chi2      : %.10f%n", result.statistic));
        sb.append(String.format(Locale.US, "Valor p (cola superior): %.10f%n", result.pValue));
        sb.append("Decision              : ").append(result.decision).append('\n');
        sb.append("Interpretacion        : ").append(result.interpretation).append('\n');
        sb.append('\n');
        sb.append(String.format(Locale.US, "%-16s%12s%12s%14s%n",
                "Intervalo", "Observado", "Esperado", "Diferencia"));
        sb.append("------------------------------------------------------\n");
        int totalObserved = 0;
        double totalExpected = 0.0;
        for (int i = 0; i < result.bins; i++) {
            totalObserved += result.observed[i];
            totalExpected += result.expected[i];
            sb.append(String.format(Locale.US, "%-16s%12d%12.1f%14.1f%n",
                    result.labels.get(i), result.observed[i], result.expected[i],
                    result.observed[i] - result.expected[i]));
        }
        sb.append("------------------------------------------------------\n");
        sb.append(String.format(Locale.US, "%-16s%12d%12.1f%n",
                "Total", totalObserved, totalExpected));
        return sb.toString();
    }
}
