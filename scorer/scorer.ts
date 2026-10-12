/**
 * Browser/Node scorer for the political-axes multidimensional graded response model.
 *
 * Mirrors pipeline/grm.py `score_eap` exactly:
 *  1. Newton's method for the posterior mode under the correlated MVN prior.
 *  2. Laplace approximation (inverse negative Hessian) as the proposal.
 *  3. Importance sampling with a fixed mulberry32 + Box-Muller stream, so the
 *     same answers always give the same scores, in Python and in the browser.
 * Output: posterior mean (EAP), posterior SD and covariance per dimension.
 */

export interface ItemParams {
  id: string;
  dim: string;
  a: number;
  d: number[]; // decreasing intercepts, length ncat - 1
  ncat: number;
}

export interface ModelParams {
  version: string;
  dimensions: { id: string; label: string }[];
  sigma: number[][];
  items: ItemParams[];
  scoring: { seed: number; draws: number; inflate: number };
  norms_percentiles_1_to_99?: Record<string, number[]>;
}

export interface ScoreResult {
  mean: number[];
  sd: number[];
  cov: number[][];
  map: number[];
  ess: number;
  nItems: number;
}

export type Responses = Record<string, number | null | undefined>;

// ---------------------------------------------------------------- PRNG
export function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1) >>> 0;
    t = (t ^ ((t + (Math.imul(t ^ (t >>> 7), t | 61) >>> 0)) >>> 0)) >>> 0;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function stdNormals(n: number, D: number, seed: number): Float64Array {
  const rng = mulberry32(seed);
  const out = new Float64Array(n * D);
  for (let i = 0; i < n * D; i += 2) {
    const u1 = Math.max(rng(), 1e-12);
    const u2 = rng();
    const r = Math.sqrt(-2 * Math.log(u1));
    out[i] = r * Math.cos(2 * Math.PI * u2);
    if (i + 1 < n * D) out[i + 1] = r * Math.sin(2 * Math.PI * u2);
  }
  return out;
}

// --------------------------------------------------------- linear algebra
function cholesky(A: number[][]): number[][] {
  const n = A.length;
  const L = A.map(() => new Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    for (let j = 0; j <= i; j++) {
      let s = A[i][j];
      for (let k = 0; k < j; k++) s -= L[i][k] * L[j][k];
      if (i === j) {
        if (s <= 0) throw new Error("matrix not positive definite");
        L[i][j] = Math.sqrt(s);
      } else {
        L[i][j] = s / L[j][j];
      }
    }
  }
  return L;
}

function invertSPD(A: number[][]): number[][] {
  const n = A.length;
  const L = cholesky(A);
  const Linv = A.map(() => new Array(n).fill(0));
  for (let i = 0; i < n; i++) {
    Linv[i][i] = 1 / L[i][i];
    for (let j = 0; j < i; j++) {
      let s = 0;
      for (let k = j; k < i; k++) s -= L[i][k] * Linv[k][j];
      Linv[i][j] = s / L[i][i];
    }
  }
  const inv = A.map(() => new Array(n).fill(0));
  for (let i = 0; i < n; i++)
    for (let j = 0; j <= i; j++) {
      let s = 0;
      for (let k = i; k < n; k++) s += Linv[k][i] * Linv[k][j];
      inv[i][j] = inv[j][i] = s;
    }
  return inv;
}

function solve(A: number[][], b: number[]): number[] {
  // Gaussian elimination with partial pivoting (A is small and may be indefinite)
  const n = b.length;
  const M = A.map((row, i) => [...row, b[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    [M[c], M[p]] = [M[p], M[c]];
    for (let r = c + 1; r < n; r++) {
      const f = M[r][c] / M[c][c];
      for (let k = c; k <= n; k++) M[r][k] -= f * M[c][k];
    }
  }
  const x = new Array(n).fill(0);
  for (let r = n - 1; r >= 0; r--) {
    let s = M[r][n];
    for (let k = r + 1; k < n; k++) s -= M[r][k] * x[k];
    x[r] = s / M[r][r];
  }
  return x;
}

// ----------------------------------------------------------- item model
const expit = (z: number) => 1 / (1 + Math.exp(-z));

/** P(Y = k | theta) for one item. */
export function catProb(a: number, d: number[], theta: number, k: number): number {
  const hi = k === 0 ? 1 : expit(a * theta + d[k - 1]);
  const lo = k === d.length ? 0 : expit(a * theta + d[k]);
  return Math.min(Math.max(hi - lo, 1e-12), 1);
}

/** All category probabilities for one item at theta. */
export function catProbs(item: ItemParams, theta: number): number[] {
  return Array.from({ length: item.ncat }, (_, k) => catProb(item.a, item.d, theta, k));
}

function itemLLDerivs(theta: number, a: number, d: number[], k: number): [number, number, number] {
  const star = [1, ...d.map((dk) => expit(a * theta + dk)), 0];
  const W = star.map((s) => s * (1 - s));
  const Wp = W.map((w, i) => w * (1 - 2 * star[i]));
  const P = Math.max(star[k] - star[k + 1], 1e-12);
  const dP = a * (W[k] - W[k + 1]);
  const d2P = a * a * (Wp[k] - Wp[k + 1]);
  return [Math.log(P), dP / P, d2P / P - (dP / P) ** 2];
}

// ---------------------------------------------------------------- scoring
export function scoreEAP(responses: Responses, model: ModelParams, opts: Partial<ModelParams["scoring"]> = {}): ScoreResult {
  const dims = model.dimensions.map((x) => x.id);
  const D = dims.length;
  const dimIdx = new Map(dims.map((d, i) => [d, i]));
  let nDraws = opts.draws ?? model.scoring.draws;
  const seed = opts.seed ?? model.scoring.seed;
  const inflate = opts.inflate ?? model.scoring.inflate;
  const used: [number, ItemParams, number][] = [];
  for (const it of model.items) {
    const r = responses[it.id];
    if (r === null || r === undefined) continue;
    if (!Number.isInteger(r) || r < 0 || r >= it.ncat) throw new Error(`bad response ${r} for ${it.id}`);
    used.push([dimIdx.get(it.dim)!, it, r]);
  }
  const Sinv = invertSPD(model.sigma);

  const logpost = (t: number[]) => {
    let lp = 0;
    for (let i = 0; i < D; i++) for (let j = 0; j < D; j++) lp -= 0.5 * t[i] * Sinv[i][j] * t[j];
    for (const [di, it, k] of used) lp += Math.log(catProb(it.a, it.d, t[di], k));
    return lp;
  };
  const lgh = (t: number[]): [number, number[], number[][]] => {
    let lp = 0;
    const g = new Array(D).fill(0);
    const H = Sinv.map((row) => row.map((v) => -v));
    for (let i = 0; i < D; i++) {
      for (let j = 0; j < D; j++) {
        lp -= 0.5 * t[i] * Sinv[i][j] * t[j];
        g[i] -= Sinv[i][j] * t[j];
      }
    }
    for (const [di, it, k] of used) {
      const [l, g1, h1] = itemLLDerivs(t[di], it.a, it.d, k);
      lp += l;
      g[di] += g1;
      H[di][di] += h1;
    }
    return [lp, g, H];
  };

  // Newton with backtracking (identical to the Python reference)
  let t = new Array(D).fill(0);
  for (let iter = 0; iter < 50; iter++) {
    const [lp, g, H] = lgh(t);
    const step = solve(H, g);
    let tNew = t.map((v, i) => v - step[i]);
    let lam = 1;
    while (lgh(tNew)[0] < lp - 1e-12 && lam > 1e-4) {
      lam /= 2;
      tNew = t.map((v, i) => v - lam * step[i]);
    }
    const moved = Math.max(...tNew.map((v, i) => Math.abs(v - t[i])));
    t = tNew;
    if (moved < 1e-8) break;
  }
  const H = lgh(t)[2];
  let cov = invertSPD(H.map((row) => row.map((v) => -v)));
  cov = cov.map((row, i) => row.map((v, j) => 0.5 * (v + cov[j][i])));
  const Lc = cholesky(cov.map((row) => row.map((v) => v * inflate * inflate)));
  // antithetic pairs (z, -z): removes odd-moment Monte Carlo error
  const half = Math.floor(nDraws / 2);
  const Zh = stdNormals(half, D, seed);
  const Z = new Float64Array(2 * half * D);
  Z.set(Zh);
  for (let i = 0; i < half * D; i++) Z[half * D + i] = -Zh[i];
  nDraws = 2 * half;

  const draws: number[][] = [];
  const lw = new Float64Array(nDraws);
  let mx = -Infinity;
  for (let n = 0; n < nDraws; n++) {
    const x = new Array(D);
    let zz = 0;
    for (let i = 0; i < D; i++) {
      let s = t[i];
      for (let j = 0; j <= i; j++) s += Lc[i][j] * Z[n * D + j];
      x[i] = s;
      zz += Z[n * D + i] ** 2;
    }
    draws.push(x);
    lw[n] = logpost(x) + 0.5 * zz;
    if (lw[n] > mx) mx = lw[n];
  }
  let wsum = 0;
  const w = new Float64Array(nDraws);
  for (let n = 0; n < nDraws; n++) {
    w[n] = Math.exp(lw[n] - mx);
    wsum += w[n];
  }
  let w2 = 0;
  const mean = new Array(D).fill(0);
  for (let n = 0; n < nDraws; n++) {
    w[n] /= wsum;
    w2 += w[n] * w[n];
    for (let i = 0; i < D; i++) mean[i] += w[n] * draws[n][i];
  }
  const pcov = mean.map(() => new Array(D).fill(0));
  for (let n = 0; n < nDraws; n++)
    for (let i = 0; i < D; i++)
      for (let j = 0; j < D; j++)
        pcov[i][j] += w[n] * (draws[n][i] - mean[i]) * (draws[n][j] - mean[j]);
  return {
    mean,
    sd: pcov.map((row, i) => Math.sqrt(row[i])),
    cov: pcov,
    map: t,
    ess: 1 / w2,
    nItems: used.length,
  };
}

/** National percentile (1-99) of a score, from the weighted norm table. */
export function percentile(model: ModelParams, dim: string, score: number): number {
  const q = model.norms_percentiles_1_to_99?.[dim];
  if (!q) throw new Error(`no norms for ${dim}`);
  if (score <= q[0]) return 1;
  if (score >= q[98]) return 99;
  for (let i = 1; i < 99; i++) {
    if (score <= q[i]) return i + (score - q[i - 1]) / (q[i] - q[i - 1]);
  }
  return 99;
}
