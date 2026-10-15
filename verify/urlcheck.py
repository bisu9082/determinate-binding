# -*- coding: utf-8 -*-
"""Layer 3/4: liveness of every cited URL (standards, legal instruments, reports)."""
import json, io, re, time, urllib.request, urllib.error, ssl
es = json.load(io.open("verify/entries.json", encoding="utf-8"))
todo = [e for e in es if e.get("url")]
ctx = ssl.create_default_context()
out = []
for i, e in enumerate(todo, 1):
    url = re.sub(r"\\([%&_#])", r"\1", e["url"]).strip()
    rec = {"key": e["key"], "class": e["class"], "url": url}
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, method="GET",
                    headers={"User-Agent": "Mozilla/5.0 (citation-audit)"})
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                rec.update(status=r.status, final=r.geturl()[:110])
            break
        except urllib.error.HTTPError as ex:
            rec.update(status=ex.code, final=""); break
        except Exception as ex:
            rec.update(status="ERR", final="", error=str(ex)[:60])
            time.sleep(1.5)
    out.append(rec)
    print(f"[{i:2d}/{len(todo)}] {str(rec['status']):>4} {e['key'][:44]}")
    time.sleep(0.25)
json.dump(out, io.open("verify/url_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print("\n", dict(Counter(str(r["status"]) for r in out)))
