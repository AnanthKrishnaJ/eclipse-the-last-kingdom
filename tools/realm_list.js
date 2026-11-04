// Reads the Realms of Aurel data out of eclipse.html and writes docs/realms.json
// (every province, city, wild and boss with its stats) for the walkthrough.
//   node tools/realm_list.js
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(ROOT, 'eclipse.html'), 'utf8');
const cut = (a, b) => { const i = src.indexOf(a); if (i < 0) throw new Error('missing ' + a); return src.slice(i, src.indexOf(b, i)); };
const code = cut('function mulberry32(', '\n') + '\n' +
  cut('/* ================= REALMS OF AUREL', '/* province gear') +
  '\nreturn {RPROV,RBIOME,RC,RB,RBASE,RSIG};';
const W = new Function(code)();
const out = { provinces: [] };
for (const P of W.RPROV) {
  const cities = W.RC.filter(c => c.p === P.i).map(c => {
    const b = W.RB[c.boss], base = W.RBASE[b.arch], k = 1 + (b.lvl - 5) * .14;
    return { city: c.name, wild: c.wild, lvl: c.lvl, boss: b.name, role: b.role, arch: b.arch, variant: b.variant,
      sig: b.sig.map(k => W.RSIG[k]), adorn: b.adorn, scale: +b.pal.scale.toFixed(2),
      hp: Math.round(base.hp * Math.max(.8, k)), atk: +(base.atk * (1 + (b.lvl - 5) * .07)).toFixed(1), def: Math.round(base.def + b.lvl * .35),
      xp: Math.round(base.xp * Math.max(.8, k) * .8), gold: 60 + b.lvl * 12 };
  });
  out.provinces.push({ name: P.name, biome: P.biome, lvl: P.lvl, foes: P.foes, cities });
}
fs.writeFileSync(path.join(ROOT, 'docs', 'realms.json'), JSON.stringify(out, null, 1));
console.log('Wrote docs/realms.json:', out.provinces.length, 'provinces,', out.provinces.reduce((a, p) => a + p.cities.length, 0), 'cities');
