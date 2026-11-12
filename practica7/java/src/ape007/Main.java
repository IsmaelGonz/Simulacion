package ape007;

import ape007.controller.ExperimentController;
import ape007.model.SplitMix64;

import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Punto de entrada Java - APE 007 - Monte Carlo para estimar pi.
 */
public final class Main {

    private Main() {
    }

    public static void main(String[] args) {
        Path resultsDirectory;
        try {
            resultsDirectory = resolveResultsDirectory();
        } catch (IOException | URISyntaxException exception) {
            System.err.println("No se pudo determinar la carpeta de resultados: "
                    + exception.getMessage());
            System.exit(1);
            return;
        }

        try {
            Files.createDirectories(resultsDirectory);
            ExperimentController controller = new ExperimentController(
                    resultsDirectory, SplitMix64.DEFAULT_SEED);
            controller.run();
        } catch (IOException exception) {
            System.err.println("Error de entrada/salida: " + exception.getMessage());
            System.exit(1);
        }
    }

    private static Path resolveResultsDirectory()
            throws IOException, URISyntaxException {
        Path location = Paths.get(Main.class.getProtectionDomain()
                .getCodeSource().getLocation().toURI());
        Path projectRoot = location.getParent().getParent();
        return projectRoot.resolve("resultados");
    }
}
