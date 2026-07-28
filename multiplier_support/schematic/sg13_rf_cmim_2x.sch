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
N 340 -220 390 -220 {lab=CX}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Julian Schwarz 2026"}
C {iopin.sym} 420 -280 3 0 {name=p1 lab=C0}
C {iopin.sym} 420 -160 1 0 {name=p2 lab=C1}
C {iopin.sym} 340 -220 2 0 {name=p3 lab=CX}
C {lab_pin.sym} 580 -220 0 0 {name=p4 sig_type=std_logic lab=CX}
C {sg13g2_pr/cap_rfcmim.sym} 420 -220 0 0 {name=C1 
model=cap_rfcmim
lvs_model=rfcmim
 w=10.0e-6
 l=10.0e-6
 wfeed=5.0e-6
 m=1
  mm_ok=1
 spiceprefix=X}
C {sg13g2_pr/cap_rfcmim.sym} 610 -220 0 0 {name=C2 
model=cap_rfcmim
lvs_model=rfcmim
 w=10.0e-6
 l=10.0e-6
 wfeed=5.0e-6
 m=1
  mm_ok=1
 spiceprefix=X}
