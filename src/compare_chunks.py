import json
for name in ("chunks_v1.json", "chunks.json"):
    c = json.load(open(name, encoding="utf-8"))
    avg = sum(len(x["text"]) for x in c) / len(c)
    low = sum(1 for x in c if x["text"][0].islower())
    print(f"{name}: total {len(c)} | avg length {avg:.0f} | starts lowercase {low}")