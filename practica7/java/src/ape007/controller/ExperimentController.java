package ape007.controller;

import ape007.model.ExperimentRow;
import ape007.model.MonteCarlo;
import ape007.model.ResultsRepository;
import ape007.model.SplitMix64;
import ape007.view.ConsoleView;

import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Locale;

/**
 * Controlador del experimento Monte Carlo en Java.
 *
 * <p>Orquesta la ejecucion de los cuatro tamanos de muestra, el cronometraje,
 * el calentamiento y la escritura de resultados.</p>
 */
public final class ExperimentController {

    private static final int GLOBAL_WARMUP_RUNS = 2;
    private final Path resultsDirectory;
    private final long seed;

    public ExperimentController(Path resultsDirectory, long seed) {
        this.resultsDirectory = resultsDirectory;
        this.seed = seed;
    }

    public void run() throws IOException {
        int largestSample = MonteCarlo.SAMPLE_SIZES[
                MonteCarlo.SAMPLE_SIZES.length - 1];

        for (int warm = 0; warm < GLOBAL_WARMUP_RUNS; warm++) {
            MonteCarlo.estimatePi(largestSample, seed);
        }

        ExperimentRow[] rows = runExperiments();

        ResultsRepository.writeResults(
                resultsDirectory.resolve("resultados_java.csv"), rows);

        SplitMix64.Verification verification = SplitMix64.verifySequence(
                MonteCarlo.VERIFICATION_PAIRS, seed);
        ResultsRepository.writeVerification(
                resultsDirectory.resolve("verificacion_java.csv"), verification);

        ConsoleView.printResults(
                rows,
                verification,
                resultsDirectory,
                System.getProperty("java.version"),
                System.getProperty("os.name"),
                System.getProperty("os.arch"),
                seed,
                MonteCarlo.REPETITIONS,
                MonteCarlo.WARMUP_RUNS,
                GLOBAL_WARMUP_RUNS,
                largestSample);
    }

    private ExperimentRow[] runExperiments() {
        ExperimentRow[] rows = new ExperimentRow[MonteCarlo.SAMPLE_SIZES.length];

        for (int index = 0; index < MonteCarlo.SAMPLE_SIZES.length; index++) {
            int n = MonteCarlo.SAMPLE_SIZES[index];
            MonteCarlo.ExperimentResult warmup = null;
            for (int warm = 0; warm < MonteCarlo.WARMUP_RUNS; warm++) {
                warmup = MonteCarlo.estimatePi(n, seed);
            }
            if (warmup == null) {
                throw new IllegalStateException("No se ejecuto el calentamiento.");
            }

            double[] times = new double[MonteCarlo.REPETITIONS];
            MonteCarlo.ExperimentResult result = warmup;

            for (int repetition = 0; repetition < MonteCarlo.REPETITIONS; repetition++) {
                long start = System.nanoTime();
                result = MonteCarlo.estimatePi(n, seed);
                long end = System.nanoTime();
                times[repetition] = (end - start) / 1_000_000.0;

                if (result.nC() != warmup.nC()) {
                    throw new IllegalStateException(
                            "El generador no es determinista: Nc cambio entre repeticiones.");
                }
            }

            double[] sorted = times.clone();
            Arrays.sort(sorted);
            double median = sorted[sorted.length / 2];
            double mean = Arrays.stream(times).average().orElse(0.0);
            double variance = 0.0;
            for (double time : times) {
                variance += (time - mean) * (time - mean);
            }
            double standardDeviation = times.length > 1
                    ? Math.sqrt(variance / (times.length - 1))
                    : 0.0;

            rows[index] = new ExperimentRow(
                    index + 1,
                    result.n(),
                    result.nC(),
                    result.piEstimate(),
                    result.absoluteError(),
                    times,
                    median,
                    mean,
                    sorted[0],
                    standardDeviation);
        }

        return rows;
    }
}
