import { test } from "node:test";
import assert from "node:assert/strict";
import { analizarUA } from "./ua.mjs";

const UA = {
  iphone: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
  ipad: "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.6099.119 Mobile/15E148 Safari/604.1",
  android: "Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
  samsung: "Mozilla/5.0 (Linux; Android 13; SM-A135F) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/117.0.0.0 Mobile Safari/537.36",
  tabletAndroid: "Mozilla/5.0 (Linux; Android 12; SM-X200) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
  windowsChrome: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  windowsEdge: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.2535.51",
  macFirefox: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
  instagram: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 312.0.0.32.112 (iPhone14,5; iOS 17_1; es_PE)",
  googlebot: "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.141 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
  googlebotDesktop: "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
  headless: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.0.0 Safari/537.36",
  whatsapp: "WhatsApp/2.23.20.0 A",
  cubot: "Mozilla/5.0 (Linux; Android 10; CUBOT X30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
};

test("iPhone con Safari", () => {
  assert.deepEqual(analizarUA(UA.iphone), {
    dispositivo_tipo: "movil", so: "iOS", so_version: "17", navegador: "Safari", navegador_version: "17", es_bot: false,
  });
});

test("iPad con Chrome es tablet", () => {
  const r = analizarUA(UA.ipad);
  assert.equal(r.dispositivo_tipo, "tablet");
  assert.equal(r.so, "iPadOS");
  assert.equal(r.navegador, "Chrome");
  assert.equal(r.navegador_version, "120");
});

test("Android con Chrome", () => {
  assert.deepEqual(analizarUA(UA.android), {
    dispositivo_tipo: "movil", so: "Android", so_version: "14", navegador: "Chrome", navegador_version: "124", es_bot: false,
  });
});

test("Samsung Internet y tablet Android", () => {
  assert.equal(analizarUA(UA.samsung).navegador, "Samsung Internet");
  assert.equal(analizarUA(UA.samsung).navegador_version, "24");
  assert.equal(analizarUA(UA.tabletAndroid).dispositivo_tipo, "tablet");
});

test("Windows con Chrome y con Edge", () => {
  assert.deepEqual(analizarUA(UA.windowsChrome), {
    dispositivo_tipo: "escritorio", so: "Windows", so_version: "10", navegador: "Chrome", navegador_version: "125", es_bot: false,
  });
  assert.equal(analizarUA(UA.windowsEdge).navegador, "Edge");
});

test("macOS con Firefox e Instagram in-app", () => {
  const mac = analizarUA(UA.macFirefox);
  assert.equal(mac.so, "macOS");
  assert.equal(mac.navegador, "Firefox");
  assert.equal(mac.navegador_version, "126");
  assert.equal(analizarUA(UA.instagram).navegador, "Instagram");
});

test("bots: Googlebot, headless y vistas previas", () => {
  for (const ua of [UA.googlebot, UA.googlebotDesktop, UA.headless, UA.whatsapp, "curl/8.4.0", ""]) {
    assert.equal(analizarUA(ua).es_bot, true, ua);
  }
  assert.equal(analizarUA(UA.cubot).es_bot, false);
});
