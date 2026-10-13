// Saves one finished quiz (or a results-page feedback note) to Netlify Blobs.
// The app POSTs the JSON body here (see app/src/app.js submit()).
import { getStore } from "@netlify/blobs";

const MAX_BODY = 400_000;

export default async (req) => {
  if (req.method !== "POST") return new Response("Send responses with POST.", { status: 405 });
  const body = await req.text();
  if (!body || body.length > MAX_BODY) return new Response("Empty or too large.", { status: 413 });
  let data;
  try {
    data = JSON.parse(body);
  } catch {
    return new Response("Not JSON.", { status: 400 });
  }
  if (typeof data.rid !== "string" || !/^[A-Z0-9]{6,32}$/.test(data.rid)) {
    return new Response("Missing response id.", { status: 400 });
  }
  const day = new Date().toISOString().slice(0, 10);
  const key = data.feedback
    ? `feedback/${day}/${data.rid}-${Date.now()}`
    : `responses/${day}/${data.rid}`;
  await getStore("quiz").set(key, body);
  return Response.json({ ok: true });
};

export const config = { path: "/api/submit" };
