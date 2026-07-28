v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 420 -380 420 -360 {lab=#net1}
N 420 -240 420 -220 {lab=#net2}
N 420 -160 420 -140 {lab=VSS}
N 420 -380 500 -380 {lab=#net1}
N 500 -380 500 -360 {lab=#net1}
N 500 -300 500 -280 {lab=ISO}
N 300 -300 420 -300 {lab=VDD}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Julian Schwarz 2026"}
C {sg13g2_pr/isolbox.sym} 420 -300 0 0 {name=D1
model=isolbox
l=10.0u
w=10.0u
spiceprefix=X
}
C {sg13g2_pr/ptap1_ring.sym} 420 -190 2 0 {name=R1
model=ptap1
spiceprefix=X
w=14e-6
l=14e-6
rw=0.3e-6
}
C {iopin.sym} 420 -140 1 0 {name=p2 lab=VSS}
C {sg13g2_pr/ptap1_ring.sym} 500 -330 2 1 {name=R2
model=ptap1
spiceprefix=X
w=7e-6
l=7e-6
rw=0.3e-6
}
C {iopin.sym} 500 -280 1 0 {name=p1 lab=ISO}
C {iopin.sym} 300 -300 2 0 {name=p3 lab=VDD}
