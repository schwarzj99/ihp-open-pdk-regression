v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1800 -980 1810 -980 {lab=vdd}
N 1330 -990 1330 -970 {lab=vss1}
N 1620 -1040 1720 -1040 {lab=#net1}
N 1620 -1050 1620 -1040 {lab=#net1}
N 1610 -920 1720 -920 {lab=#net2}
N 1610 -930 1610 -920 {lab=#net2}
N 1610 -1010 1610 -990 {lab=vss2}
N 1620 -1130 1620 -1110 {lab=vss1}
N 1330 -1040 1620 -1040 {lab=#net1}
N 1330 -990 1470 -990 {lab=vss1}
N 1330 -1010 1330 -990 {lab=vss1}
N 1470 -1130 1470 -990 {lab=vss1}
N 1470 -1130 1620 -1130 {lab=vss1}
N 1330 -900 1540 -900 {lab=vss2}
N 1540 -1010 1540 -900 {lab=vss2}
N 1540 -1010 1610 -1010 {lab=vss2}
N 1260 -1040 1290 -1040 {lab=inp}
N 1330 -1100 1330 -1070 {lab=out}
N 1330 -1100 1360 -1100 {lab=out}
N 1330 -1130 1330 -1100 {lab=out}
N 1260 -1160 1290 -1160 {lab=inp}
N 1260 -1160 1260 -1040 {lab=inp}
N 1220 -1040 1260 -1040 {lab=inp}
N 1330 -1240 1330 -1190 {lab=vdd}
N 1410 -1240 1800 -1240 {lab=vdd}
N 1800 -1240 1800 -980 {lab=vdd}
N 1720 -980 1800 -980 {lab=vdd}
N 1410 -1280 1410 -1240 {lab=vdd}
N 1330 -1240 1410 -1240 {lab=vdd}
N 1410 -1240 1410 -1220 {lab=vdd}
N 1330 -1160 1410 -1160 {lab=#net3}
C {iopin.sym} 1220 -1040 2 0 {name=p1 lab=inp}
C {iopin.sym} 1360 -1100 0 0 {name=p2 lab=out}
C {iopin.sym} 1330 -970 2 0 {name=p3 lab=vss1}
C {sg13g2_pr/sg13_lv_nmos.sym} 1310 -1040 0 0 {name=M1
l=0.13u
w=1u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/isolbox.sym} 1720 -980 0 0 {name=D1
model=isolbox
l=7.0u
w=5.5u
spiceprefix=X
}
C {iopin.sym} 1410 -1280 3 0 {name=p6 lab=vdd1}
C {iopin.sym} 1330 -900 2 0 {name=p7 lab=vss2}
C {sg13g2_pr/ptap1.sym} 1620 -1080 0 0 {name=R1
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/ptap1.sym} 1610 -960 0 0 {name=R2
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/sg13_lv_pmos.sym} 1310 -1160 0 0 {name=M2
l=0.13u
w=1u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/ntap1.sym} 1410 -1190 0 0 {name=R3
model=ntap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
