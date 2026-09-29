// Uso:
//   node render.mjs shots 1.0 3.5 ...   -> capturas PNG en ./shots
//   node render.mjs video               -> frames a ffmpeg -> out/video-mudo.mp4
import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import url from 'node:url';

const dir = path.dirname(url.fileURLToPath(import.meta.url));
const FPS = 30;
const [mode, ...rest] = process.argv.slice(2);
const FFMPEG = process.env.FFMPEG || 'ffmpeg';

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
page.on('pageerror', e => console.error('PAGE ERROR', e.message));
await page.goto('file://' + path.join(dir, 'index.html'));
await page.waitForFunction(() => window.READY === true);
const stage = await page.$('#stage');

async function frame(t, opts) {
  await page.evaluate(t => window.render(t), t);
  return stage.screenshot(opts);
}

if (mode === 'shots') {
  mkdirSync(path.join(dir, 'shots'), { recursive: true });
  for (const s of rest) {
    const t = parseFloat(s);
    await frame(t, { path: path.join(dir, 'shots', `f_${t.toFixed(2).padStart(5, '0')}.png`) });
    console.log('shot', t);
  }
} else if (mode === 'video') {
  mkdirSync(path.join(dir, 'out'), { recursive: true });
  const dur = await page.evaluate(() => window.DURATION);
  const total = Math.round(dur * FPS);
  const ff = spawn(FFMPEG, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    path.join(dir, 'out', 'video-mudo.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < total; i++) {
    const buf = await frame(i / FPS, { type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 60 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
}
await browser.close();
