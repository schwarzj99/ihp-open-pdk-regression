v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 940 -1040 980 -1040 {lab=A}
N 940 -880 980 -880 {lab=C}
N 940 -960 980 -960 {lab=B}
N 1040 -1040 1060 -1040 {lab=#net1}
N 1060 -960 1060 -880 {lab=#net1}
N 1040 -880 1060 -880 {lab=#net1}
N 1040 -960 1060 -960 {lab=#net1}
N 1060 -1040 1060 -960 {lab=#net1}
C {title-3.sym} 0 0 0 0 {name=l1 author="IHP-Open-PDK Authors 2026" rev=1.0 lock=true title="Isolated nmos"}
C {iopin.sym} 940 -1040 2 0 {name=p1 lab=A}
C {iopin.sym} 940 -960 2 0 {name=p2 lab=B}
C {iopin.sym} 940 -880 2 0 {name=p3 lab=C}
C {res.sym} 1010 -1040 1 0 {name=R1
value=10m
footprint=1206
device=resistor
m=1}
C {res.sym} 1010 -960 1 0 {name=R2
value=10m
footprint=1206
device=resistor
m=1}
C {res.sym} 1010 -880 1 0 {name=R3
value=10m
footprint=1206
device=resistor
m=1}
