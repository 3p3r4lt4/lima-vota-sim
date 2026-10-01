// Traduce la geolocalización por IP de Netlify (context.geo) a ubigeo INEI.
// Regla: solo se sube de precisión con una coincidencia exacta (sin tildes ni mayúsculas).
// Si algo no cuadra, se queda en el nivel anterior; nunca se inventa un distrito.

export const normalizar = (s) =>
  String(s ?? "").normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase()
    .replace(/[-_.,']/g, " ").replace(/\s+/g, " ").trim();

// Departamentos (y Callao) con su código ISO 3166-2:PE. LMA es la Municipalidad Metropolitana de Lima.
export const DEPARTAMENTOS = [
  ["01", "Amazonas", "AMA"], ["02", "Áncash", "ANC"], ["03", "Apurímac", "APU"], ["04", "Arequipa", "ARE"],
  ["05", "Ayacucho", "AYA"], ["06", "Cajamarca", "CAJ"], ["07", "Callao", "CAL"], ["08", "Cusco", "CUS"],
  ["09", "Huancavelica", "HUV"], ["10", "Huánuco", "HUC"], ["11", "Ica", "ICA"], ["12", "Junín", "JUN"],
  ["13", "La Libertad", "LAL"], ["14", "Lambayeque", "LAM"], ["15", "Lima", "LIM"], ["16", "Loreto", "LOR"],
  ["17", "Madre de Dios", "MDD"], ["18", "Moquegua", "MOQ"], ["19", "Pasco", "PAS"], ["20", "Piura", "PIU"],
  ["21", "Puno", "PUN"], ["22", "San Martín", "SAM"], ["23", "Tacna", "TAC"], ["24", "Tumbes", "TUM"],
  ["25", "Ucayali", "UCA"],
].map(([ubigeo, nombre, iso]) => ({ ubigeo, nombre, iso }));

// Provincias cubiertas: las del departamento de Lima y la Provincia Constitucional del Callao.
export const PROVINCIAS = [
  ["0701", "Callao"],
  ["1501", "Lima"], ["1502", "Barranca"], ["1503", "Cajatambo"], ["1504", "Canta"], ["1505", "Cañete"],
  ["1506", "Huaral"], ["1507", "Huarochirí"], ["1508", "Huaura"], ["1509", "Oyón"], ["1510", "Yauyos"],
].map(([ubigeo, nombre]) => ({ ubigeo, nombre }));

// Distritos de la provincia de Lima publicados en public/data/ambitos.json (un test vigila que coincidan)
// más el Cercado (150101), que solo se acepta con el nombre explícito «Cercado de Lima».
export const DISTRITOS_LIMA = [
  ["150101", "Lima", ["cercado de lima", "cercado"]],
  ["150102", "Ancón"], ["150103", "Ate", ["ate vitarte"]], ["150104", "Barranco"], ["150105", "Breña"],
  ["150106", "Carabayllo"], ["150107", "Chaclacayo"], ["150108", "Chorrillos"], ["150109", "Cieneguilla"],
  ["150110", "Comas"], ["150111", "El Agustino"], ["150112", "Independencia"], ["150113", "Jesús María"],
  ["150114", "La Molina"], ["150115", "La Victoria"], ["150116", "Lince"], ["150117", "Los Olivos"],
  ["150118", "Lurigancho-Chosica", ["lurigancho", "chosica"]], ["150119", "Lurín"],
  ["150120", "Magdalena del Mar", ["magdalena"]], ["150121", "Pueblo Libre", ["magdalena vieja"]],
  ["150122", "Miraflores"], ["150123", "Pachacámac"], ["150124", "Pucusana"], ["150125", "Puente Piedra"],
  ["150126", "Punta Hermosa"], ["150127", "Punta Negra"], ["150128", "Rímac"], ["150129", "San Bartolo"],
  ["150130", "San Borja"], ["150131", "San Isidro"], ["150132", "San Juan de Lurigancho"],
  ["150133", "San Juan de Miraflores"], ["150134", "San Luis"], ["150135", "San Martín de Porres"],
  ["150136", "San Miguel"], ["150137", "Santa Anita"], ["150138", "Santa María del Mar"], ["150139", "Santa Rosa"],
  ["150140", "Santiago de Surco", ["surco"]], ["150141", "Surquillo"], ["150142", "Villa El Salvador"],
  ["150143", "Villa María del Triunfo"],
].map(([ubigeo, nombre, alias = []]) => ({ ubigeo, nombre, alias }));

// Con subdivisión LIM (región Lima, no LMA) estos nombres también existen en otras provincias del
// departamento (p. ej. Miraflores en Yauyos): no se asigna distrito.
const AMBIGUOS_REGION_LIMA = new Set(["miraflores", "santa rosa", "san bartolo", "lima", "cercado"]);

const indice = (filas, claves) => {
  const m = new Map();
  for (const f of filas) for (const k of claves(f)) m.set(normalizar(k), f);
  return m;
};
const DEP_POR_ISO = new Map(DEPARTAMENTOS.map((d) => [d.iso, d]));
const DEP_POR_NOMBRE = indice(DEPARTAMENTOS, (d) => [d.nombre]);
const PROV_POR_UBIGEO = new Map(PROVINCIAS.map((p) => [p.ubigeo, p]));
const PROV_LIMA_POR_NOMBRE = indice(PROVINCIAS.filter((p) => p.ubigeo.startsWith("15")), (p) => [p.nombre]);
const DIST_POR_NOMBRE = indice(DISTRITOS_LIMA, (d) => [d.nombre, ...d.alias]);
// «Lima» a secas es la provincia (o el Cercado): no basta para un distrito
DIST_POR_NOMBRE.delete("lima");

// Nombres de subdivisión con prefijos y variantes habituales en bases de geo-IP
function departamentoPorNombre(nombre) {
  const n = normalizar(nombre)
    .replace(/^(region|departamento|provincia constitucional del?|provincia de|municipalidad metropolitana de|gobierno regional de)\s+/, "")
    .replace(/\s+(region|province|department|provincia)$/, "")
    .replace(/^el callao$/, "callao").replace(/^cuzco$/, "cusco");
  return DEP_POR_NOMBRE.get(n) ?? null;
}

const esLimaMetropolitana = (sub) => {
  const code = String(sub?.code ?? "").toUpperCase().replace(/^PE-/, "");
  const n = normalizar(sub?.name);
  return code === "LMA" || /^(lima province|provincia de lima|municipalidad metropolitana de lima|lima metropolitana)$/.test(n);
};

const vacio = { pais: null, departamento: null, provincia: null, distrito: null, ubigeo_geo: null, precision_geo: null };

export function resolverGeo(geo) {
  const pais = String(geo?.country?.code ?? "").toUpperCase();
  if (!/^[A-Z]{2}$/.test(pais)) return { ...vacio };
  const r = { ...vacio, pais, precision_geo: "pais" };
  if (pais !== "PE") return r;

  const sub = geo?.subdivision ?? {};
  const code = String(sub.code ?? "").toUpperCase().replace(/^PE-/, "");
  const metropolitana = esLimaMetropolitana(sub);
  const dep = metropolitana ? DEP_POR_ISO.get("LIM") : DEP_POR_ISO.get(code) ?? departamentoPorNombre(sub.name);
  if (!dep) return r;
  Object.assign(r, { departamento: dep.nombre, ubigeo_geo: dep.ubigeo, precision_geo: "departamento" });

  const ciudad = normalizar(geo?.city);
  const fijarProvincia = (p) => Object.assign(r, { provincia: p.nombre, ubigeo_geo: p.ubigeo, precision_geo: "provincia" });

  if (dep.ubigeo === "07") { fijarProvincia(PROV_POR_UBIGEO.get("0701")); return r; }  // provincia única
  if (dep.ubigeo !== "15") return r;

  if (metropolitana) fijarProvincia(PROV_POR_UBIGEO.get("1501"));
  if (!ciudad) return r;

  const distrito = DIST_POR_NOMBRE.get(ciudad);
  if (distrito && (metropolitana || !AMBIGUOS_REGION_LIMA.has(ciudad))) {
    fijarProvincia(PROV_POR_UBIGEO.get("1501"));
    return Object.assign(r, { distrito: distrito.nombre, ubigeo_geo: distrito.ubigeo, precision_geo: "distrito" });
  }
  // La ciudad coincide con una provincia de Lima (Huaral, Cañete…, o «Lima»): precisión de provincia
  const provincia = PROV_LIMA_POR_NOMBRE.get(ciudad);
  if (provincia && (metropolitana ? provincia.ubigeo === "1501" : true)) fijarProvincia(provincia);
  return r;
}
