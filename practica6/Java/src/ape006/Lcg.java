package ape006;

/**
 * Generador congruencial lineal reproducible.
 *
 * X(n+1) = (a * X(n) + c) mod m
 * U(n+1) = X(n+1) / m
 *
 * Los parametros por defecto coinciden exactamente con la implementacion
 * Python para poder comparar las secuencias.
 */
public final class Lcg {
    public static final long DEFAULT_SEED = 12345L;
    public static final long DEFAULT_A = 1664525L;
    public static final long DEFAULT_C = 1013904223L;
    public static final long DEFAULT_M = 1L << 32; // 4294967296

    private final long seed;
    private final long a;
    private final long c;
    private final long m;
    private long state;

    public Lcg() {
        this(DEFAULT_SEED, DEFAULT_A, DEFAULT_C, DEFAULT_M);
    }

    public Lcg(long seed, long a, long c, long m) {
        if (m <= 1L) {
            throw new IllegalArgumentException("El modulo m debe ser mayor que 1.");
        }
        if (seed < 0L || seed >= m) {
            throw new IllegalArgumentException("La semilla debe cumplir 0 <= semilla < m.");
        }
        if (a <= 0L || a >= m) {
            throw new IllegalArgumentException("El multiplicador debe cumplir 0 < a < m.");
        }
        if (c < 0L || c >= m) {
            throw new IllegalArgumentException("El incremento debe cumplir 0 <= c < m.");
        }
        this.seed = seed;
        this.a = a;
        this.c = c;
        this.m = m;
        this.state = seed;
    }

    public long getSeed() { return seed; }
    public long getMultiplier() { return a; }
    public long getIncrement() { return c; }
    public long getModulus() { return m; }
    public long getState() { return state; }

    public void reset() {
        this.state = seed;
    }

    public long nextState() {
        // Con m = 2^32 y valores de 32 bits, la operacion cabe en long.
        state = (a * state + c) % m;
        return state;
    }

    public double nextU() {
        return (double) nextState() / (double) m;
    }

    public long[] generateStates(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("La cantidad de numeros debe ser no negativa.");
        }
        long[] states = new long[n];
        for (int i = 0; i < n; i++) {
            states[i] = nextState();
        }
        return states;
    }

    public double[] generate(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("La cantidad de numeros debe ser no negativa.");
        }
        double[] values = new double[n];
        for (int i = 0; i < n; i++) {
            values[i] = nextU();
        }
        return values;
    }

    public static double[] valuesFromStates(long[] states, long modulus) {
        double[] values = new double[states.length];
        for (int i = 0; i < states.length; i++) {
            values[i] = (double) states[i] / (double) modulus;
        }
        return values;
    }
}
