package ape006;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;

/**
 * Programa principal de la practica APE 006 - implementacion Java.
 *
 * Uso:
 *   java -cp Java/out ape006.Main            # menu interactivo
 *   java -cp Java/out ape006.Main --all      # todos los resultados Java
 *   java -cp Java/out ape006.Main --generate 10000
 *   java -cp Java/out ape006.Main --chi
 *   java -cp Java/out ape006.Main --ks
 *   java -cp Java/out ape006.Main --compare
 */
public final class Main {
    private static final int DEFAULT_N = 10_000;

    private static Path projectRoot;
    private static Path dataDir;
    private static Path plotsDir;

    private static final class SequenceData {
        final int n;
        final long[] states;
        final double[] values;
        final String sha256;

        SequenceData(int n, long[] states, double[] values, String sha256) {
            this.n = n;
            this.states = states;
            this.values = values;
            this.sha256 = sha256;
        }
    }

    private Main() {
    }

    public static void main(String[] args) throws Exception {
        projectRoot = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        dataDir = projectRoot.resolve("Java").resolve("resultados").resolve("datos");
        plotsDir = projectRoot.resolve("Java").resolve("resultados").resolve("graficas");
        ensureDirectories();

        if (args.length == 0) {
            interactiveMenu();
            return;
        }

        boolean executed = false;
        for (int i = 0; i < args.length; i++) {
            String argument = args[i];
            switch (argument) {
                case "--all":
                    runAll(true);
                    executed = true;
                    break;
                case "--generate": {
                    int n = DEFAULT_N;
                    if (i + 1 < args.length && !args[i + 1].startsWith("--")) {
                        n = Integer.parseInt(args[++i]);
                    }
                    SequenceData sequence = generateSequence(n, true);
                    printSequence(sequence);
                    executed = true;
                    break;
                }
                case "--chi": {
                    double[] values = loadOrGenerateValues();
                    System.out.println(ChiSquareTest.formatReport(
                            ChiSquareTest.run(values, 10, 0.05)));
                    executed = true;
                    break;
                }
                case "--ks": {
                    double[] values = loadOrGenerateValues();
                    System.out.println(KolmogorovSmirnovTest.formatReport(
                            KolmogorovSmirnovTest.run(values, 0.05)));
                    executed = true;
                    break;
                }
                case "--compare":
                    ResultsComparator.compareAndReport(projectRoot, true);
                    executed = true;
                    break;
                case "--help":
                    printHelp();
                    executed = true;
                    break;
                default:
                    System.err.println("Argumento no reconocido: " + argument);
                    printHelp();
                    return;
            }
        }
        if (!executed) {
            interactiveMenu();
        }
    }

    private static void printHelp() {
        System.out.println("Uso: java -cp Java/out ape006.Main [opcion]");
        System.out.println("  --all              Generar todos los resultados Java");
        System.out.println("  --generate [N]     Generar una secuencia de N numeros");
        System.out.println("  --chi              Ejecutar Chi-cuadrado");
        System.out.println("  --ks               Ejecutar Kolmogorov-Smirnov");
        System.out.println("  --compare          Comparar resultados Python vs Java");
    }

    private static void ensureDirectories() throws IOException {
        Files.createDirectories(dataDir);
        Files.createDirectories(plotsDir);
    }

    private static SequenceData generateSequence(int n, boolean save) throws IOException {
        if (n < 0) {
            throw new IllegalArgumentException("La cantidad de numeros debe ser no negativa.");
        }
        Lcg generator = new Lcg();
        long[] states = generator.generateStates(n);
        double[] values = Lcg.valuesFromStates(states, generator.getModulus());
        String hash = ExportUtils.sha256States(states);
        if (save) {
            Path file = n == DEFAULT_N
                    ? dataDir.resolve("java_secuencia_10000.csv")
                    : dataDir.resolve("java_secuencia_" + n + ".csv");
            ExportUtils.writeSequenceCsv(file, states, values);
            ExportUtils.writeText(dataDir.resolve("muestra_java.txt"), sampleText(values, 10));
        }
        return new SequenceData(n, states, values, hash);
    }

    private static double[] loadOrGenerateValues() throws IOException {
        Path path = dataDir.resolve("java_secuencia_10000.csv");
        if (!Files.exists(path)) {
            return generateSequence(DEFAULT_N, true).values;
        }
        List<String> lines = Files.readAllLines(path);
        double[] values = new double[Math.max(0, lines.size() - 1)];
        int index = 0;
        for (int i = 1; i < lines.size(); i++) {
            String[] parts = lines.get(i).split(",");
            values[index++] = Double.parseDouble(parts[2]);
        }
        return values;
    }

    private static String sampleText(double[] values, int count) {
        StringBuilder sb = new StringBuilder();
        int length = Math.min(count, values.length);
        for (int i = 0; i < length; i++) {
            sb.append(String.format(Locale.US, "  U(%5d) = %.12f%n", i + 1, values[i]));
        }
        return sb.toString();
    }

    private static void printSequence(SequenceData sequence) {
        System.out.printf(Locale.US, "Secuencia de %d numeros generada.%n", sequence.n);
        System.out.println("SHA-256: " + sequence.sha256);
        System.out.print(sampleText(sequence.values, 10));
    }

    public static void runAll(boolean verbose) throws IOException {
        ensureDirectories();
        SequenceData sequence = generateSequence(DEFAULT_N, true);
        ChiSquareTest.Result chi = ChiSquareTest.run(sequence.values, 10, 0.05);
        KolmogorovSmirnovTest.Result ks = KolmogorovSmirnovTest.run(sequence.values, 0.05);

        ExportUtils.writeChiSquareCsv(dataDir.resolve("java_chi_cuadrado.csv"), chi);
        ExportUtils.writeText(dataDir.resolve("java_resultados.json"),
                buildResultsJson(sequence, chi, ks));

        Plots.plotHistogram(sequence.values, plotsDir.resolve("java_histograma.png"));
        Plots.plotChiSquare(chi, plotsDir.resolve("java_chi_cuadrado.png"));
        Plots.plotKs(sequence.values, ks, plotsDir.resolve("java_kolmogorov_smirnov.png"));

        if (verbose) {
            System.out.println("======================================================================");
            System.out.println("APE 006 - VALIDACION ESTADISTICA - JAVA");
            System.out.println("======================================================================");
            System.out.printf(Locale.US,
                    "Parametros LCG: semilla=%d, a=%d, c=%d, m=%d%n",
                    Lcg.DEFAULT_SEED, Lcg.DEFAULT_A, Lcg.DEFAULT_C, Lcg.DEFAULT_M);
            System.out.printf(Locale.US, "Secuencia generada: %d numeros%n", sequence.n);
            System.out.println("SHA-256 de estados: " + sequence.sha256);
            System.out.println("Muestra inicial:");
            System.out.print(sampleText(sequence.values, 10));
            System.out.println();
            System.out.println(ChiSquareTest.formatReport(chi));
            System.out.println(KolmogorovSmirnovTest.formatReport(ks));
            System.out.println("Archivos generados en: "
                    + projectRoot.resolve("Java").resolve("resultados"));
        }
    }

    private static String buildResultsJson(SequenceData sequence,
                                           ChiSquareTest.Result chi,
                                           KolmogorovSmirnovTest.Result ks) {
        double minimum = sequence.values.length > 0 ? sequence.values[0] : 0.0;
        double maximum = sequence.values.length > 0 ? sequence.values[0] : 0.0;
        for (double value : sequence.values) {
            minimum = Math.min(minimum, value);
            maximum = Math.max(maximum, value);
        }

        StringBuilder sb = new StringBuilder();
        sb.append("{\n");
        sb.append("  \"lenguaje\": \"Java\",\n");
        sb.append("  \"parametros\": {\n");
        sb.append("    \"semilla\": ").append(Lcg.DEFAULT_SEED).append(",\n");
        sb.append("    \"multiplicador\": ").append(Lcg.DEFAULT_A).append(",\n");
        sb.append("    \"incremento\": ").append(Lcg.DEFAULT_C).append(",\n");
        sb.append("    \"modulo\": ").append(Lcg.DEFAULT_M).append("\n");
        sb.append("  },\n");
        sb.append("  \"secuencia\": {\n");
        sb.append("    \"n\": ").append(sequence.n).append(",\n");
        sb.append("    \"sha256_estados\": ")
                .append(ExportUtils.jsonQuote(sequence.sha256)).append(",\n");
        sb.append("    \"primeros_estados\": ")
                .append(ExportUtils.jsonArray(
                        ExportUtils.firstLongValues(sequence.states, 10))).append(",\n");
        sb.append("    \"primeros_valores\": ")
                .append(ExportUtils.jsonArray(
                        ExportUtils.firstDoubleValues(sequence.values, 10))).append(",\n");
        sb.append("    \"minimo\": ").append(ExportUtils.jsonNumber(minimum)).append(",\n");
        sb.append("    \"maximo\": ").append(ExportUtils.jsonNumber(maximum)).append(",\n");
        sb.append("    \"archivo\": \"Java/resultados/datos/java_secuencia_10000.csv\"\n");
        sb.append("  },\n");

        sb.append("  \"chi_cuadrado\": {\n");
        sb.append("    \"prueba\": \"Chi-cuadrado\",\n");
        sb.append("    \"n\": ").append(chi.n).append(",\n");
        sb.append("    \"intervalos\": ").append(chi.bins).append(",\n");
        sb.append("    \"amplitud\": ").append(ExportUtils.jsonNumber(chi.amplitude)).append(",\n");
        sb.append("    \"etiquetas_intervalos\": ")
                .append(ExportUtils.jsonStringArray(chi.labels)).append(",\n");
        sb.append("    \"frecuencias_observadas\": ")
                .append(ExportUtils.jsonArray(chi.observed)).append(",\n");
        sb.append("    \"frecuencias_esperadas\": ")
                .append(ExportUtils.jsonArray(chi.expected)).append(",\n");
        sb.append("    \"estadistico\": ")
                .append(ExportUtils.jsonNumber(chi.statistic)).append(",\n");
        sb.append("    \"grados_libertad\": ").append(chi.degreesOfFreedom).append(",\n");
        sb.append("    \"alpha\": ").append(ExportUtils.jsonNumber(chi.alpha)).append(",\n");
        sb.append("    \"valor_p\": ").append(ExportUtils.jsonNumber(chi.pValue)).append(",\n");
        sb.append("    \"rechazar_h0\": ").append(chi.rejectH0).append(",\n");
        sb.append("    \"decision\": ").append(ExportUtils.jsonQuote(chi.decision)).append(",\n");
        sb.append("    \"interpretacion\": ")
                .append(ExportUtils.jsonQuote(chi.interpretation)).append("\n");
        sb.append("  },\n");

        sb.append("  \"kolmogorov_smirnov\": {\n");
        sb.append("    \"prueba\": \"Kolmogorov-Smirnov\",\n");
        sb.append("    \"n\": ").append(ks.n).append(",\n");
        sb.append("    \"d_mas\": ").append(ExportUtils.jsonNumber(ks.dPlus)).append(",\n");
        sb.append("    \"d_menos\": ").append(ExportUtils.jsonNumber(ks.dMinus)).append(",\n");
        sb.append("    \"estadistico_d\": ")
                .append(ExportUtils.jsonNumber(ks.statisticD)).append(",\n");
        sb.append("    \"indice_d_mas\": ").append(ks.dPlusIndex).append(",\n");
        sb.append("    \"indice_d_menos\": ").append(ks.dMinusIndex).append(",\n");
        sb.append("    \"valor_p\": ").append(ExportUtils.jsonNumber(ks.pValue)).append(",\n");
        sb.append("    \"alpha\": ").append(ExportUtils.jsonNumber(ks.alpha)).append(",\n");
        sb.append("    \"rechazar_h0\": ").append(ks.rejectH0).append(",\n");
        sb.append("    \"decision\": ").append(ExportUtils.jsonQuote(ks.decision)).append(",\n");
        sb.append("    \"interpretacion\": ")
                .append(ExportUtils.jsonQuote(ks.interpretation)).append("\n");
        sb.append("  },\n");

        sb.append("  \"entorno\": {\n");
        sb.append("    \"java_version\": ")
                .append(ExportUtils.jsonQuote(System.getProperty("java.version"))).append(",\n");
        sb.append("    \"java_vendor\": ")
                .append(ExportUtils.jsonQuote(System.getProperty("java.vendor"))).append(",\n");
        sb.append("    \"sistema_operativo\": ")
                .append(ExportUtils.jsonQuote(System.getProperty("os.name") + " "
                        + System.getProperty("os.version"))).append("\n");
        sb.append("  }\n");
        sb.append("}\n");
        return sb.toString();
    }

    private static void interactiveMenu() throws Exception {
        Scanner scanner = new Scanner(System.in);
        double[] currentValues = null;
        while (true) {
            System.out.println();
            System.out.println("==============================================================");
            System.out.println("APE 006 - SIMULACION - MENU PRINCIPAL (Java)");
            System.out.println("==============================================================");
            System.out.println("1. Generar numeros pseudoaleatorios");
            System.out.println("2. Ejecutar prueba Chi-cuadrado");
            System.out.println("3. Ejecutar prueba Kolmogorov-Smirnov");
            System.out.println("4. Ejecutar comparacion Python vs Java");
            System.out.println("5. Generar todas las pruebas y resultados");
            System.out.println("6. Salir");
            System.out.print("Seleccione una opcion: ");
            String option = scanner.nextLine().trim();

            switch (option) {
                case "1": {
                    System.out.printf(Locale.US, "Cantidad de numeros [%d]: ", DEFAULT_N);
                    String raw = scanner.nextLine().trim();
                    int n = raw.isEmpty() ? DEFAULT_N : Integer.parseInt(raw);
                    SequenceData sequence = generateSequence(n, true);
                    currentValues = sequence.values;
                    printSequence(sequence);
                    break;
                }
                case "2":
                    currentValues = currentValues == null
                            ? loadOrGenerateValues() : currentValues;
                    System.out.println(ChiSquareTest.formatReport(
                            ChiSquareTest.run(currentValues, 10, 0.05)));
                    break;
                case "3":
                    currentValues = currentValues == null
                            ? loadOrGenerateValues() : currentValues;
                    System.out.println(KolmogorovSmirnovTest.formatReport(
                            KolmogorovSmirnovTest.run(currentValues, 0.05)));
                    break;
                case "4":
                    ResultsComparator.compareAndReport(projectRoot, true);
                    break;
                case "5":
                    runAll(true);
                    break;
                case "6":
                    System.out.println("Hasta luego.");
                    scanner.close();
                    return;
                default:
                    System.out.println("Opcion no valida.");
            }
        }
    }
}
