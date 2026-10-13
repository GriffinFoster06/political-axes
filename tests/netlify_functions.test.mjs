// Tests the Netlify functions with an in-memory stand-in for Netlify Blobs.
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const MOCK = `const __mem = globalThis.__mem || (globalThis.__mem = new Map());
const getStore = () => ({ set: async (k, v) => __mem.set(k, v), get: async (k) => __mem.get(k),
  list: async ({ prefix }) => ({ blobs: [...__mem.keys()].filter(k => k.startsWith(prefix)).map(key => ({ key })) }) });`;
const dir = mkdtempSync(join(tmpdir(), "fn-"));
for (const f of ["submit.mjs", "export.mjs"]) {
  const src = readFileSync(new URL(`../netlify/functions/${f}`, import.meta.url), "utf8");
  writeFileSync(join(dir, f), src.replace('import { getStore } from "@netlify/blobs";', MOCK));
}
globalThis.Netlify = { env: { get: (k) => (k === "EXPORT_KEY" ? "k" : undefined) } };
const submit = (await import(join(dir, "submit.mjs"))).default;
const exp = (await import(join(dir, "export.mjs"))).default;
const post = (b) => submit(new Request("https://x/api/submit", { method: "POST", body: b }));

test("stores responses and feedback separately, rejects bad input", async () => {
  assert.equal((await post(JSON.stringify({ rid: "ABCDEFGH1234", ans: { a: { c: 1 } } }))).status, 200);
  assert.equal((await post(JSON.stringify({ rid: "ABCDEFGH1234", feedback: true }))).status, 200);
  assert.equal((await post("nope")).status, 400);
  assert.equal((await post(JSON.stringify({ rid: "bad id!" }))).status, 400);
  assert.equal((await submit(new Request("https://x/api/submit"))).status, 405);
});

test("export needs the key and returns JSON lines", async () => {
  assert.equal((await exp(new Request("https://x/api/export?key=wrong"))).status, 403);
  const lines = (await (await exp(new Request("https://x/api/export?key=k"))).text()).trim().split("\n");
  assert.equal(lines.length, 1);
  assert.equal(JSON.parse(lines[0]).rid, "ABCDEFGH1234");
  const fb = (await (await exp(new Request("https://x/api/export?key=k&what=feedback"))).text()).trim();
  assert.ok(JSON.parse(fb).feedback);
});
