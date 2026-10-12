// Minify the theme CSS/JS into *.min.* files (the theme loads these automatically).
// Usage: NODE_PATH=<dir with terser + csso> node tools/minify.js
const fs = require('fs');
const path = require('path');
const { minify } = require('terser');
const csso = require('csso');

const theme = path.join(__dirname, '..', 'astra-child-schnitzmenu', 'assets');

(async () => {
  const cssIn = path.join(theme, 'css', 'schnitz.css');
  const css = csso.minify(fs.readFileSync(cssIn, 'utf8'), { restructure: false }).css;
  fs.writeFileSync(path.join(theme, 'css', 'schnitz.min.css'), css);

  const jsIn = path.join(theme, 'js', 'schnitz.js');
  const js = (await minify(fs.readFileSync(jsIn, 'utf8'), { compress: true, mangle: true })).code;
  fs.writeFileSync(path.join(theme, 'js', 'schnitz.min.js'), js);

  for (const [src, out] of [[cssIn, 'css/schnitz.min.css'], [jsIn, 'js/schnitz.min.js']]) {
    const before = fs.statSync(src).size;
    const after = fs.statSync(path.join(theme, out)).size;
    console.log(`${out}: ${(before / 1024).toFixed(1)} KB -> ${(after / 1024).toFixed(1)} KB`);
  }
})();
