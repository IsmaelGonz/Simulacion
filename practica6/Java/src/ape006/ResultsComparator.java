package ape006;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Comparador de los archivos JSON producidos por Python y Java.
 *
 * No ejecuta la implementacion Python; compara archivos ya generados. La
 * comparacion orquestada (generar ambos y comparar) se realiza con
 * comparacion_resultados.py.
 */
public final class ResultsComparator {

    private static final double TOLERANCE_SEQUENCE = 1.0e-15;
    private static final double TOLERANCE_STATISTIC = 1.0e-9;
    private static final double TOLERANCE_KS = 1.0e-12;
    private static final double TOLERANCE_P = 1.0e-6;

    private ResultsComparator() {
    }

    private static final class Check {
        final String name;
        final boolean passed;
        final String detail;

        Check(String name, boolean passed, String detail) {
            this.name = name;
            this.passed = passed;
            this.detail = detail;
        }
    }

    public static boolean compareAndReport(Path projectRoot, boolean print) throws IOException {
        Path pythonJson = projectRoot.resolve("Python/resultados/datos/python_resultados.json");
        Path javaJson = projectRoot.resolve("Java/resultados/datos/java_resultados.json");

        if (!Files.exists(pythonJson) || !Files.exists(javaJson)) {
            String message = "Faltan resultados para comparar. Ejecute primero:\n"
                    + "  py Python/main.py --all\n"
                    + "  java -cp Java/out ape006.Main --all\n"
                    + "o use: py comparacion_resultados.py";
            if (print) {
                System.out.println(message);
            }
            return false;
        }

        String python = Files.readString(pythonJson, StandardCharsets.UTF_8);
        String java = Files.readString(javaJson, StandardCharsets.UTF_8);

        List<Check> checks = new ArrayList<>();
        checks.add(new Check("Parametros del LCG",
                parametersMatch(python, java),
                "semilla, multiplicador, incremento y modulo"));
        String pythonHash = extractString(python, "sha256_estados");
        String javaHash = extractString(java, "sha256_estados");
        checks.add(new Check("Secuencia de 10 000 numeros",
                pythonHash != null && pythonHash.equals(javaHash),
                "SHA-256 estados Python=" + pythonHash + ", Java=" + javaHash));

        double[] pythonFirstValues = extractDoubleArray(python, "primeros_valores");
        double[] javaFirstValues = extractDoubleArray(java, "primeros_valores");
        checks.add(new Check("Primeros 10 valores",
                arraysMatch(pythonFirstValues, javaFirstValues, TOLERANCE_SEQUENCE),
                "comparacion numerica con tolerancia " + TOLERANCE_SEQUENCE));

        int[] pythonObserved = extractIntArray(python, "frecuencias_observadas");
        int[] javaObserved = extractIntArray(java, "frecuencias_observadas");
        checks.add(new Check("Frecuencias observadas Chi-cuadrado",
                intArraysEqual(pythonObserved, javaObserved),
                arrayText(pythonObserved) + " vs " + arrayText(javaObserved)));

        double pythonChi = extractNumber(python, "estadistico", 1);
        double javaChi = extractNumber(java, "estadistico", 1);
        checks.add(new Check("Estadistico Chi-cuadrado",
                close(pythonChi, javaChi, TOLERANCE_STATISTIC),
                String.format(Locale.US, "Python=%.12f, Java=%.12f", pythonChi, javaChi)));

        int pythonGl = (int) extractNumber(python, "grados_libertad", 1);
        int javaGl = (int) extractNumber(java, "grados_libertad", 1);
        checks.add(new Check("Grados de libertad", pythonGl == javaGl,
                "Python=" + pythonGl + ", Java=" + javaGl));

        double pythonChiP = extractNumber(python, "valor_p", 1);
        double javaChiP = extractNumber(java, "valor_p", 1);
        checks.add(new Check("Valor p Chi-cuadrado",
                close(pythonChiP, javaChiP, TOLERANCE_P),
                String.format(Locale.US, "Python=%.12f, Java=%.12f", pythonChiP, javaChiP)));

        double pythonDPlus = extractNumber(python, "d_mas", 1);
        double javaDPlus = extractNumber(java, "d_mas", 1);
        double pythonDMinus = extractNumber(python, "d_menos", 1);
        double javaDMinus = extractNumber(java, "d_menos", 1);
        double pythonD = extractNumber(python, "estadistico_d", 1);
        double javaD = extractNumber(java, "estadistico_d", 1);
        checks.add(new Check("Estadisticos KS D+ y D-",
                close(pythonDPlus, javaDPlus, TOLERANCE_KS)
                        && close(pythonDMinus, javaDMinus, TOLERANCE_KS),
                String.format(Locale.US,
                        "Python D+=%.12f D-=%.12f, Java D+=%.12f D-=%.12f",
                        pythonDPlus, pythonDMinus, javaDPlus, javaDMinus)));
        checks.add(new Check("Estadistico KS D",
                close(pythonD, javaD, TOLERANCE_KS),
                String.format(Locale.US, "Python=%.12f, Java=%.12f", pythonD, javaD)));

        double pythonKsP = extractNumber(python, "valor_p", 2);
        double javaKsP = extractNumber(java, "valor_p", 2);
        checks.add(new Check("Valor p Kolmogorov-Smirnov",
                close(pythonKsP, javaKsP, TOLERANCE_P),
                String.format(Locale.US, "Python=%.12f, Java=%.12f", pythonKsP, javaKsP)));

        List<Boolean> pythonDecisions = extractBooleans(python, "rechazar_h0");
        List<Boolean> javaDecisions = extractBooleans(java, "rechazar_h0");
        checks.add(new Check("Decisiones estadisticas",
                pythonDecisions.equals(javaDecisions),
                "Python=" + pythonDecisions + ", Java=" + javaDecisions));

        boolean allPassed = checks.stream().allMatch(check -> check.passed);

        if (print) {
            System.out.println();
            System.out.println("COMPARACION PYTHON VS JAVA (desde Java)");
            System.out.println("--------------------------------------------------------------------");
            for (Check check : checks) {
                System.out.printf(Locale.US, "[%s] %s: %s%n",
                        check.passed ? "OK" : "FALLA", check.name, check.detail);
            }
            System.out.println("--------------------------------------------------------------------");
            System.out.println(allPassed
                    ? "RESULTADO: las implementaciones son equivalentes."
                    : "RESULTADO: se encontraron diferencias.");
        }
        return allPassed;
    }

    private static boolean parametersMatch(String python, String java) {
        return (int) extractNumber(python, "semilla", 1) == (int) extractNumber(java, "semilla", 1)
                && (long) extractNumber(python, "multiplicador", 1)
                        == (long) extractNumber(java, "multiplicador", 1)
                && (long) extractNumber(python, "incremento", 1)
                        == (long) extractNumber(java, "incremento", 1)
                && (long) extractNumber(python, "modulo", 1)
                        == (long) extractNumber(java, "modulo", 1);
    }

    private static String extractString(String json, String key) {
        Matcher matcher = Pattern.compile("\"" + Pattern.quote(key) + "\"\\s*:\\s*\"([^\"]*)\"")
                .matcher(json);
        return matcher.find() ? matcher.group(1) : null;
    }

    private static double extractNumber(String json, String key, int occurrence) {
        Matcher matcher = Pattern.compile("\"" + Pattern.quote(key)
                + "\"\\s*:\\s*([-+]?[0-9]*\\.?[0-9]+(?:[eE][-+]?[0-9]+)?)").matcher(json);
        int count = 0;
        while (matcher.find()) {
            count++;
            if (count == occurrence) {
                return Double.parseDouble(matcher.group(1));
            }
        }
        throw new IllegalArgumentException("No se encontro la clave " + key
                + " (ocurrencia " + occurrence + ")");
    }

    private static int[] extractIntArray(String json, String key) {
        double[] values = extractDoubleArray(json, key);
        int[] result = new int[values.length];
        for (int i = 0; i < values.length; i++) {
            result[i] = (int) values[i];
        }
        return result;
    }

    private static double[] extractDoubleArray(String json, String key) {
        Matcher matcher = Pattern.compile("\"" + Pattern.quote(key) + "\"\\s*:\\s*\\[([^\\]]*)\\]")
                .matcher(json);
        if (!matcher.find()) {
            return new double[0];
        }
        String content = matcher.group(1).trim();
        if (content.isEmpty()) {
            return new double[0];
        }
        String[] parts = content.split(",");
        double[] values = new double[parts.length];
        for (int i = 0; i < parts.length; i++) {
            values[i] = Double.parseDouble(parts[i].trim());
        }
        return values;
    }

    private static List<Boolean> extractBooleans(String json, String key) {
        Matcher matcher = Pattern.compile("\"" + Pattern.quote(key) + "\"\\s*:\\s*(true|false)")
                .matcher(json);
        List<Boolean> values = new ArrayList<>();
        while (matcher.find()) {
            values.add(Boolean.parseBoolean(matcher.group(1)));
        }
        return values;
    }

    private static boolean close(double left, double right, double tolerance) {
        return Math.abs(left - right) <= tolerance
                || Math.abs(left - right) <= tolerance * Math.max(1.0, Math.abs(left));
    }

    private static boolean arraysMatch(double[] left, double[] right, double tolerance) {
        if (left.length != right.length) {
            return false;
        }
        for (int i = 0; i < left.length; i++) {
            if (!close(left[i], right[i], tolerance)) {
                return false;
            }
        }
        return true;
    }

    private static boolean intArraysEqual(int[] left, int[] right) {
        if (left.length != right.length) {
            return false;
        }
        for (int i = 0; i < left.length; i++) {
            if (left[i] != right[i]) {
                return false;
            }
        }
        return true;
    }

    private static String arrayText(int[] values) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                sb.append(", ");
            }
            sb.append(values[i]);
        }
        return sb.append(']').toString();
    }

}
