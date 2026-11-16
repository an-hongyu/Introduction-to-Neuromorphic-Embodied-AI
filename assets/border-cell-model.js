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
  // Nearest-boundary mode pools the complete enclosing border. It is not the
  // receptive field of a biologically identified single-wall-selective cell.
  function trueNearestBoundaryDistance(shape, x, y) {
    if (!inside(x, y, shape)) return NaN;
    return shape === 'circle' ? R - Math.hypot(x, y)
      : Math.min(R - y, R + y, R - x, R + x);
  }
  function estimateNearestBoundaryDistance(shape, x, y, hits) {
    if (!inside(x, y, shape) || !Array.isArray(hits)) return NaN;
    const valid = hits.filter(h => h.valid && Number.isFinite(h.wx) && Number.isFinite(h.wy));
    if (shape === 'square') {
      // Reconstruct each of the four enclosing wall coordinates from world-frame
      // LiDAR hits, then take their minimum distance. No direct trueWallDistance().
      if (valid.length < 4) return NaN;
      const distances = ['north', 'east', 'south', 'west'].map(w =>
        estimateWallDistance(shape, w, x, y, valid));
      return distances.every(Number.isFinite) ? Math.min(...distances) : NaN;
    }
    // Infer the enclosing circular radius from valid LiDAR hit endpoints.
    // For noiseless, full-visibility rays, each world-frame hit has norm R.
    // The median radius is less vulnerable than one return to a bad hit.
    if (valid.length < 3) return NaN;
    const radii = valid.map(h => Math.hypot(h.wx, h.wy)).sort((a, b) => a - b);
    const mid = Math.floor(radii.length / 2);
    const radiusEstimate = radii.length % 2 ? radii[mid] : .5 * (radii[mid - 1] + radii[mid]);
    return clamp(radiusEstimate - Math.hypot(x, y), 0, MAX_RANGE);
  }
  function estimateBoundaryDistance(shape, mode, wall, x, y, hits) {
    if (mode === 'all') return estimateNearestBoundaryDistance(shape, x, y, hits);
    if (mode === 'single') return estimateWallDistance(shape, wall, x, y, hits);
    throw Error('Invalid boundary mode');
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
  function stepLIF(neuron, currentA, duration = 0.16, timestep = 0.001, onSample = null) {
    if (!Number.isFinite(duration) || !Number.isFinite(timestep) || duration <= 0 || timestep <= 0) throw Error('Invalid LIF timing');
    const n = Math.round(duration / timestep);
    if (!Number.isFinite(currentA) || currentA < 0) throw Error('Invalid LIF current');
    const alpha = Math.exp(-timestep / TAU);
    let spikes = 0;
    for (let i = 0; i < n; i++) {
      if (neuron.refractory > 0) {
        neuron.refractory = Math.max(0, neuron.refractory - timestep);
        neuron.voltage = RESET;
        if (onSample) onSample(neuron.voltage, false, (i + 1) * timestep);
        continue;
      }
      neuron.voltage = EL + (neuron.voltage - EL) * alpha + (currentA / G_LEAK) * (1 - alpha);
      const fired = neuron.voltage >= THRESHOLD;
      if (fired) {
        spikes++;
        neuron.spikes++;
        neuron.voltage = RESET;
        neuron.refractory = REFRACTORY;
      }
      if (onSample) onSample(neuron.voltage, fired, (i + 1) * timestep);
    }
    return spikes;
  }
  function probe(shape, wall, mode = 'single') {
    // Choose a position near the selected cardinal wall/arc.
    const q = R - 0.38;
    const center = WALL_ANGLES[wall];
    const px = q * Math.cos(center), py = q * Math.sin(center);
    const headingA = center, headingB = center + Math.PI;
    const before = scan(shape, px, py, headingA);
    const after = scan(shape, px, py, headingB);
    const forwardA = before[18], forwardB = after[18];
    const worldA = estimateBoundaryDistance(shape, mode, wall, px, py, before);
    const worldB = estimateBoundaryDistance(shape, mode, wall, px, py, after);
    return {x: px, y: py, bodyBefore: forwardA.range, bodyAfter: forwardB.range,
      worldBefore: worldA, worldAfter: worldB,
      rateBefore: lifRate(wallCurrent(worldA)), rateAfter: lifRate(wallCurrent(worldB))};
  }

  // Seeded stochastic goal exploration for square and circular teaching arenas.
  // Geometry and synthetic LiDAR provide the collision guard; spike rates do NOT steer the robot.
  function createExplorer(shape, seed = 23) {
    if (shape !== 'square' && shape !== 'circle') throw Error('Unknown arena');
    if (!Number.isSafeInteger(seed) || seed < 1 || seed > 999999) throw Error('Seed must be an integer from 1 to 999999');
    let randomState = seed >>> 0;
    const random = () => { randomState = (Math.imul(1664525, randomState) + 1013904223) >>> 0; return randomState / 4294967296; };
    return {shape, seed, x: 0, y: 0, heading: 2 * Math.PI * random() - Math.PI,
      random, goal: null, age: 0, turnNoise: 0, steps: 0};
  }
  function chooseRandomGoal(e) {
    for (let k = 0; k < 100; k++) {
      let x, y;
      if (e.random() < 0.48) {
        if (e.shape === 'circle') {
          const theta = 2 * Math.PI * e.random(), radius = 1.48 + 0.28 * e.random();
          x = radius * Math.cos(theta); y = radius * Math.sin(theta);
        } else {
          const edge = Math.floor(4 * e.random()), side = (e.random() < .5 ? -1 : 1) * (1.46 + .30 * e.random());
          const across = (2 * e.random() - 1) * 1.76;
          x = edge % 2 ? across : side; y = edge % 2 ? side : across;
        }
      } else {
        x = (2 * e.random() - 1) * 1.76;
        y = (2 * e.random() - 1) * 1.76;
      }
      if (inside(x, y, e.shape, 0.20) && Math.hypot(x - e.x, y - e.y) > .65) {
        e.goal = [x, y]; e.age = 0; return;
      }
    }
    e.goal = [0, 0]; e.age = 0;
  }
  function exploreStep(e, stride = 0.107) {
    if (!(stride > 0 && stride <= .107) || !Number.isFinite(stride)) throw Error('Invalid step length');
    const distanceToGoal = e.goal ? Math.hypot(e.goal[0] - e.x, e.goal[1] - e.y) : 0;
    if (!e.goal || distanceToGoal < .17 || e.age > 64) chooseRandomGoal(e);
    const desired = Math.atan2(e.goal[1] - e.y, e.goal[0] - e.x);
    e.turnNoise = clamp(.85 * e.turnNoise + (e.random() - .5) * .14, -.16, .16);
    let heading = wrap(e.heading + clamp(.72 * wrap(desired - e.heading) + e.turnNoise, -.24, .24));
    // Clearance is a simplified geometric point-robot guard, not measured chassis size.
    if (rayDistance(e.shape, e.x, e.y, heading) < .34) {
      const inward = Math.atan2(-e.y, -e.x);
      heading = wrap(e.heading + clamp(wrap(inward - e.heading), -.45, .45));
      e.goal = null;
    }
    let nextX = e.x + stride * Math.cos(heading);
    let nextY = e.y + stride * Math.sin(heading);
    if (!inside(nextX, nextY, e.shape, .15)) {
      heading = Math.atan2(-e.y, -e.x);
      nextX = e.x + stride * Math.cos(heading);
      nextY = e.y + stride * Math.sin(heading);
      e.goal = null;
      if (!inside(nextX, nextY, e.shape, .15)) throw Error('No safe explorer step');
    }
    e.x = nextX; e.y = nextY; e.heading = heading; e.age++; e.steps++;
    return {x:e.x, y:e.y, heading:e.heading};
  }

  // Historical raster/circle waypoint generator; retained only for legacy numerical examples.
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
    estimateWallDistance, estimateNearestBoundaryDistance, trueNearestBoundaryDistance,
    estimateBoundaryDistance, sensorCurrent, wallCurrent, lifRate, newLIF, stepLIF,
    probe, waypoints, createExplorer, exploreStep, wrap, clamp, WALL_ANGLES};
});
