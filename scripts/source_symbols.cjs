/** Inventory TypeScript source symbols using the same compiler as the frontend build. */
const ts = require("../frontend/node_modules/typescript");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const purposes = JSON.parse(
  fs.readFileSync(path.join(__dirname, "frontend_purposes.json"), "utf8"),
);
if (process.argv.includes("--annotate"))
  for (const f of fs
    .readdirSync(path.join(root, "frontend/src"))
    .filter((f) => /\.tsx?$/.test(f) && !f.includes(".test."))) {
    const p = path.join(root, "frontend/src", f);
    let code = fs.readFileSync(p, "utf8");
    let ast = ts.createSourceFile(f, code, ts.ScriptTarget.Latest, true);
    let edits = [];
    function visit(n) {
      if (
        (ts.isFunctionDeclaration(n) ||
          ts.isClassDeclaration(n) ||
          ts.isInterfaceDeclaration(n)) &&
        n.name &&
        purposes[n.name.text] &&
        !n.jsDoc?.length
      )
        edits.push([
          n.getStart(ast),
          "/** " +
            purposes[n.name.text] +
            " */\n" +
            " ".repeat(
              ast.getLineAndCharacterOfPosition(n.getStart(ast)).character,
            ),
        ]);
      ts.forEachChild(n, visit);
    }
    visit(ast);
    for (const [pos, text] of edits.sort((a, b) => b[0] - a[0]))
      code = code.slice(0, pos) + text + code.slice(pos);
    fs.writeFileSync(p, code);
  }
let result = [];
for (const base of ["frontend/src", "transcription"])
  for (const f of fs
    .readdirSync(path.join(root, base))
    .filter((f) => /\.(tsx?|mjs)$/.test(f) && !f.includes(".test."))) {
    const relative = base + "/" + f;
    const code = fs.readFileSync(path.join(root, relative), "utf8");
    const ast = ts.createSourceFile(
      f,
      code,
      ts.ScriptTarget.Latest,
      true,
      f.endsWith("mjs") ? ts.ScriptKind.JS : undefined,
    );
    let symbols = [];
    function line(n) {
      return ast.getLineAndCharacterOfPosition(n.getStart(ast)).line + 1;
    }
    function scope(n) {
      let names = [];
      for (let p = n.parent; p; p = p.parent)
        if (
          (ts.isFunctionDeclaration(p) ||
            ts.isClassDeclaration(p) ||
            ts.isInterfaceDeclaration(p)) &&
          p.name
        )
          names.unshift(p.name.text);
      return names.join(".") || "module";
    }
    function visit(n) {
      let names = [];
      let name;
      if (
        (ts.isFunctionDeclaration(n) ||
          ts.isClassDeclaration(n) ||
          ts.isInterfaceDeclaration(n) ||
          ts.isTypeAliasDeclaration(n)) &&
        n.name
      )
        name = n.name.text;
      else if (
        ts.isVariableDeclaration(n) ||
        ts.isParameter(n) ||
        ts.isPropertySignature(n)
      )
        name = n.name.getText(ast);
      if (
        (ts.isVariableDeclaration(n) || ts.isParameter(n)) &&
        !ts.isIdentifier(n.name)
      ) {
        function binding(b) {
          if (ts.isIdentifier(b)) names.push(b.text);
          else if (b.elements)
            for (const e of b.elements) if (e.name) binding(e.name);
        }
        binding(n.name);
        name = undefined;
      }
      if (
        ts.isArrowFunction(n) ||
        ts.isFunctionExpression(n) ||
        ts.isMethodDeclaration(n) ||
        ts.isConstructorDeclaration(n)
      )
        name = n.name?.getText(ast) || "callback@" + line(n);
      if (name) names.push(name);
      for (const name of names)
        symbols.push({
          name,
          scope: scope(n),
          line: line(n),
          kind: ts.SyntaxKind[n.kind],
          signature: (ts.isFunctionDeclaration(n)
            ? n.parameters.map((p) => p.getText(ast)).join(", ")
            : n.type?.getText(ast) || n.initializer?.getText(ast) || ""
          )
            .replace(/\s+/g, " ")
            .slice(0, 180),
          purpose: purposes[name] || "",
        });
      ts.forEachChild(n, visit);
    }
    visit(ast);
    result.push({ file: relative, symbols });
  }
process.stdout.write(JSON.stringify(result));
