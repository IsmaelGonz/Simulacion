package ape006;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Locale;

/**
 * Utilidades de exportacion (CSV, JSON, SHA-256 y archivos de texto).
 */
public final class ExportUtils {

    private ExportUtils() {
    }

    public static String sha256States(long[] states) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            for (long state : states) {
                digest.update((byte) (state & 0xFF));
                digest.update((byte) ((state >>> 8) & 0xFF));
                digest.update((byte) ((state >>> 16) & 0xFF));
                digest.update((byte) ((state >>> 24) & 0xFF));
            }
            byte[] hash = digest.digest();
            StringBuilder sb = new StringBuilder(hash.length * 2);
            for (byte b : hash) {
                sb.append(String.format(Locale.US, "%02x", b & 0xFF));
            }
            return sb.toString();
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 no disponible.", exception);
        }
    }

    public static void writeSequenceCsv(Path path, long[] states, double[] values)
            throws IOException {
        Files.createDirectories(path.getParent());
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("indice,estado,u\n");
            for (int i = 0; i < states.length; i++) {
                writer.write(String.format(Locale.US, "%d,%d,%s%n",
                        i + 1, states[i], Double.toString(values[i])));
            }
        }
    }

    public static void writeChiSquareCsv(Path path, ChiSquareTest.Result result)
            throws IOException {
        Files.createDirectories(path.getParent());
        try (BufferedWriter writer = Files.newBufferedWriter(path, StandardCharsets.UTF_8)) {
            writer.write("intervalo,observado,esperado,diferencia\n");
            for (int i = 0; i < result.bins; i++) {
                writer.write(String.format(Locale.US, "%s,%d,%s,%s%n",
                        result.labels.get(i), result.observed[i],
                        Double.toString(result.expected[i]),
                        Double.toString(result.observed[i] - result.expected[i])));
            }
        }
    }

    public static void writeText(Path path, String text) throws IOException {
        Files.createDirectories(path.getParent());
        Files.writeString(path, text, StandardCharsets.UTF_8);
    }

    public static String jsonQuote(String value) {
        if (value == null) {
            return "null";
        }
        StringBuilder sb = new StringBuilder(value.length() + 2);
        sb.append('"');
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (c < 0x20) {
                        sb.append(String.format(Locale.US, "\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
        return sb.toString();
    }

    public static String jsonNumber(double value) {
        if (Double.isNaN(value) || Double.isInfinite(value)) {
            throw new IllegalArgumentException("Valor no finito en JSON: " + value);
        }
        return Double.toString(value);
    }

    public static String jsonArray(int[] values) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(values[i]);
        }
        return sb.append(']').toString();
    }

    public static String jsonArray(long[] values) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(values[i]);
        }
        return sb.append(']').toString();
    }

    public static String jsonArray(double[] values) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(jsonNumber(values[i]));
        }
        return sb.append(']').toString();
    }

    public static String jsonStringArray(List<String> values) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < values.size(); i++) {
            if (i > 0) {
                sb.append(',');
            }
            sb.append(jsonQuote(values.get(i)));
        }
        return sb.append(']').toString();
    }

    public static double[] firstDoubleValues(double[] values, int count) {
        int length = Math.min(count, values.length);
        double[] result = new double[length];
        System.arraycopy(values, 0, result, 0, length);
        return result;
    }

    public static long[] firstLongValues(long[] values, int count) {
        int length = Math.min(count, values.length);
        long[] result = new long[length];
        System.arraycopy(values, 0, result, 0, length);
        return result;
    }
}
