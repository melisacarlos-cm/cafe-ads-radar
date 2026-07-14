#!/usr/bin/env python3
"""
Actualizador diario del dashboard Café Ads Radar.

Uso:
  1. El agente diario recolecta los números del día y escribe ./today.json:
     {
       "date": "2026-07-14",
       "followers": { "@handle": 123456, ... },        # seguidores IG de hoy
       "ads":       { "@handle": {"active": 31, "week": 8}, ... }  # opcional, solo marcas con Motion
     }
  2. Corre:  python3 update.py
  3. Esto muta cafe-ads-radar.html en el lugar:
     - agrega {d:"date",v:N} al followersHist de cada marca (activa el % de crecimiento real)
     - actualiza ads.active / ads.week de las marcas con datos nuevos
     - actualiza SNAPSHOT_DATE y NOW
  4. Luego el agente publica el HTML al mismo link del artifact y hace git commit.

Regla de honestidad: si un dato no se encontró hoy, NO lo incluyas en today.json.
El script solo agrega snapshots para las marcas presentes; las ausentes conservan su último valor.
"""
import json, re, sys, os

HTML = os.path.join(os.path.dirname(__file__), "index.html")
TODAY = os.path.join(os.path.dirname(__file__), "today.json")

def now_decimal(date_str):
    y, m, d = (int(x) for x in date_str.split("-"))
    return y + ((m - 1) * 30 + (d - 1)) / 365.0

def main():
    if not os.path.exists(TODAY):
        sys.exit("No existe today.json — el agente debe crearlo primero.")
    data = json.load(open(TODAY))
    date = data["date"]
    followers = data.get("followers", {})
    ads = data.get("ads", {})

    html = open(HTML, encoding="utf-8").read()
    orig = html
    added, adupd = [], []

    # 1) append snapshot a followersHist por handle
    for handle, val in followers.items():
        val = int(val)
        pat = re.compile(r'(handle:"' + re.escape(handle) + r'"[\s\S]*?followersHist:\[)([\s\S]*?)(\])')
        m = pat.search(html)
        if not m:
            print(f"  ! no encontré followersHist para {handle}")
            continue
        # evita duplicar si ya se corrió hoy
        if f'd:"{date}"' in m.group(2):
            print(f"  = {handle} ya tiene snapshot de {date}, salto")
            continue
        new = m.group(1) + m.group(2) + f',{{d:"{date}",v:{val}}}' + m.group(3)
        html = html[:m.start()] + new + html[m.end():]
        added.append(handle)

    # 2) actualiza ads.active / ads.week por handle
    for handle, a in ads.items():
        act = a.get("active"); wk = a.get("week")
        if act is None:
            continue
        pat = re.compile(r'(handle:"' + re.escape(handle) + r'"[\s\S]*?ads:\{active:)(?:\d+|null)(,week:)(?:\d+|null)')
        m = pat.search(html)
        if not m:
            print(f"  ! no encontré ads para {handle}")
            continue
        wk_s = str(int(wk)) if wk is not None else "null"
        new = m.group(1) + str(int(act)) + m.group(2) + wk_s
        html = html[:m.start()] + new + html[m.end():]
        adupd.append(handle)

    # 3) fecha y NOW
    html = re.sub(r'const SNAPSHOT_DATE = "[^"]*";', f'const SNAPSHOT_DATE = "{date}";', html)
    html = re.sub(r'const NOW = [^;]+;', f'const NOW = {now_decimal(date):.5f};', html)

    if html == orig:
        print("Sin cambios.")
        return
    open(HTML, "w", encoding="utf-8").write(html)
    print(f"OK {date}: snapshots + [{', '.join(added) or 'ninguno'}]; ads actualizados [{', '.join(adupd) or 'ninguno'}]")

if __name__ == "__main__":
    main()
