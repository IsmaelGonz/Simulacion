package ape007.view;

import ape007.model.ExperimentRow;
import ape007.model.MonteCarlo;
import ape007.model.SplitMix64.Verification;

import java.nio.file.Path;
import java.util.Locale;

/**
 * Vista de consola de la implementacion Java.
 *
 * <p>Se encarga unicamente de presentar los resultados al usuario.</p>
 */
public final class ConsoleView {

    private ConsoleView() {
    }

    public static void printResults(
            ExperimentRow[] rows,
            Verification verification,
            Path resultsDirectory,
            String javaVersion,
            String osName,
            String osArch,
            long seed,
            int repetitions,
            int warmupRuns,
            int globalWarmupRuns,
            int largestSample) {
        System.out.println("=".repeat(92));
        System.out.println("APE 007 - ESTIMACION DE pi MEDIANTE MONTE CARLO - JAVA");
        System.out.println("=".repeat(92));
        System.out.printf(Locale.ROOT,
                "Java: %s | Sistema: %s %s%n",
                javaVersion, osName, osArch);
        System.out.printf(Locale.ROOT,
                "Generador: SplitMix64 | Semilla: %d%n", seed);
        System.out.printf(Locale.ROOT,
                "Repeticiones cronometradas: %d | Calentamiento por tamano: %d%n",
                repetitions, warmupRuns);
        System.out.printf(Locale.ROOT,
                "Calentamiento global adicional: %d x %,d puntos%n",
                globalWarmupRuns, largestSample);
        System.out.printf(Locale.ROOT,
                "%-5s%12s%12s%16s%18s%16s%n",
                "Exp.", "N", "Nc", "pi estimado", "Error absoluto", "Mediana (ms)");
        System.out.println("-".repeat(92));

        for (ExperimentRow row : rows) {
            System.out.printf(Locale.ROOT,
                    "%-5d%,12d%,12d%16.10f%18.10f%16.6f%n",
                    row.experiment(),
                    row.n(),
                    row.nC(),
                    row.piEstimate(),
                    row.absoluteError(),
                    row.median());
        }

        System.out.println("-".repeat(92));
        System.out.printf(Locale.ROOT,
                "Valor real de pi (Math.PI): %.15f%n", MonteCarlo.REAL_PI);
        System.out.printf(Locale.ROOT,
                "Verificacion de secuencia: %d pares, SHA-256 = %s%n",
                verification.pairs(), verification.sha256());
        System.out.println("Resultados Java: "
                + resultsDirectory.resolve("resultados_java.csv"));
        System.out.println("Verificacion Java: "
                + resultsDirectory.resolve("verificacion_java.csv"));
    }

    public static void printError(String message) {
        System.err.println(message);
    }
}
