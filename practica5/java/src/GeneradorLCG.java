/**
 * Generador Congruencial Lineal (LCG) con aritmética modular de 32 bits.
 *
 * Fórmula:
 *     X(n+1) = (a * X(n) + c) mod m
 *     U(n)   = X(n) / m
 *
 * Para m = 2^32 se utiliza un {@code long} y una máscara de 32 bits. Así se
 * evita el desbordamiento con signo de {@code int} y se reproduce exactamente
 * el mismo resultado que la implementación de Python.
 */
public final class GeneradorLCG {

    public static final long MULTIPLICADOR_POR_DEFECTO = 1_664_525L;
    public static final long INCREMENTO_POR_DEFECTO = 1_013_904_223L;
    public static final long MODULO_POR_DEFECTO = 4_294_967_296L;
    public static final long SEMILLA_POR_DEFECTO = 12_345L;

    private final long multiplicador;
    private final long incremento;
    private final long modulo;
    private final boolean moduloPotenciaDeDos;
    private long estado;

    /**
     * Crea un generador con los parámetros indicados.
     *
     * @param multiplicador valor de a
     * @param incremento    valor de c
     * @param modulo        valor de m
     * @param semilla       valor inicial X(0)
     */
    public GeneradorLCG(long multiplicador, long incremento, long modulo, long semilla) {
        if (modulo <= 0) {
            throw new IllegalArgumentException("El módulo debe ser un entero positivo.");
        }
        if (multiplicador < 0 || incremento < 0) {
            throw new IllegalArgumentException(
                    "El multiplicador y el incremento no pueden ser negativos.");
        }
        if (semilla < 0 || semilla >= modulo) {
            throw new IllegalArgumentException(
                    "La semilla debe cumplir 0 <= semilla < " + modulo + ".");
        }

        this.multiplicador = multiplicador;
        this.incremento = incremento;
        this.modulo = modulo;
        this.moduloPotenciaDeDos = (modulo & (modulo - 1L)) == 0L;
        this.estado = semilla;
    }

    /** Crea un generador con los parámetros obligatorios de la práctica. */
    public static GeneradorLCG conParametrosPorDefecto(long semilla) {
        return new GeneradorLCG(
                MULTIPLICADOR_POR_DEFECTO,
                INCREMENTO_POR_DEFECTO,
                MODULO_POR_DEFECTO,
                semilla);
    }

    /**
     * Calcula el siguiente estado X(n+1) y actualiza el estado interno.
     *
     * Con m = 2^32, la máscara {@code 0xFFFFFFFFL} es equivalente a aplicar
     * módulo 2^32. El producto máximo de estos parámetros cabe holgadamente en
     * un {@code long} (aprox. 7.15e15 < 9.22e18).
     */
    public long siguiente() {
        long producto = multiplicador * estado + incremento;
        if (moduloPotenciaDeDos) {
            estado = producto & (modulo - 1L);
        } else {
            estado = producto % modulo;
        }
        return estado;
    }

    /** Convierte un valor X al intervalo [0, 1) mediante U = X / m. */
    public double normalizar(long valorX) {
        return (double) valorX / (double) modulo;
    }

    /** Devuelve el estado actual X(n). */
    public long getEstado() {
        return estado;
    }

    /** Devuelve el módulo configurado. */
    public long getModulo() {
        return modulo;
    }
}
