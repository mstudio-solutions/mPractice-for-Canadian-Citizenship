// Build the app version of the page into www/ for Capacitor (iOS).
// Same page as the website, but with Tailwind compiled to a local file
// (www/app.css, made by the build:www npm script) so the app works offline.
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';

const CDN = '<script src="https://cdn.tailwindcss.com"></script>';
const html = readFileSync('index.html', 'utf8');
if (!html.includes(CDN)) throw new Error('Tailwind CDN tag not found in index.html');
if (html.includes('cloudflareinsights')) throw new Error('Remove analytics from the app build');

mkdirSync('www', { recursive: true });
writeFileSync('www/index.html', html.replace(CDN, '<link rel="stylesheet" href="app.css"/>'));
console.log('www/index.html written');
