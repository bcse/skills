#!/usr/bin/env node
// Renders every ```mermaid block of a Markdown file in headless Chromium and saves one PNG per diagram.
// Usage: node render_mermaid.mjs <file.md> [out-dir]
// Run it from a repository that has @playwright/test installed. It loads mermaid@11 from cdn.jsdelivr.net, so it needs
// network access. GitHub pins its own Mermaid version, so a diagram that renders here can still differ there.
// Exit codes: 0 all diagrams rendered, 1 a diagram has a syntax error, 2 setup problem.
import { mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const [file, outArg] = process.argv.slice(2);
if (!file) {
  console.error("usage: node render_mermaid.mjs <file.md> [out-dir]");
  process.exit(2);
}

const blocks = [...readFileSync(file, "utf8").matchAll(/```mermaid\n([\s\S]*?)```/g)].map((m) => m[1]);
if (blocks.length === 0) {
  console.log("0 mermaid blocks");
  process.exit(0);
}

let chromium;
try {
  ({ chromium } = createRequire(join(process.cwd(), "noop.js"))("@playwright/test"));
} catch {
  console.error(`Cannot load @playwright/test from ${process.cwd()}. Run this from a repository that installs it.`);
  process.exit(2);
}

const out = resolve(outArg ?? join(tmpdir(), `mermaid-${Date.now()}`));
mkdirSync(out, { recursive: true });

const html = `<!doctype html><meta charset="utf-8"><body style="background:#fff;padding:16px;width:1100px"><div id="out"></div>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: false });
  const blocks = ${JSON.stringify(blocks).replace(/</g, "\\u003c")};
  window.__results = [];
  // One render per block: a syntax error in one diagram is reported and the others still render.
  for (const [i, text] of blocks.entries()) {
    const holder = document.createElement("div");
    holder.className = "diagram";
    document.getElementById("out").append(holder);
    try {
      holder.innerHTML = (await mermaid.render("diagram-" + i, text)).svg;
      window.__results.push({ ok: true });
    } catch (error) {
      const reason = String(error.message ?? error).split("\\n")[0];
      holder.textContent = "SYNTAX ERROR: " + reason;
      window.__results.push({ ok: false, reason });
    }
  }
  document.body.dataset.done = "1";
</script>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1150, height: 900 } });
const pageErrors = [];
page.on("pageerror", (error) => pageErrors.push(String(error)));
await page.setContent(html);
try {
  await page.waitForSelector('body[data-done="1"]', { timeout: 30_000 });
} catch {
  console.error("Mermaid did not finish in 30 seconds. Check the network access to cdn.jsdelivr.net, and the page errors:");
  console.error(pageErrors.join("\n") || "(none)");
  await browser.close();
  process.exit(2);
}

const results = await page.evaluate(() => window.__results);
const failed = [];
for (const [i, result] of results.entries()) {
  if (!result.ok) {
    failed.push(i + 1);
    console.error(`diagram ${i + 1}: ${result.reason}`);
  }
  await page.locator(".diagram").nth(i).screenshot({ path: join(out, `diagram-${i + 1}.png`) });
}
await browser.close();

console.log(`diagrams=${blocks.length} syntax-errors=${failed.length}${failed.length ? ` (diagram ${failed.join(", ")})` : ""} page-errors=${pageErrors.length}`);
console.log(`PNGs in ${out}: read each one to check order, labels, and layout.`);
process.exit(failed.length || pageErrors.length ? 1 : 0);
