import java.io.BufferedWriter;
import java.io.FileDescriptor;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Locale;

/**
 * Punto de entrada de la implementación Java de la práctica LCG.
 *
 * Sin argumentos genera dos archivos CSV: uno con la semilla 12 345 y otro con
 * la semilla 54 321. También acepta la forma:
 *
 *     java -cp java/out Main <semilla> <archivo_salida>
 */
public final class Main {

    private static final int CANTIDAD = 10_000;
    private static final long SEMILLA_ALTERNA = 54_321L;
    private static final int VALORES_VISIBLES = 5;

    private Main() {
        // Clase de utilidad: no se instancia.
    }

    public static void main(String[] args) throws IOException {
        configurarSalidaUtf8();
        Path raizProyecto = buscarRaizProyecto();
        Path directorioResultados = raizProyecto.resolve("java").resolve("resultados");

        System.out.println("=".repeat(72));
        System.out.println("PRÁCTICA 05 - GENERADOR CONGRUENCIAL LINEAL (LCG) - JAVA");
        System.out.println("=".repeat(72));
        System.out.printf(Locale.ROOT, "a (multiplicador) = %d%n",
                GeneradorLCG.MULTIPLICADOR_POR_DEFECTO);
        System.out.printf(Locale.ROOT, "c (incremento)    = %d%n",
                GeneradorLCG.INCREMENTO_POR_DEFECTO);
        System.out.printf(Locale.ROOT, "m (módulo)        = %d%n",
                GeneradorLCG.MODULO_POR_DEFECTO);
        System.out.printf(Locale.ROOT, "cantidad          = %d%n", CANTIDAD);

        if (args.length == 0) {
            generarYGuardar(
                    GeneradorLCG.SEMILLA_POR_DEFECTO,
                    directorioResultados.resolve("secuencia_java.csv"));
            generarYGuardar(
                    SEMILLA_ALTERNA,
                    directorioResultados.resolve("secuencia_java_semilla_54321.csv"));
        } else if (args.length == 2) {
            long semilla = Long.parseLong(args[0]);
            Path rutaSalida = Paths.get(args[1]);
            generarYGuardar(semilla, rutaSalida);
        } else {
            System.out.println("Uso:");
            System.out.println("  java -cp java/out Main");
            System.out.println("  java -cp java/out Main <semilla> <archivo_salida>");
            return;
        }

        System.out.println();
        System.out.println("Proceso de Java finalizado correctamente.");
        System.out.println(
                "Ejecute comparacion/comparar.py para verificar la igualdad con Python.");
    }

    /**
     * Genera {@link #CANTIDAD} valores con la semilla indicada y los guarda en CSV.
     */
    private static void generarYGuardar(long semilla, Path rutaSalida) throws IOException {
        Path rutaAbsoluta = rutaSalida.toAbsolutePath();
        Files.createDirectories(rutaAbsoluta.getParent());

        GeneradorLCG generador = GeneradorLCG.conParametrosPorDefecto(semilla);
        long[] primerosX = new long[VALORES_VISIBLES];
        double[] primerosU = new double[VALORES_VISIBLES];

        try (BufferedWriter escritor = Files.newBufferedWriter(
                rutaSalida, StandardCharsets.UTF_8)) {
            escritor.write("iteracion,X,U\n");

            for (int iteracion = 1; iteracion <= CANTIDAD; iteracion++) {
                long x = generador.siguiente();
                double u = generador.normalizar(x);
                escritor.write(String.format(
                        Locale.ROOT, "%d,%d,%.12f\n", iteracion, x, u));

                if (iteracion <= VALORES_VISIBLES) {
                    primerosX[iteracion - 1] = x;
                    primerosU[iteracion - 1] = u;
                }
            }
        }

        System.out.println();
        System.out.printf(Locale.ROOT, "Secuencia generada con semilla %d%n", semilla);
        System.out.printf(Locale.ROOT, "Primeros %d valores:%n", VALORES_VISIBLES);
        System.out.printf(Locale.ROOT, "%6s  %12s  %14s%n", "n", "X(n)", "U(n)");
        System.out.println("-".repeat(38));
        for (int i = 0; i < VALORES_VISIBLES; i++) {
            System.out.printf(
                    Locale.ROOT, "%6d  %12d  %14.12f%n",
                    i + 1, primerosX[i], primerosU[i]);
        }
        System.out.printf(Locale.ROOT, "CSV guardado en: %s%n", rutaAbsoluta);
    }

    /** Fuerza UTF-8 en la consola para mostrar correctamente tildes y símbolos. */
    private static void configurarSalidaUtf8() {
        System.setOut(new PrintStream(
                new FileOutputStream(FileDescriptor.out), true, StandardCharsets.UTF_8));
        System.setErr(new PrintStream(
                new FileOutputStream(FileDescriptor.err), true, StandardCharsets.UTF_8));
    }

    /**
     * Busca la raíz del proyecto subiendo desde el directorio actual. Esto permite
     * ejecutar el programa desde la raíz o desde la carpeta java sin cambiar las
     * rutas de salida.
     */
    private static Path buscarRaizProyecto() {
        Path actual = Paths.get("").toAbsolutePath();
        while (actual != null) {
            if (Files.exists(actual.resolve("java").resolve("src").resolve("Main.java"))) {
                return actual;
            }
            actual = actual.getParent();
        }
        return Paths.get("").toAbsolutePath();
    }
}
