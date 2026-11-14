#!/usr/bin/env python3
import gzip,json,lzma,pathlib,subprocess,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
POOL=ROOT/"pool"; REPO=ROOT/"repo"; REPO.mkdir(exist_ok=True)
entries=[]; catalog=[]
for deb in sorted(POOL.rglob("*.deb")):
    rel=deb.relative_to(ROOT).as_posix()
    raw=subprocess.check_output(["dpkg-deb","-f",str(deb)],text=True)
    fields={}; key=None
    for line in raw.splitlines():
        if line and not line[0].isspace() and ":" in line:
            key,value=line.split(":",1); fields[key]=value.strip()
        elif key and line:
            fields[key]+="\n"+line.strip()
    data=deb.read_bytes(); fields["Filename"]=rel; fields["Size"]=str(len(data)); fields["SHA256"]=hashlib.sha256(data).hexdigest()
    entries.append("\n".join(f"{k}: {v}" for k,v in fields.items()))
    platforms=[]
    for value in (fields.get("Architecture",""),fields.get("Description",""),fields.get("Tag","")):
        for label in ("RootHide","Rootless","Rootful"):
            if label.lower() in value.lower(): platforms.append(label)
    catalog.append({"name":fields.get("Name",fields.get("Package",deb.stem)),"package":fields.get("Package",""),"version":fields.get("Version",""),"description":fields.get("Description",""),"author":fields.get("Author",""),"platforms":sorted(set(platforms)),"depiction":fields.get("Depiction","")})
payload=("\n\n".join(entries)+("\n" if entries else "")).encode()
(ROOT/"Packages").write_bytes(payload)
(ROOT/"Packages.gz").write_bytes(gzip.compress(payload,compresslevel=9))
(ROOT/"Packages.xz").write_bytes(lzma.compress(payload,preset=9))
(REPO/"packages.json").write_text(json.dumps(catalog,indent=2),encoding="utf-8")
print("Indexed",len(entries),"packages")
