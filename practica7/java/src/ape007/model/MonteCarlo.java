package ape007.model;

/**
 * Experimento Monte Carlo para estimar pi.
 *
 * <p>Se generan N puntos uniformes en el cuadrado unitario y se cuentan los
 * que cumplen x^2 + y^2 <= 1. La estimacion es 4 * Nc / N.</p>
 */
public final class MonteCarlo {

    public static final double REAL_PI = Math.PI;
    public static final int[] SAMPLE_SIZES = {1_000, 10_000, 100_000, 1_000_000};
    public static final int REPETITIONS = 3;
    public static final int WARMUP_RUNS = 1;
    public static final int VERIFICATION_PAIRS = 1_000;

    private MonteCarlo() {
    }

    public record ExperimentResult(
            long n,
            long nC,
            double piEstimate,
            double absoluteError,
            long seed) {
    }

    /**
     * Estima pi generando n puntos con SplitMix64.
     *
     * <p>Solo esta operacion se cronometra. No incluye escritura de archivos,
     * impresion en consola ni generacion de graficos.</p>
     */
    public static ExperimentResult estimatePi(long n, long seed) {
        if (n <= 0) {
            throw new IllegalArgumentException("El numero de puntos debe ser positivo.");
        }

        long state = seed;
        long inside = 0;

        for (long i = 0; i < n; i++) {
            state += SplitMix64.GOLDEN_GAMMA;
            long z = state;
            z = (z ^ (z >>> 30)) * SplitMix64.MIX1;
            z = (z ^ (z >>> 27)) * SplitMix64.MIX2;
            z ^= z >>> 31;
            double x = (z >>> 11) * SplitMix64.TWO_POW_MINUS_53;

            state += SplitMix64.GOLDEN_GAMMA;
            z = state;
            z = (z ^ (z >>> 30)) * SplitMix64.MIX1;
            z = (z ^ (z >>> 27)) * SplitMix64.MIX2;
            z ^= z >>> 31;
            double y = (z >>> 11) * SplitMix64.TWO_POW_MINUS_53;

            if (x * x + y * y <= 1.0) {
                inside++;
            }
        }

        double piEstimate = 4.0 * inside / n;
        return new ExperimentResult(
                n,
                inside,
                piEstimate,
                Math.abs(REAL_PI - piEstimate),
                seed);
    }
}
