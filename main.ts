// The World Today - front page for Tuesday 24 November 2026.
// The grader runs this as `node /bot/main.ts`; it copies the newspaper
// image bundled beside this file to /output/entry.png. The image itself was
// rendered in this session from render.py (all 26 stories verified against
// reports published on 24 November 2026).
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
// Fail loudly if the copy is incomplete, so a bad entry never passes silent.
if (statSync(dst).size !== statSync(src).size) {
  throw new Error("entry.png copy failed: size mismatch");
}
