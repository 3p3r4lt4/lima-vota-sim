// Parser mínimo de user-agent: tipo de dispositivo, SO y navegador con versión mayor, y detección de bots.
// No pretende ser exhaustivo; lo desconocido queda como "Otro" en vez de adivinar.

const BOT = /(?<!cu)bot\b|bot\/|crawl|spider|slurp|preview|headless|lighthouse|pagespeed|facebookexternalhit|facebookcatalog|embedly|whatsapp|telegram|discord|skype|curl\/|wget|python-|httpclient|okhttp|axios|node-fetch|undici|go-http|java\/|libwww|monitor|uptime|pingdom|scan|phantomjs|puppeteer|playwright|selenium|validator|feed|archiver/i;

const mayor = (v) => (v ? String(v).split(/[._]/)[0] : null);

function sistema(ua) {
  let m;
  if ((m = ua.match(/(iPhone|iPod|iPad)[^)]*? OS (\d+)/))) return { so: m[1] === "iPad" ? "iPadOS" : "iOS", so_version: m[2] };
  if (/iPhone|iPod/.test(ua)) return { so: "iOS", so_version: null };
  if ((m = ua.match(/Android[ /]?(\d+)?/))) return { so: "Android", so_version: m[1] ?? null };
  if ((m = ua.match(/Windows NT (\d+\.\d+)/))) {
    const v = { "10.0": "10", "6.3": "8.1", "6.2": "8", "6.1": "7" }[m[1]] ?? m[1];
    return { so: "Windows", so_version: v };
  }
  if (/Windows/.test(ua)) return { so: "Windows", so_version: null };
  if ((m = ua.match(/CrOS [^ ]+ (\d+)/))) return { so: "ChromeOS", so_version: m[1] };
  if ((m = ua.match(/Mac OS X (\d+)/))) return { so: "macOS", so_version: m[1] };
  if (/Macintosh/.test(ua)) return { so: "macOS", so_version: null };
  if (/Linux/.test(ua)) return { so: "Linux", so_version: null };
  return { so: "Otro", so_version: null };
}

// El orden importa: las apps y los navegadores derivados de Chromium se reconocen antes que Chrome/Safari.
const NAVEGADORES = [
  ["Instagram", /Instagram (\d+)/],
  ["Facebook", /FBAV\/(\d+)|FB_IAB/],
  ["TikTok", /(?:musical_ly|BytedanceWebview|TikTok)[_/ ]?(\d+)?/],
  ["Edge", /Edg(?:e|A|iOS)?\/(\d+)/],
  ["Opera", /OPR\/(\d+)|OPT\/(\d+)|Opera[/ ](\d+)/],
  ["Samsung Internet", /SamsungBrowser\/(\d+)/],
  ["UC Browser", /UCBrowser\/(\d+)/],
  ["Firefox", /(?:Firefox|FxiOS)\/(\d+)/],
  ["Chrome", /CriOS\/(\d+)/],
  ["Android WebView", /; wv\).*Chrome\/(\d+)/],
  ["Chrome", /Chrome\/(\d+)/],
  ["Safari", /Version\/(\d+)[^ ]* (?:Mobile\/\S+ )?Safari\//],
];

function navegador(ua) {
  for (const [nombre, re] of NAVEGADORES) {
    const m = ua.match(re);
    if (m) return { navegador: nombre, navegador_version: mayor(m.slice(1).find(Boolean)) };
  }
  return { navegador: "Otro", navegador_version: null };
}

function tipo(ua, so) {
  if (/iPad|Tablet|PlayBook|Silk|Kindle/.test(ua)) return "tablet";
  if (so === "Android") return /Mobile/.test(ua) ? "movil" : "tablet";
  if (/iPhone|iPod|Mobile|Opera Mini|IEMobile|Windows Phone/.test(ua)) return "movil";
  if (["Windows", "macOS", "Linux", "ChromeOS"].includes(so)) return "escritorio";
  return "desconocido";
}

export function analizarUA(entrada) {
  const ua = String(entrada ?? "").slice(0, 512);
  if (!ua.trim()) return { dispositivo_tipo: "desconocido", so: "Otro", so_version: null, navegador: "Otro", navegador_version: null, es_bot: true };
  const s = sistema(ua);
  return { dispositivo_tipo: tipo(ua, s.so), ...s, ...navegador(ua), es_bot: BOT.test(ua) };
}
