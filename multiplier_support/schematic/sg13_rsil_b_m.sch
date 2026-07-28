v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 420 -280 420 -250 {lab=A}
N 420 -190 420 -160 {lab=B}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Julian Schwarz 2026"}
C {iopin.sym} 420 -280 3 0 {name=p1 lab=A}
C {iopin.sym} 420 -160 1 0 {name=p2 lab=B}
C {sg13g2_pr/rsil.sym} 420 -220 0 0 {name=R1
w=0.5e-6
l=0.5e-6
model=rsil
body=sub!
spiceprefix=X
b=0
m=2 
mm_ok=1
value="expr_eng(  ( 9.0e-6 / @w + 7.0 * ( (@b+1) * @l ) / ( @w + 1.0e-8 ) ) / @m  )"
}
