package ape007.model;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;

/**
 * Repositorio de resultados del modelo.
 *
 * <p>Encapsula la escritura de los archivos CSV generados por la implementacion
 * Java del experimento Monte Carlo.</p>
 */
public final class ResultsRepository {

    private ResultsRepository() {
    }

    /**
     * Escribe los resultados detallados de los experimentos.
     */
    public static void writeResults(Path path, ExperimentRow[] rows) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(
                path, StandardCharsets.UTF_8)) {
            writer.write("experimento,n,n_c,pi_estimado,error_absoluto,pi_real,"
                    + "semilla,repeticiones,tiempo_rep1_ms,tiempo_rep2_ms,"
                    + "tiempo_rep3_ms,tiempo_mediana_ms,tiempo_promedio_ms,"
                    + "tiempo_minimo_ms,tiempo_desv_std_ms");
            writer.newLine();

            for (ExperimentRow row : rows) {
                writer.write(String.format(Locale.ROOT,
                        "%d,%d,%d,%.15f,%.15f,%.15f,%d,%d,%.6f,%.6f,%.6f,"
                        + "%.6f,%.6f,%.6f,%.6f",
                        row.experiment(),
                        row.n(),
                        row.nC(),
                        row.piEstimate(),
                        row.absoluteError(),
                        MonteCarlo.REAL_PI,
                        SplitMix64.DEFAULT_SEED,
                        MonteCarlo.REPETITIONS,
                        row.times()[0],
                        row.times()[1],
                        row.times()[2],
                        row.median(),
                        row.mean(),
                        row.minimum(),
                        row.standardDeviation()));
                writer.newLine();
            }
        }
    }

    /**
     * Escribe el archivo de verificacion de la secuencia pseudoaleatoria.
     */
    public static void writeVerification(
            Path path, SplitMix64.Verification verification) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(
                path, StandardCharsets.UTF_8)) {
            writer.write("indice,x_bits_hex,y_bits_hex,sha256_2000_uniformes");
            writer.newLine();

            double[][] firstPairs = verification.firstPairs();
            for (int index = 0; index < firstPairs.length; index++) {
                writer.write(String.format(Locale.ROOT, "%d,%s,%s,%s",
                        index + 1,
                        SplitMix64.bitsHex(firstPairs[index][0]),
                        SplitMix64.bitsHex(firstPairs[index][1]),
                        verification.sha256()));
                writer.newLine();
            }
        }
    }
}
