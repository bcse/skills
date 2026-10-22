#!/usr/bin/env node
// Shows an SVG as an <img> in headless Chromium, on a light page and on a dark page, and saves one PNG per page.
// Usage: node rasterize_svg.mjs <diagram.svg> [out-dir]
// Run it from a repository that has @playwright/test installed. The SVG loads as a data URI, because a page set with
// setContent cannot open file:// images. An <img> has no page styles, which is how GitHub shows an attached SVG.
// Exit codes: 0 both pages rendered, 1 the SVG did not load, 2 setup problem.
import { mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";

const [file, outArg] = process.argv.slice(2);
if (!file) {
  console.error("usage: node rasterize_svg.mjs <diagram.svg> [out-dir]");
  process.exit(2);
}

let svg;
try {
  svg = readFileSync(file);
} catch {
  console.error(`Cannot read ${file}`);
  process.exit(2);
}

let chromium;
try {
  ({ chromium } = createRequire(join(process.cwd(), "noop.js"))("@playwright/test"));
} catch {
  console.error(`Cannot load @playwright/test from ${process.cwd()}. Run this from a repository that installs it.`);
  process.exit(2);
}

const out = resolve(outArg ?? join(tmpdir(), `svg-${Date.now()}`));
mkdirSync(out, { recursive: true });
const uri = `data:image/svg+xml;base64,${svg.toString("base64")}`;
const name = basename(file, ".svg");

const browser = await chromium.launch();
let failed = false;
for (const [theme, background] of [
  ["light", "#ffffff"],
  ["dark", "#0d1117"],
]) {
  const page = await browser.newPage({ viewport: { width: 1240, height: 100 } });
  await page.setContent(
    `<body style="margin:0;padding:20px;background:${background}"><img id="i" src="${uri}" style="max-width:100%"></body>`,
  );
  await page.waitForFunction(() => document.getElementById("i").complete);
  // A broken image is also complete, so check that it has a size.
  const size = await page.evaluate(() => {
    const img = document.getElementById("i");
    return { width: img.naturalWidth, height: img.naturalHeight };
  });
  if (size.width === 0) {
    console.error(`${theme}: the SVG did not load. Check that it is well-formed XML.`);
    failed = true;
  } else {
    const path = join(out, `${name}-${theme}.png`);
    await page.screenshot({ path, fullPage: true });
    console.log(`${theme}: ${path} (image ${size.width}x${size.height})`);
  }
  await page.close();
}
await browser.close();
process.exit(failed ? 1 : 0);
