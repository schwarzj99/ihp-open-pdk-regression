v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 410 -220 410 -210 {lab=C2}
N 410 -290 410 -280 {lab=C1}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Julian Schwarz 2026"}
C {iopin.sym} 410 -290 3 0 {name=p1 lab=C1}
C {iopin.sym} 410 -210 1 0 {name=p2 lab=C2}
C {sg13cmos5l_pr/cap_mfringe.sym} 410 -250 0 0 {name=C2
model=cap_mfringe
w=4.0u
l=4.0u
mmin=1
mmax=4
spiceprefix=X
}
