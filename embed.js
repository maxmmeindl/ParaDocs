// embed.js
import "dotenv/config.js";
import fs from "fs";
import path from "path";
import pdfParse from "pdf-parse";
import mammoth from "mammoth";

// LangChain imports (v0.0.4)
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter.js";
import { OpenAIEmbeddings }            from "langchain/embeddings/openai.js";
import { HNSWLib }                     from "langchain/vectorstores/hnswlib.js";

async function loadFile(filePath) {
  if (filePath.endsWith(".md")) {
    // Markdown files: read raw text
    return fs.readFileSync(filePath, "utf8");
  } else if (filePath.endsWith(".pdf")) {
    // PDFs: parse with pdf-parse
    const buffer = fs.readFileSync(filePath);
    const { text } = await pdfParse(buffer);
    return text;
  } else if (filePath.endsWith(".docx")) {
    // DOCXs: parse with mammoth
    const buffer = fs.readFileSync(filePath);
    const { value } = await mammoth.extractRawText({ buffer });
    return value;
  }
  // skip unsupported types
  return null;
}

async function main() {
  const dir = "downloaded";
  if (!fs.existsSync(dir)) {
    console.error(`❌ Folder "${dir}/" not found – run ingest.js first.`);
    process.exit(1);
  }

  // 1) Load & parse each file
  const docs = [];
  for (const fname of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, fname);
    const content = await loadFile(fullPath);
    if (!content) continue;
    docs.push({ pageContent: content, metadata: { source: fname } });
    console.log("Loaded", fname);
  }

  if (docs.length === 0) {
    console.error("❌ No supported files found in downloaded/.");
    return;
  }

  // 2) Split into chunks
  const splitter = new RecursiveCharacterTextSplitter({
    chunkSize: 1000,
    chunkOverlap: 200,
  });
  const splitDocs = await splitter.splitDocuments(docs);

  // 3) Embed & build the vector store
  const vectorStore = await HNSWLib.fromDocuments(
    splitDocs,
    new OpenAIEmbeddings()
  );

  // 4) Persist it for querying
  await vectorStore.save("paradocs_store");
  console.log("✅ Embedding complete, store saved.");
}

main();
