v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1310 -1010 1310 -980 {lab=n1}
N 1300 -980 1300 -920 {lab=n1}
N 1300 -980 1310 -980 {lab=n1}
N 1300 -840 1300 -820 {lab=vss}
N 1300 -890 1360 -890 {lab=vss}
N 1360 -890 1360 -840 {lab=vss}
N 1300 -840 1360 -840 {lab=vss}
N 1300 -860 1300 -840 {lab=vss}
N 1210 -890 1260 -890 {lab=inp}
N 1210 -1040 1210 -890 {lab=inp}
N 1210 -1040 1270 -1040 {lab=inp}
N 1310 -1120 1310 -1070 {lab=vdd}
N 1360 -840 1470 -840 {lab=vss}
N 1470 -920 1470 -840 {lab=vss}
N 1470 -980 1540 -980 {lab=vdd}
N 1310 -980 1390 -980 {lab=n1}
N 1390 -1040 1390 -980 {lab=n1}
N 1310 -1040 1390 -1040 {lab=n1}
N 1390 -1040 1470 -1040 {lab=n1}
C {iopin.sym} 1210 -970 2 0 {name=p1 lab=inp}
C {iopin.sym} 1310 -1120 2 0 {name=p2 lab=vdd}
C {iopin.sym} 1300 -820 2 0 {name=p3 lab=vss}
C {sg13g2_pr/sg13_lv_nmos.sym} 1290 -1040 0 0 {name=M2
l=0.13u
w=8u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 1280 -890 0 0 {name=M1
l=0.13u
w=8u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/isolbox.sym} 1470 -980 0 0 {name=D1
model=isolbox
l=7.0u
w=5.5u
spiceprefix=X
}
C {lab_wire.sym} 1540 -980 0 1 {name=p4 sig_type=std_logic lab=vdd}
C {lab_wire.sym} 1300 -950 0 1 {name=p5 sig_type=std_logic lab=n1}
