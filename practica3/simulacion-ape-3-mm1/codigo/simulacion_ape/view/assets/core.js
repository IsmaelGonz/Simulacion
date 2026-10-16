/* Lógica pura de la pantalla: reconstruye el estado del sistema a partir de los registros de SimPy.
 * Cada registro es [id, llegada, inicioAtencion, salida]; inicio y salida son null si no ocurrieron
 * dentro de la corrida. Nada aquí es aleatorio: el navegador solo reproduce lo que simuló Python. */
const Core = (() => {
  // Estado en el minuto t: quién espera (en orden FIFO), quién está en la caja y quién va saliendo.
  function stateAt(records, t, exitWindow) {
    const waiting = [];
    const leaving = [];
    let inService = null;
    let served = 0;
    let arrived = 0;
    for (const [id, arrival, start, departure] of records) {
      if (arrival > t) break;
      arrived += 1;
      if (start === null || start > t) {
        waiting.push(id);
        continue;
      }
      if (departure === null || departure > t) {
        inService = id;
        continue;
      }
      served += 1;
      if (t - departure <= exitWindow) leaving.push(id);
    }
    return { time: t, waiting, inService, leaving, arrived, served };
  }

  // Métricas simuladas con lo ocurrido hasta t: ρ, L y Lq promediados en el tiempo; W y Wq por cliente.
  function metricsAt(records, t) {
    let busy = 0;
    let systemArea = 0;
    let queueArea = 0;
    let waitSum = 0;
    let waitCount = 0;
    let systemSum = 0;
    let systemCount = 0;
    for (const [, arrival, start, departure] of records) {
      if (arrival > t) break;
      const startKnown = start !== null && start <= t;
      const departureKnown = departure !== null && departure <= t;
      systemArea += (departureKnown ? departure : t) - arrival;
      queueArea += (startKnown ? start : t) - arrival;
      if (startKnown) {
        busy += (departureKnown ? departure : t) - start;
        waitSum += start - arrival;
        waitCount += 1;
      }
      if (departureKnown) {
        systemSum += departure - arrival;
        systemCount += 1;
      }
    }
    if (t <= 0) return null;
    return {
      utilization: busy / t,
      mean_in_system: systemArea / t,
      mean_in_queue: queueArea / t,
      mean_time_in_system: systemCount ? systemSum / systemCount : NaN,
      mean_wait: waitCount ? waitSum / waitCount : NaN,
    };
  }

  // Función escalonada de clientes en el sistema y en la cola hasta `end`.
  function occupancyTrace(records, end) {
    const events = [];
    for (const [, arrival, start, departure] of records) {
      if (arrival <= end) events.push([arrival, 1, 1]);
      if (start !== null && start <= end) events.push([start, 0, -1]);
      if (departure !== null && departure <= end) events.push([departure, -1, 0]);
    }
    events.sort((a, b) => a[0] - b[0]);
    const times = [0];
    const inSystem = [0];
    const inQueue = [0];
    for (const [time, dSystem, dQueue] of events) {
      times.push(time);
      inSystem.push(inSystem[inSystem.length - 1] + dSystem);
      inQueue.push(inQueue[inQueue.length - 1] + dQueue);
    }
    return { times, inSystem, inQueue };
  }

  // Tiempos entre llegadas y de servicio observados hasta t.
  function interarrivalTimes(records, t) {
    const gaps = [];
    let previous = 0;
    for (const [, arrival] of records) {
      if (arrival > t) break;
      gaps.push(arrival - previous);
      previous = arrival;
    }
    return gaps;
  }

  function serviceTimes(records, t) {
    const durations = [];
    for (const [, arrival, start, departure] of records) {
      if (arrival > t) break;
      if (departure !== null && departure <= t) durations.push(departure - start);
    }
    return durations;
  }

  // Histograma como densidad; los valores mayores al último borde caen en la última barra.
  function histogramDensity(values, maxValue, bins) {
    const width = maxValue / bins;
    const counts = new Array(bins).fill(0);
    for (const value of values) counts[Math.min(Math.floor(value / width), bins - 1)] += 1;
    return counts.map((count) => (values.length ? count / (values.length * width) : 0));
  }

  return { stateAt, metricsAt, occupancyTrace, interarrivalTimes, serviceTimes, histogramDensity };
})();

if (typeof module !== "undefined") module.exports = Core;
