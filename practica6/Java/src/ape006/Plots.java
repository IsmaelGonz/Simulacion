package ape006;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Locale;

import javax.imageio.ImageIO;

/**
 * Generacion de graficas PNG con Java2D, sin bibliotecas externas.
 */
public final class Plots {
    private static final int WIDTH = 1100;
    private static final int HEIGHT = 680;
    private static final int LEFT = 95;
    private static final int RIGHT = 45;
    private static final int TOP = 75;
    private static final int BOTTOM = 105;

    private static final Color BLUE = new Color(37, 99, 235);
    private static final Color LIGHT_BLUE = new Color(59, 130, 246);
    private static final Color RED = new Color(220, 38, 38);
    private static final Color AMBER = new Color(245, 158, 11);
    private static final Color GRID = new Color(220, 220, 220);
    private static final Color AXIS = new Color(60, 60, 60);

    private Plots() {
    }

    public static void plotHistogram(double[] values, Path path) throws IOException {
        int bins = 20;
        int[] counts = new int[bins];
        for (double value : values) {
            int index = (int) (value * bins);
            if (index >= bins) {
                index = bins - 1;
            }
            counts[index]++;
        }

        double binWidth = 1.0 / bins;
        double[] density = new double[bins];
        double maxDensity = 1.0;
        for (int i = 0; i < bins; i++) {
            density[i] = counts[i] / (values.length * binWidth);
            maxDensity = Math.max(maxDensity, density[i]);
        }

        BufferedImage image = newCanvas();
        Graphics2D g2 = image.createGraphics();
        configure(g2);
        drawTitle(g2, "Histograma de 10 000 numeros pseudoaleatorios del LCG");
        drawAxes(g2, "Valor pseudoaleatorio U", "Densidad");

        double yMax = maxDensity * 1.10;
        int[] ticks = {0, 1, 2, 3, 4, 5};
        for (int tick : ticks) {
            double y = tick * (1.0 / 5.0) * yMax;
            drawHorizontalGrid(g2, y, 0.0, yMax);
            g2.setColor(AXIS);
            g2.drawString(format(tick * (1.0 / 5.0) * yMax, 2), LEFT - 42, mapY(y, 0.0, yMax) + 5);
        }

        int plotWidth = plotWidth();
        int barWidth = Math.max(1, plotWidth / bins - 2);
        for (int i = 0; i < bins; i++) {
            int x = mapX(i * binWidth, 0.0, 1.0);
            int yTop = mapY(density[i], 0.0, yMax);
            g2.setColor(LIGHT_BLUE);
            g2.fillRect(x + 1, yTop, barWidth, mapY(0.0, 0.0, yMax) - yTop);
            g2.setColor(Color.WHITE);
            g2.setStroke(new BasicStroke(1.0f));
            g2.drawRect(x + 1, yTop, barWidth, mapY(0.0, 0.0, yMax) - yTop);
        }

        g2.setColor(RED);
        g2.setStroke(new BasicStroke(2.5f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER,
                10.0f, new float[]{9.0f, 7.0f}, 0.0f));
        int yOne = mapY(1.0, 0.0, yMax);
        g2.drawLine(LEFT, yOne, WIDTH - RIGHT, yOne);

        drawLegend(g2, new String[]{"Densidad observada", "Densidad teorica U(0,1) = 1"},
                new Color[]{LIGHT_BLUE, RED}, WIDTH - RIGHT - 330, TOP + 12, true);

        drawXTicks(g2, new double[]{0.0, 0.2, 0.4, 0.6, 0.8, 1.0}, 0.0, 1.0);
        g2.dispose();
        save(image, path);
    }

    public static void plotChiSquare(ChiSquareTest.Result result, Path path) throws IOException {
        int bins = result.observed.length;
        double maxValue = 0.0;
        for (int i = 0; i < bins; i++) {
            maxValue = Math.max(maxValue, Math.max(result.observed[i], result.expected[i]));
        }
        double yMax = maxValue * 1.18;

        BufferedImage image = newCanvas();
        Graphics2D g2 = image.createGraphics();
        configure(g2);
        drawTitle(g2, String.format(Locale.US,
                "Chi-cuadrado: observadas vs esperadas  (chi2 = %.4f, gl = %d, p = %.6f)",
                result.statistic, result.degreesOfFreedom, result.pValue));
        drawAxes(g2, "Intervalo de U(0,1)", "Frecuencia (cantidad de numeros)");

        for (int tick = 0; tick <= 5; tick++) {
            double y = tick * yMax / 5.0;
            drawHorizontalGrid(g2, y, 0.0, yMax);
            g2.setColor(AXIS);
            g2.drawString(format(y, 0), LEFT - 55, mapY(y, 0.0, yMax) + 5);
        }

        double groupWidth = plotWidth() / (double) bins;
        double barWidth = groupWidth * 0.36;
        for (int i = 0; i < bins; i++) {
            double center = (i + 0.5) / bins;
            double xObserved = mapX(center, 0.0, 1.0) - barWidth / 2.0;
            double xExpected = mapX(center, 0.0, 1.0) + barWidth / 2.0;

            int observedTop = mapY(result.observed[i], 0.0, yMax);
            int expectedTop = mapY(result.expected[i], 0.0, yMax);
            int base = mapY(0.0, 0.0, yMax);

            g2.setColor(BLUE);
            g2.fillRect((int) xObserved, observedTop, (int) barWidth, base - observedTop);
            g2.setColor(AMBER);
            g2.fillRect((int) xExpected, expectedTop, (int) barWidth, base - expectedTop);
        }

        drawRotatedLabels(g2, result.labels, 0.0, 1.0);
        drawLegend(g2, new String[]{"Frecuencia observada", "Frecuencia esperada"},
                new Color[]{BLUE, AMBER}, WIDTH - RIGHT - 300, TOP + 12, false);

        g2.dispose();
        save(image, path);
    }

    public static void plotKs(double[] values, KolmogorovSmirnovTest.Result result,
                              Path path) throws IOException {
        double[] ordered = values.clone();
        Arrays.sort(ordered);
        int n = ordered.length;

        BufferedImage image = newCanvas();
        Graphics2D g2 = image.createGraphics();
        configure(g2);
        drawTitle(g2, String.format(Locale.US,
                "Kolmogorov-Smirnov: ECDF vs U(0,1)  (D+ = %.6f, D- = %.6f, D = %.6f, p = %.6f)",
                result.dPlus, result.dMinus, result.statisticD, result.pValue));
        drawAxes(g2, "Valor x", "Probabilidad acumulada F(x)");

        for (int tick = 0; tick <= 5; tick++) {
            double value = tick / 5.0;
            drawHorizontalGrid(g2, value, 0.0, 1.02);
            g2.setColor(AXIS);
            int y = mapY(value, 0.0, 1.02);
            g2.drawString(format(value, 1), LEFT - 45, y + 5);
        }
        drawXTicks(g2, new double[]{0.0, 0.2, 0.4, 0.6, 0.8, 1.0}, 0.0, 1.0);

        g2.setColor(RED);
        g2.setStroke(new BasicStroke(2.0f, BasicStroke.CAP_BUTT, BasicStroke.JOIN_MITER,
                10.0f, new float[]{9.0f, 7.0f}, 0.0f));
        g2.drawLine(mapX(0.0, 0.0, 1.0), mapY(0.0, 0.0, 1.02),
                mapX(1.0, 0.0, 1.0), mapY(1.0, 0.0, 1.02));

        g2.setColor(BLUE);
        g2.setStroke(new BasicStroke(1.8f));
        int previousX = mapX(0.0, 0.0, 1.0);
        int previousY = mapY(0.0, 0.0, 1.02);
        for (int i = 0; i < n; i++) {
            int x = mapX(ordered[i], 0.0, 1.0);
            g2.drawLine(previousX, previousY, x, previousY);
            int y = mapY((i + 1) / (double) n, 0.0, 1.02);
            g2.drawLine(x, previousY, x, y);
            previousX = x;
            previousY = y;
        }
        g2.drawLine(previousX, previousY, mapX(1.0, 0.0, 1.0), previousY);

        drawLegend(g2, new String[]{"Distribucion empirica F_n(x)", "Distribucion teorica F(x) = x"},
                new Color[]{BLUE, RED}, WIDTH - RIGHT - 370, HEIGHT - BOTTOM - 80, true);

        g2.dispose();
        save(image, path);
    }

    private static BufferedImage newCanvas() {
        BufferedImage image = new BufferedImage(WIDTH, HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g2 = image.createGraphics();
        configure(g2);
        g2.setColor(Color.WHITE);
        g2.fillRect(0, 0, WIDTH, HEIGHT);
        g2.dispose();
        return image;
    }

    private static void configure(Graphics2D g2) {
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,
                RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        g2.setFont(new Font("SansSerif", Font.PLAIN, 13));
    }

    private static void drawTitle(Graphics2D g2, String title) {
        g2.setColor(Color.DARK_GRAY);
        g2.setFont(new Font("SansSerif", Font.BOLD, 16));
        FontMetrics metrics = g2.getFontMetrics();
        int x = (WIDTH - metrics.stringWidth(title)) / 2;
        g2.drawString(title, Math.max(10, x), 32);
    }

    private static void drawAxes(Graphics2D g2, String xLabel, String yLabel) {
        g2.setColor(AXIS);
        g2.setStroke(new BasicStroke(1.3f));
        g2.drawLine(LEFT, TOP, LEFT, HEIGHT - BOTTOM);
        g2.drawLine(LEFT, HEIGHT - BOTTOM, WIDTH - RIGHT, HEIGHT - BOTTOM);

        g2.setFont(new Font("SansSerif", Font.PLAIN, 13));
        FontMetrics metrics = g2.getFontMetrics();
        int x = LEFT + (plotWidth() - metrics.stringWidth(xLabel)) / 2;
        g2.drawString(xLabel, x, HEIGHT - 32);

        AffineTransform original = g2.getTransform();
        g2.rotate(-Math.PI / 2.0, 28, HEIGHT / 2.0);
        int y = (int) (HEIGHT / 2.0 + metrics.stringWidth(yLabel) / 2.0);
        g2.drawString(yLabel, 28, y);
        g2.setTransform(original);
    }

    private static void drawHorizontalGrid(Graphics2D g2, double value,
                                           double yMin, double yMax) {
        g2.setColor(GRID);
        g2.setStroke(new BasicStroke(1.0f));
        int y = mapY(value, yMin, yMax);
        g2.drawLine(LEFT, y, WIDTH - RIGHT, y);
    }

    private static void drawXTicks(Graphics2D g2, double[] values,
                                   double xMin, double xMax) {
        g2.setColor(AXIS);
        g2.setStroke(new BasicStroke(1.0f));
        FontMetrics metrics = g2.getFontMetrics();
        for (double value : values) {
            int x = mapX(value, xMin, xMax);
            g2.drawLine(x, HEIGHT - BOTTOM, x, HEIGHT - BOTTOM + 5);
            String text = format(value, 1);
            g2.drawString(text, x - metrics.stringWidth(text) / 2, HEIGHT - BOTTOM + 22);
        }
    }

    private static void drawRotatedLabels(Graphics2D g2, java.util.List<String> labels,
                                          double xMin, double xMax) {
        g2.setColor(AXIS);
        g2.setFont(new Font("SansSerif", Font.PLAIN, 11));
        int bins = labels.size();
        for (int i = 0; i < bins; i++) {
            double center = (i + 0.5) / bins;
            int x = mapX(center, xMin, xMax);
            int y = HEIGHT - BOTTOM + 12;
            AffineTransform original = g2.getTransform();
            g2.rotate(-Math.toRadians(35.0), x, y);
            g2.drawString(labels.get(i), x - 12, y + 4);
            g2.setTransform(original);
        }
    }

    private static void drawLegend(Graphics2D g2, String[] labels, Color[] colors,
                                   int x, int y, boolean lineStyle) {
        g2.setFont(new Font("SansSerif", Font.PLAIN, 12));
        int rowHeight = 22;
        for (int i = 0; i < labels.length; i++) {
            int rowY = y + i * rowHeight;
            g2.setColor(colors[i]);
            if (lineStyle) {
                g2.setStroke(new BasicStroke(3.0f));
                g2.drawLine(x, rowY, x + 28, rowY);
            } else {
                g2.fillRect(x, rowY - 7, 22, 13);
            }
            g2.setColor(Color.DARK_GRAY);
            g2.drawString(labels[i], x + 38, rowY + 4);
        }
    }

    private static void save(BufferedImage image, Path path) throws IOException {
        Files.createDirectories(path.getParent());
        ImageIO.write(image, "png", path.toFile());
    }

    private static int plotWidth() {
        return WIDTH - LEFT - RIGHT;
    }

    private static int plotHeight() {
        return HEIGHT - TOP - BOTTOM;
    }

    private static int mapX(double value, double xMin, double xMax) {
        double ratio = (value - xMin) / (xMax - xMin);
        return (int) Math.round(LEFT + ratio * plotWidth());
    }

    private static int mapY(double value, double yMin, double yMax) {
        double ratio = (value - yMin) / (yMax - yMin);
        return (int) Math.round(HEIGHT - BOTTOM - ratio * plotHeight());
    }

    private static String format(double value, int decimals) {
        return String.format(Locale.US, "%." + decimals + "f", value);
    }
}
