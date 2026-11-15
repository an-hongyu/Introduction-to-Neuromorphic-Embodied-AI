/* Shared deterministic geometric and LIF model for the interactive textbook.
 * This is a constructed sensory representation, NOT biological border-cell learning.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) root.BorderCellModel = api;
})(typeof window !== 'undefined' ? window : null, function () {
  'use strict';
  const R = 2.0;
  const SECTORS = 36;
  const TAU = 0.020;
  const EL = -0.065;
  const THRESHOLD = -0.050;
  const RESET = -0.065;
  const G_LEAK = 10e-9;
  const REFRACTORY = 0.002;
  const MAX_RANGE = 5;
  const WALL_ANGLES = {north: Math.PI / 2, east: 0, south: -Math.PI / 2, west: Math.PI};
  const EPS = 1e-10;

  function clamp(x, a, b) { return Math.max(a, Math.min(b, x)); }
  function wrap(a) { return Math.atan2(Math.sin(a), Math.cos(a)); }
  function inside(x, y, shape, margin = 0) {
    return shape === 'circle' ? Math.hypot(x, y) <= R - margin + EPS
      : Math.max(Math.abs(x), Math.abs(y)) <= R - margin + EPS;
  }
  function rayDistance(shape, x, y, angle) {
    if (!inside(x, y, shape)) return NaN;
    const dx = Math.cos(angle), dy = Math.sin(angle);
    if (shape === 'circle') {
      const b = x * dx + y * dy;
      const discriminant = b * b + R * R - x * x - y * y;
      return discriminant < 0 ? NaN : -b + Math.sqrt(discriminant);
    }
    const hits = [];
    if (Math.abs(dx) > 1e-12) {
      for (const wall of [-R, R]) {
        const t = (wall - x) / dx;
        if (t > EPS && Math.abs(y + t * dy) <= R + EPS) hits.push(t);
      }
    }
    if (Math.abs(dy) > 1e-12) {
      for (const wall of [-R, R]) {
        const t = (wall - y) / dy;
        if (t > EPS && Math.abs(x + t * dx) <= R + EPS) hits.push(t);
      }
    }
    return hits.length ? Math.min.apply(null, hits) : NaN;
  }
  function scan(shape, x, y, heading, invalidSectors) {
    const returns = [];
    for (let k = 0; k < SECTORS; k++) {
      // Centered body-relative sectors: 0 degrees forward is sector 18.
      const bodyAngle = (k - 18) * Math.PI / 18;
      const angle = heading + bodyAngle;
      const range = rayDistance(shape, x, y, angle);
      const valid = Number.isFinite(range) && range >= 0.05 && range <= MAX_RANGE &&
        !(invalidSectors && invalidSectors.has(k));
      returns.push({sector: k, bodyAngle, angle, range: valid ? range : NaN, valid,
        wx: valid ? x + range * Math.cos(angle) : NaN,
        wy: valid ? y + range * Math.sin(angle) : NaN});
    }
    return returns;
  }
  function trueWallDistance(shape, wall, x, y) {
    if (shape === 'square') {
      return ({north: R - y, east: R - x, south: R + y, west: R + x})[wall];
    }
    const center = WALL_ANGLES[wall];
    const phi = Math.atan2(y, x);
    const delta = wrap(phi - center);
    if (Math.abs(delta) <= Math.PI / 4) return R - Math.hypot(x, y);
    const end = center + Math.sign(delta) * Math.PI / 4;
    return Math.hypot(x - R * Math.cos(end), y - R * Math.sin(end));
  }
  // Use transformed LiDAR endpoints, not the ground-truth wall distance, to
  // estimate proximity. This idealized demo knows which wall/arc is selected.
  function estimateWallDistance(shape, wall, x, y, hits) {
    const points = hits.filter(h => h.valid);
    if (shape === 'square') {
      if (points.length < 2) return NaN;
      // Cardinal normal of the selected world-fixed wall.
      const axis = wall === 'north' || wall === 'south' ? 'wy' : 'wx';
      const sign = wall === 'north' || wall === 'east' ? 1 : -1;
      const coordinates = points.map(h => sign * h[axis]);
      const extreme = Math.max.apply(null, coordinates);
      return clamp(extreme - sign * (axis === 'wy' ? y : x), 0, MAX_RANGE);
    }
    const center = WALL_ANGLES[wall];
    const selected = points.filter(h => Math.abs(wrap(Math.atan2(h.wy, h.wx) - center)) <= Math.PI / 4 + 1e-7);
    if (selected.length < 1) return NaN;
    return Math.min.apply(null, selected.map(h => Math.hypot(h.wx - x, h.wy - y)));
  }
  function sensorCurrent(range, valid = true) {
    return valid && Number.isFinite(range) && range >= 0 && range <= MAX_RANGE ?
      (100 + 180 * (1 - range / MAX_RANGE)) * 1e-12 : 0;
  }
  function wallCurrent(distance, sigma = 0.55) {
    return Number.isFinite(distance) && distance >= 0 ?
      (100 + 180 * Math.exp(-0.5 * (distance / sigma) ** 2)) * 1e-12 : 0;
  }
  function lifRate(currentA) {
    if (!Number.isFinite(currentA) || currentA <= G_LEAK * (THRESHOLD - EL)) return 0;
    const infinityV = EL + currentA / G_LEAK;
    return 1 / (REFRACTORY + TAU * Math.log((infinityV - RESET) / (infinityV - THRESHOLD)));
  }
  function newLIF() { return {voltage: EL, refractory: 0, spikes: 0}; }
  function stepLIF(neuron, currentA, duration = 0.16, timestep = 0.001) {
    if (!Number.isFinite(duration) || !Number.isFinite(timestep) || duration <= 0 || timestep <= 0) throw Error('Invalid LIF timing');
    const n = Math.round(duration / timestep);
    if (!Number.isFinite(currentA) || currentA < 0) throw Error('Invalid LIF current');
    const alpha = Math.exp(-timestep / TAU);
    let spikes = 0;
    for (let i = 0; i < n; i++) {
      if (neuron.refractory > 0) {
        neuron.refractory = Math.max(0, neuron.refractory - timestep);
        neuron.voltage = RESET;
        continue;
      }
      neuron.voltage = EL + (neuron.voltage - EL) * alpha + (currentA / G_LEAK) * (1 - alpha);
      if (neuron.voltage >= THRESHOLD) {
        spikes++;
        neuron.spikes++;
        neuron.voltage = RESET;
        neuron.refractory = REFRACTORY;
      }
    }
    return spikes;
  }
  function probe(shape, wall, x = 0, y = 1.6) {
    // Choose a position near the selected cardinal wall/arc.
    const q = R - 0.38;
    const center = WALL_ANGLES[wall];
    const px = q * Math.cos(center), py = q * Math.sin(center);
    const headingA = center, headingB = center + Math.PI;
    const before = scan(shape, px, py, headingA);
    const after = scan(shape, px, py, headingB);
    const forwardA = before[18], forwardB = after[18];
    const worldA = estimateWallDistance(shape, wall, px, py, before);
    const worldB = estimateWallDistance(shape, wall, px, py, after);
    return {x: px, y: py, bodyBefore: forwardA.range, bodyAfter: forwardB.range,
      worldBefore: worldA, worldAfter: worldB,
      rateBefore: lifRate(wallCurrent(worldA)), rateAfter: lifRate(wallCurrent(worldB))};
  }
  function waypoints(shape) {
    const p = [];
    if (shape === 'square') {
      for (let lap = 0; lap < 2; lap++) {
        const ys = [1.72, 1.34, 0.95, 0.56, 0.18, -0.20, -0.58, -0.96, -1.35, -1.72];
        for (let i = 0; i < ys.length; i++) {
          p.push([i % 2 ? 1.72 : -1.72, ys[i]]);
          p.push([i % 2 ? -1.72 : 1.72, ys[i]]);
        }
      }
    } else {
      // Several radii provide interior as well as near-boundary coverage.
      for (const radius of [1.72, 1.35, 0.95, 0.55, 1.72, 1.35]) {
        const N = 32;
        for (let i = 0; i <= N; i++) {
          const a = Math.PI / 2 + i * 2 * Math.PI / N;
          p.push([radius * Math.cos(a), radius * Math.sin(a)]);
        }
      }
    }
    return p;
  }
  return {R, SECTORS, EL, THRESHOLD, scan, inside, rayDistance, trueWallDistance,
    estimateWallDistance, sensorCurrent, wallCurrent, lifRate, newLIF, stepLIF,
    probe, waypoints, wrap, clamp, WALL_ANGLES};
});
