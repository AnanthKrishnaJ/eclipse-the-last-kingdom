// Reads the heroine data straight out of eclipse.html and writes docs/heroine_events.json,
// which build_walkthrough.py renders as the heroine chapters of the walkthrough.
//   node tools/heroine_events.js
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(ROOT, 'eclipse.html'), 'utf8');

function block(start, end) {
  const i = src.indexOf(start);
  if (i < 0) throw new Error('missing ' + start);
  const j = src.indexOf(end, i);
  return src.slice(i, j);
}
const ctx = {};
const run = code => new Function('C', code.replace(/^const (\w+)=/, 'C.$1=') + ';')(ctx);
run(block('const HEROINES={', '\nfor(const id in HEROINES)'));
run(block('const TALK={', '\nfunction S('));
run(block('const DATE2={', '\nfunction afterDate'));
run(block('const KISS={', '\nconst KISSYES'));
run(block('const ANNIV={', '\n\n'));
run(block('const EVE={', '\nconst wivesNow'));
run(block('const CAMP=[', '\nfunction campScene'));
run(block('const BANTER=[', '\nconst greetLine'));

const names = {};
for (const m of src.matchAll(/(\w+):\{name:'((?:[^'\\]|\\.)*)'/g)) if (!names[m[1]]) names[m[1]] = m[2].replace(/\\'/g, "'");
const nm = id => names[id] || id;
const clean = s => s.replace(/^\[\w+\]\s*/, '');
const H = ctx.HEROINES, T = ctx.TALK, D2 = ctx.DATE2;
const order = ['mimi', 'lyra', 'serah', 'noelle'];
const PLACE = { hill: 'Sakura Hill', cafe: 'Plaza café', river: 'Riverside (Woods)', garden: 'Flower garden', lake: 'Lakeside at sunset', picnic: 'Picnic in Dawnmeadow', stars: 'Stargazing', walk: 'Evening walk' };
const STAT = { aff: 'affection', trust: 'trust', friend: 'friendship' };

const WHERE = {
  mimi: 'Eldoria, south-west of the plaza, beside the bounty board of the guild outpost.',
  lyra: 'The Whispering Woods, beside the lantern in the eastern part of the forest.',
  serah: 'Eldoria, on the east side of the village by the garrison supply crates.',
  noelle: 'Eldoria, at the guild outpost counter in the south-west of the village. Meeting her registers you with the guild.'
};
const JOIN = {
  mimi: 'Offers to team up at your first meeting. Accept and she joins at once; refuse and ask her later.',
  lyra: 'Joins once you hold the Sanctum Key or Grukk has fallen ("Ask her to join you").',
  serah: 'Joins only after Grukk the Warlord is defeated.',
  noelle: 'Never fights. Her story is about finding the courage to adventure again.'
};
const MEET = {
  mimi: ["Let's team up.", 'She joins your party and gains friendship.', 'Maybe later.', 'No change; she waits in Eldoria.'],
  lyra: ['I could use a scholar.', '+5 trust.', 'You are a bit creepy.', '-2 affection.'],
  serah: ['I am here to help.', '+3 trust. She tells you to prove it against Grukk.', 'Nice to meet you, Captain.', '+3 affection.'],
  noelle: null
};
const QUEST = {
  mimi: [['Unlock', 'Friendship 30, then choose "Is something on your mind?"'], ['Step 1', "Find the bell charm in the slime meadow, south of the woodland road in the Whispering Woods. It glints on the ground only while this quest is active."], ['Finish', 'Give it back ("Return the bell charm"). +25 trust, +8 affection. Scene: Mimi\'s bell (riverside).']],
  lyra: [['Unlock', 'Friendship 30, then choose "Is something on your mind?"'], ['Step 1', 'Bring her 2 Lumen Crystals (Crystal Shards) from the Crystal Caverns. +10 trust.'], ['Step 2', 'With Lyra in your party, examine the Moon Shrine in the hidden glade at night. Earlier in the day she asks to come back after dark.'], ['Finish', 'Scene: Moonlit shrine. +20 trust, +8 affection.']],
  serah: [['Unlock', 'Friendship 30, then choose "Is something on your mind?"'], ['Step 1', 'Defeat the Eclipsed Sentinel with Serah in your party.'], ['Step 2', 'Talk to her and choose "Spar with her".'], ['Finish', 'Scene: Sparring at dawn (training yard). +20 trust, +8 affection.']],
  noelle: [['Unlock', 'Friendship 30, then choose "Is something on your mind?"'], ['Step 1', 'Reach guild rank D. The quest updates the next time you talk to her.'], ['Step 2', "After Grukk falls, pick up the Lantern Dagger in Grukk's clearing in the Whispering Woods."], ['Finish', 'Give it back ("Return her dagger"). +22 trust, +8 affection. Scene: The fourth lantern (guild).']]
};

function best(opts) { return opts.slice().sort((a, b) => b[1] - a[1]); }
const out = { heroines: [], shared: {} };
for (const id of order) {
  const h = H[id], t = T[id];
  const topics = t.topics.map(tp => {
    const c = tp.c.slice().sort((a, b) => (b[2] - a[2]));
    return [tp.t, `Best: "${c[0][0]}" (+${c[0][2]} ${STAT[c[0][1]]}). Avoid: "${c[c.length - 1][0]}" (${c[c.length - 1][2]} ${STAT[c[c.length - 1][1]]}).`];
  });
  const dates = [];
  for (const p of ['hill', 'cafe', 'river']) { const d = t.date[p], b = best([d[1], d[2]]); dates.push([PLACE[p], `"${b[0][0]}" (+${b[0][1]})`]); }
  for (const p of ['garden', 'lake', 'picnic', 'stars', 'walk']) { const d = D2[id][p], b = best(d.slice(1)); dates.push([PLACE[p], `"${b[0][0]}" (+${b[0][1]})`]); }
  out.heroines.push({
    id, name: h.name, short: h.short, title: h.title, age: h.age, bio: h.bio, goal: h.goal, flaw: h.flaw,
    where: WHERE[id], join: JOIN[id], special: h.combat ? `${h.combat.special}: ${h.combat.sdesc}` : 'None (non-combat).',
    gifts: [['Loves (+8)', h.loves.map(nm).join(', ')], ['Likes (+4)', h.likes.map(nm).join(', ')], ['Dislikes (-5)', h.dislikes.map(nm).join(', ')]],
    meet: MEET[id], topics, dates, quest: QUEST[id],
    confess: t.confess.map(p => p[1]).join(' '), kiss: ctx.KISS[id].map(p => p[1]).join(' '),
    propose: t.propose.map(p => p[1]).join(' '), wed: t.wed.map(p => p[1]).join(' '),
    eve: [ctx.EVE[id][0], best(ctx.EVE[id][1])[0][0]], anniv: ctx.ANNIV[id].map(p => p[1]).join(' ')
  });
}
out.shared.camp = ctx.CAMP.map(c => [c.p.map(p => H[p].short).join(' + '), clean(c.s[0][2]) + (c.c ? ' Choices: ' + c.c.map(o => '"' + o[0] + '"').join(' or ') : ' No choice; everyone gains friendship.')]);
out.shared.banter = ctx.BANTER.map(b => [H[b[0]].short + ' and ' + H[b[2]].short, `"${b[1]}" / "${b[3]}"`]);
fs.writeFileSync(path.join(ROOT, 'docs', 'heroine_events.json'), JSON.stringify(out, null, 1));
console.log('Wrote docs/heroine_events.json');
