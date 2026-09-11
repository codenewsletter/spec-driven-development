import re,sys
txt=open(sys.argv[1]).read()
# strip code blocks, tables, headings, quotes
body=re.sub(r"```.*?```","",txt,flags=re.S)
paras=[p.strip() for p in body.split("\n\n") if p.strip()]
words=0
for p in paras:
    if p.startswith(("#","|","- [","---")): continue
    p2=re.sub(r"\[([^\]]+)\]\([^)]+\)",r"\1",p)
    words+=len(p2.split())
    sents=[s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])",p2) if s]
    if len(sents)>3: print("PARA>3:",p2[:70])
    for s in sents:
        q=re.sub(r"\"[^\"]*\"","",s)  # skip quoted text
        n=len(s.split())
        if n>25: print(f"LONG({n}):",s[:90])
        for w in re.findall(r"\b\w+ing\b",q):
            if w.lower() not in ("thing","anything","nothing","everything","during","bring","string","morning","following"): print("ING:",w,"|",s[:60])
    if "—" in p: print("EMDASH:",p[:60])
    if re.search(r"\bworth\b|why this matters|this matters",p,re.I): print("BANNED:",p[:60])
print("words:",words)
