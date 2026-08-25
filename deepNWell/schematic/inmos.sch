v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 1350 -700 1350 -680 {lab=sub!}
N 1030 -880 1170 -880 {lab=isosub}
N 1170 -880 1170 -860 {lab=isosub}
N 1030 -800 1170 -800 {lab=S}
N 1030 -850 1030 -800 {lab=S}
N 940 -800 1030 -800 {lab=S}
N 1350 -880 1350 -820 {lab=isosub}
N 1170 -880 1350 -880 {lab=isosub}
N 940 -760 1350 -760 {lab=nwell}
N 940 -880 990 -880 {lab=G}
N 1030 -950 1030 -910 {lab=D}
N 940 -950 1030 -950 {lab=D}
N 1170 -930 1170 -880 {lab=isosub}
C {title-3.sym} 0 0 0 0 {name=l1 author="IHP-Open-PDK Authors 2026" rev=1.0 lock=true title="Isolated nmos"}
C {sg13g2_pr/sub.sym} 1350 -680 0 0 {name=l2 lab=sub!}
C {sg13g2_pr/sg13_lv_nmos.sym} 1010 -880 0 0 {name=M1
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/ptap1.sym} 1170 -830 2 1 {name=R1
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/isolbox.sym} 1350 -760 0 0 {name=D1
model=isolbox
l=6.0u
w=6.0u
spiceprefix=X
}
C {iopin.sym} 940 -950 2 0 {name=p1 lab=D}
C {iopin.sym} 940 -880 2 0 {name=p2 lab=G}
C {iopin.sym} 940 -800 2 0 {name=p3 lab=S}
C {iopin.sym} 940 -760 2 0 {name=p4 lab=nwell}
C {lab_pin.sym} 1170 -930 2 0 {name=p5 sig_type=std_logic lab=isosub}
