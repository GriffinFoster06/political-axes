// Downloads every saved response as JSON Lines, for scripts/pilot_responses.py.
// Protected by the EXPORT_KEY environment variable (set it in Netlify: Site configuration -> Environment variables).
//   https://YOUR-SITE.netlify.app/api/export?key=YOUR_KEY          (responses)
//   https://YOUR-SITE.netlify.app/api/export?key=YOUR_KEY&what=feedback
import { getStore } from "@netlify/blobs";

export default async (req) => {
  const url = new URL(req.url);
  const secret = Netlify.env.get("EXPORT_KEY");
  if (!secret || url.searchParams.get("key") !== secret) return new Response("Not allowed.", { status: 403 });
  const prefix = url.searchParams.get("what") === "feedback" ? "feedback/" : "responses/";
  const store = getStore("quiz");
  const { blobs } = await store.list({ prefix });
  const lines = [];
  for (const b of blobs) {
    const v = await store.get(b.key);
    if (v) lines.push(v);
  }
  return new Response(lines.join("\n") + (lines.length ? "\n" : ""), {
    headers: {
      "content-type": "application/x-ndjson; charset=utf-8",
      "content-disposition": `attachment; filename="${prefix.slice(0, -1)}.jsonl"`,
    },
  });
};

export const config = { path: "/api/export" };
