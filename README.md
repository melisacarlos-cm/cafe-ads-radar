# Café Ads Radar ☕

Dashboard de benchmark competitivo de 6 marcas de café DTC/especialidad en EE. UU.
Rastrea presencia en Instagram/Facebook y actividad publicitaria en Meta.

**Repo privado** — contiene el código fuente y la automatización. NO es el link que se comparte.
El dashboard se comparte por su **link de Artifact** (privado, link-only):
https://claude.ai/code/artifact/34c3d938-e82f-41aa-bdad-9157c927019d

## Marcas
Chamberlain Coffee · Blue Bottle Coffee · Death Wish Coffee · Onyx Coffee Lab · Cometeer · Trade Coffee

## Archivos
- `cafe-ads-radar.html` — el dashboard (datos embebidos en el bloque `const BRANDS` / `CAMPAIGNS`).
- `update.py` — actualizador diario: lee `today.json` y muta el HTML (agrega snapshot de seguidores, actualiza ads, fecha).
- `today.json` — (lo escribe el agente diario) números recolectados del día.

## Flujo del tracking diario
1. Recolectar seguidores IG (WebSearch → snippets de StarNgage/SpeakRJ/etc.) y ads (WebFetch a Motion) de cada marca.
2. Escribir `today.json`:
   ```json
   { "date":"2026-07-14",
     "followers": {"@chamberlaincoffee":544500, "@bluebottle":513200, "@deathwishcoffee":344500,
                   "@onyxcoffeelab":285300, "@cometeer":95200, "@tradecoffeeco":84100},
     "ads": {"@chamberlaincoffee":{"active":17,"week":5}, "@bluebottle":{"active":31,"week":8},
             "@onyxcoffeelab":{"active":38,"week":5}} }
   ```
3. `python3 update.py` → muta `cafe-ads-radar.html`.
4. Publicar el HTML al mismo link del Artifact + `git commit`.

## Fuentes de datos (Motion slugs que funcionan)
- Motion (ads): `onyx-coffee-lab`, `blue-bottle-coffee`, `chamberlain-coffee`. Los demás (Death Wish, Cometeer, Trade) no tienen página → `s/d`.
- Regla de honestidad: si un dato no se encuentra, NO se incluye en `today.json` (conserva el último valor). Nunca inventar cifras.
