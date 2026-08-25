"""Split the monolithic sg13g2_io netlist into one self-contained file per IO pad.

Each output holds the pad's .subckt plus the transitive closure of every
sub-block it instantiates, emitted in the source file's own bottom-up order.
"""
import pathlib, re, datetime, sys

ROOT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "netlist" / "sg13g2_io.spi"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "netlist" / "pads"
LAYOUT = ROOT / "layout"

raw = SRC.read_text().splitlines()

# join '+' continuation lines onto their predecessor, remembering the split
lines = []
for ln in raw:
    if ln.startswith("+") and lines:
        lines[-1] = lines[-1] + " " + ln[1:].strip()
    else:
        lines.append(ln)

# ---- carve into blocks -------------------------------------------------
header = []
blocks = {}       # name -> list of lines (leading comments + subckt body)
order = []        # source order of subckt names

i = 0
# header: everything before the first .subckt, minus the comments that belong to it
first = next(k for k, l in enumerate(lines) if l.lower().startswith(".subckt"))
h_end = first
while h_end > 0 and lines[h_end - 1].startswith("*"):
    h_end -= 1
header = lines[:h_end]

while i < len(lines):
    if lines[i].lower().startswith(".subckt"):
        start = i
        while start > 0 and lines[start - 1].startswith("*"):
            start -= 1
        name = lines[i].split()[1]
        end = i
        while not lines[end].lower().startswith(".ends"):
            end += 1
        blocks[name] = lines[start:end + 1]
        order.append(name)
        i = end + 1
    else:
        i += 1

names = set(blocks)

# ---- dependency edges --------------------------------------------------
def deps_of(name):
    out = []
    for ln in blocks[name]:
        s = ln.strip()
        if not s or not s[0] in "Xx":
            continue
        toks = [t for t in s.split() if "=" not in t]
        if len(toks) >= 2 and toks[-1] in names:
            out.append(toks[-1])
    return out

def closure(top):
    seen, stack = set(), [top]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(deps_of(n))
    return seen

# ---- pads to emit: one per extracted GDS -------------------------------
pads = sorted(p.stem for p in LAYOUT.glob("sg13g2_IOPad*.gds"))
missing = [p for p in pads if p not in names]
if missing:
    raise SystemExit(f"no subckt for: {missing}")

OUT.mkdir(exist_ok=True)
stamp = datetime.date.today().isoformat()

for pad in pads:
    need = closure(pad)
    body = []
    for n in order:
        if n in need:
            body.extend(blocks[n])
            body.append("")
    text = "\n".join(
        [f"* {pad}", "",
         f"* Split from {SRC.name} on {stamp}; contains {pad} and its",
         f"* {len(need) - 1} supporting subckts. Edit the source netlist, not this file.",
         ""]
        + header[1:]
        + [""]
        + body
    ).rstrip() + "\n"
    (OUT / f"{pad}.spi").write_text(text)
    print(f"{pad:28s} {len(need):3d} subckts  {len(text.splitlines()):5d} lines")
