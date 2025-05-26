import "dotenv/config.js";
import fs from "fs";
import fetch from "node-fetch";

async function main() {
  // 1) Download the Pages index
  const html = await (await fetch(
    "https://maxmmeindl.github.io/ParaDocs/"
  )).text();

  // 2) Grab every “href=…(pdf|docx|md)”
  const paths = Array.from(
    html.matchAll(/href="([^"]+\.(pdf|docx|md))"/g)
  ).map(m => m[1]);

  // 3) Ensure our download folder exists
  fs.mkdirSync("downloaded", { recursive: true });

  // 4) Fetch each raw file and save it
  for (const p of paths) {
    const url = `https://raw.githubusercontent.com/maxmmeindl/ParaDocs/main/docs/${p}`;
    const data = await (await fetch(url)).arrayBuffer();
    fs.writeFileSync(`downloaded/${p}`, Buffer.from(data));
    console.log("✅ Saved", p);
  }
}

main();
