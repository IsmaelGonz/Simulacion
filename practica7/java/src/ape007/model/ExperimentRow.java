package ape007.model;

/** Fila de resultados de un experimento Monte Carlo. */
public record ExperimentRow(
        int experiment,
        long n,
        long nC,
        double piEstimate,
        double absoluteError,
        double[] times,
        double median,
        double mean,
        double minimum,
        double standardDeviation) {
}
