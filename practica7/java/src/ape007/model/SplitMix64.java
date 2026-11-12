package ape007.model;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Locale;

/**
 * Generador pseudoaleatorio SplitMix64 reproducible.
 *
 * <p>El estado avanza con la constante dorada y cada salida se mezcla con dos
 * multiplicaciones y desplazamientos XOR. La conversion a double utiliza los
 * 53 bits superiores, igual que la implementacion Python, de modo que ambas
 * producen exactamente la misma secuencia.</p>
 */
public final class SplitMix64 {

    public static final long DEFAULT_SEED = 12345L;

    static final long GOLDEN_GAMMA = 0x9E3779B97F4A7C15L;
    static final long MIX1 = 0xBF58476D1CE4E5B9L;
    static final long MIX2 = 0x94D049BB133111EBL;
    static final double TWO_POW_MINUS_53 = 0x1.0p-53;

    private long state;

    public SplitMix64(long seed) {
        this.state = seed;
    }

    public void reset(long seed) {
        this.state = seed;
    }

    /** Devuelve el siguiente entero de 64 bits mezclado (bits sin signo). */
    public long nextU64() {
        state += GOLDEN_GAMMA;
        long z = state;
        z = (z ^ (z >>> 30)) * MIX1;
        z = (z ^ (z >>> 27)) * MIX2;
        return z ^ (z >>> 31);
    }

    /** Devuelve un valor pseudoaleatorio uniforme en [0, 1). */
    public double nextDouble() {
        return (nextU64() >>> 11) * TWO_POW_MINUS_53;
    }

    /** Representacion hexadecimal exacta de los bits IEEE 754 de un double. */
    public static String bitsHex(double value) {
        return String.format(Locale.ROOT, "%016x", Double.doubleToRawLongBits(value));
    }

    /**
     * Genera una muestra de verificacion y calcula SHA-256 sobre los bytes
     * little-endian de cada coordenada x e y.
     */
    public static Verification verifySequence(int pairs, long seed) {
        SplitMix64 rng = new SplitMix64(seed);
        MessageDigest digest;
        try {
            digest = MessageDigest.getInstance("SHA-256");
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 no disponible.", exception);
        }

        ByteBuffer buffer = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN);
        double[][] firstPairs = new double[Math.min(10, pairs)][2];

        for (int index = 1; index <= pairs; index++) {
            double x = rng.nextDouble();
            double y = rng.nextDouble();

            buffer.clear();
            buffer.putDouble(x);
            digest.update(buffer.array());

            buffer.clear();
            buffer.putDouble(y);
            digest.update(buffer.array());

            if (index <= 10) {
                firstPairs[index - 1][0] = x;
                firstPairs[index - 1][1] = y;
            }
        }

        StringBuilder hex = new StringBuilder();
        for (byte value : digest.digest()) {
            hex.append(String.format(Locale.ROOT, "%02x", value));
        }
        return new Verification(pairs, hex.toString(), firstPairs);
    }

    public record Verification(int pairs, String sha256, double[][] firstPairs) {
    }
}
