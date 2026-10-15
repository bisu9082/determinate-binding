# -*- coding: utf-8 -*-
import re, json, io, sys

def parse(path):
    txt = io.open(path, encoding="utf-8").read()
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", txt):
        start = m.end()
        depth = 1; i = start
        while i < len(txt) and depth:
            if txt[i] == "{": depth += 1
            elif txt[i] == "}": depth -= 1
            i += 1
        body = txt[start:i-1]
        f = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            j = fm.end()
            if j >= len(body): break
            if body[j] == "{":
                d = 1; k = j + 1
                while k < len(body) and d:
                    if body[k] == "{": d += 1
                    elif body[k] == "}": d -= 1
                    k += 1
                val = body[j+1:k-1]
            elif body[j] == '"':
                k = body.index('"', j+1) + 1
                val = body[j+1:k-1]
            else:
                k = body.find(",", j)
                if k < 0: k = len(body)
                val = body[j:k]
            f[fm.group(1).lower()] = " ".join(val.split())
        entries.append(dict(key=m.group(2).strip(), type=m.group(1).lower(), **f))
    return entries

def classify(e):
    t = (e.get("title","") + " " + e.get("author","") + " " + e.get("note","")).lower()
    if e.get("doi"): return "doi"
    if re.search(r"\biso\b|\biec\b|\bastm\b|\bieee\b|ansi|\bul \b|nist ai|technical specification", t):
        return "standard"
    if re.search(r"regulation \(eu\)|directive|act,|act\b|notice no|decree|code of practice|"
                 r"authorised professional practice|framework convention|recommendation of the council", t):
        return "legal"
    if e["type"] in ("article","inproceedings","incollection"): return "academic_nodoi"
    return "report_or_web"

if __name__ == "__main__":
    es = parse(sys.argv[1])
    from collections import Counter
    for e in es: e["class"] = classify(e)
    print("total entries:", len(es))
    print("by class:", dict(Counter(e["class"] for e in es)))
    print("by type :", dict(Counter(e["type"] for e in es)))
    print("with url:", sum(1 for e in es if e.get("url")))
    json.dump(es, io.open(sys.argv[2],"w",encoding="utf-8"), ensure_ascii=False, indent=1)
