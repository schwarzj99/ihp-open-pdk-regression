v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 420 -270 420 -250 {lab=C0}
N 420 -170 420 -160 {lab=C1}
N 420 -170 610 -170 {lab=C1}
N 420 -190 420 -170 {lab=C1}
N 610 -190 610 -170 {lab=C1}
N 610 -270 610 -250 {lab=C0}
N 420 -270 610 -270 {lab=C0}
N 420 -280 420 -270 {lab=C0}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Julian Schwarz 2026"}
C {sg13g2_pr/cap_cmim.sym} 420 -220 0 0 {name=C1
model=cap_cmim
w=7.0e-6
l=7.0e-6
m=1
spiceprefix=X}
C {iopin.sym} 420 -280 3 0 {name=p1 lab=C0}
C {iopin.sym} 420 -160 1 0 {name=p2 lab=C1}
C {sg13g2_pr/cap_cmim.sym} 610 -220 0 0 {name=C2
model=cap_cmim
w=7.0e-6
l=7.0e-6
m=1
spiceprefix=X}
