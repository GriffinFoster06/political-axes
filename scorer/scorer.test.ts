// Run: node --test scorer/   (Node 22.18+ runs TypeScript directly)
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { scoreEAP, mulberry32, percentile, catProbs, type ModelParams } from "./scorer.ts";

const here = new URL(".", import.meta.url);
const model: ModelParams = JSON.parse(readFileSync(new URL("../model/params.json", here), "utf8"));
const fixtures = JSON.parse(readFileSync(new URL("./fixtures.json", here), "utf8"));
const anesModel: ModelParams = JSON.parse(readFileSync(new URL("../model/params_anes.json", here), "utf8"));
const anesFixtures = JSON.parse(readFileSync(new URL("./fixtures_anes.json", here), "utf8"));

test("mulberry32 matches the Python stream", () => {
  const r = mulberry32(20261012);
  const first = [r(), r(), r()];
  // Values printed by pipeline/grm.py Mulberry32(20261012)
  const expected = JSON.parse(readFileSync(new URL("./prng_reference.json", here), "utf8"));
  first.forEach((v, i) => assert.ok(Math.abs(v - expected[i]) < 1e-15, `draw ${i}: ${v} vs ${expected[i]}`));
});

test("category probabilities sum to 1", () => {
  for (const it of model.items) {
    for (const th of [-4, -1, 0, 0.7, 3]) {
      const s = catProbs(it, th).reduce((a, b) => a + b, 0);
      assert.ok(Math.abs(s - 1) < 1e-9, `${it.id} at ${th}: ${s}`);
    }
  }
});

for (const [label, m, fx] of [["GSS", model, fixtures], ["ANES bifactor", anesModel, anesFixtures]] as const) {
for (const c of fx) {
  test(`${label} matches Python reference: ${c.name}`, () => {
    const out = scoreEAP(c.responses, m);
    for (let i = 0; i < out.mean.length; i++) {
      assert.ok(Math.abs(out.mean[i] - c.expected.mean[i]) < 1e-6, `mean[${i}] ${out.mean[i]} vs ${c.expected.mean[i]}`);
      assert.ok(Math.abs(out.sd[i] - c.expected.sd[i]) < 1e-6, `sd[${i}] ${out.sd[i]} vs ${c.expected.sd[i]}`);
    }
    assert.ok(Math.abs(out.ess - c.expected.ess) / c.expected.ess < 1e-6);
  });
}
}

test("no answers returns the prior (mean 0, sd about 1)", () => {
  const out = scoreEAP({}, model);
  out.mean.forEach((m) => assert.ok(Math.abs(m) < 0.05));
  out.sd.forEach((s) => assert.ok(Math.abs(s - 1) < 0.08));
});

test("rejects out-of-range answers", () => {
  const it = model.items[0];
  assert.throws(() => scoreEAP({ [it.id]: it.ncat }, model));
});

test("percentiles are monotone", () => {
  const d = model.dimensions[0].id;
  let prev = 0;
  for (const s of [-3, -1, 0, 1, 3]) {
    const p = percentile(model, d, s);
    assert.ok(p >= prev);
    prev = p;
  }
});
