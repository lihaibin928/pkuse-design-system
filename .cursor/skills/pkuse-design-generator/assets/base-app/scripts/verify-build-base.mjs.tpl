import { readFile } from "node:fs/promises";

const html = await readFile(new URL("../dist/index.html", import.meta.url), "utf8");
const requireAbsolute = process.argv.includes("--require-absolute");
const configuredBase = process.env.VITE_PUBLIC_BASE?.trim();
const expectedBase = configuredBase
  ? configuredBase.endsWith("/")
    ? configuredBase
    : `${configuredBase}/`
  : undefined;
const assetUrls = [
  ...Array.from(
    html.matchAll(/(?:src|href)="([^"]+\.(?:js|css))"/g),
    (match) => match[1],
  ),
  ...Array.from(
    html.matchAll(/import\(['"]([^'"]+\.js)['"]\)/g),
    (match) => match[1],
  ),
];

if (assetUrls.length === 0) {
  throw new Error("No JavaScript or CSS assets found in dist/index.html");
}

for (const url of assetUrls) {
  if (
    requireAbsolute &&
    !url.startsWith("https://") &&
    !url.startsWith("http://")
  ) {
    throw new Error(
      `qiankun build requires an absolute asset URL, received "${url}"`,
    );
  }
  if (requireAbsolute && expectedBase && !url.startsWith(expectedBase)) {
    throw new Error(
      `qiankun asset URL "${url}" does not use VITE_PUBLIC_BASE "${expectedBase}"`,
    );
  }
  if (url.startsWith("/")) {
    throw new Error(
      `Root-absolute asset URL "${url}" would resolve against the host origin`,
    );
  }
  if (
    !url.startsWith("./") &&
    !url.startsWith("https://") &&
    !url.startsWith("http://")
  ) {
    throw new Error(`Unexpected asset URL "${url}"`);
  }
}

console.log(`Verified ${assetUrls.length} deploy-safe asset URL(s)`);
