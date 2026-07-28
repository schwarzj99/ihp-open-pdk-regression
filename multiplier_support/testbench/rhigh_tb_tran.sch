v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
T {Testbench for transient analysis - Inverter} 740 -1730 0 0 1 1 {}
N 980 -840 980 -820 {lab=VDD}
N 980 -760 980 -740 {lab=GND}
N 1300 -1060 1300 -1020 {lab=#net1}
N 1520 -1060 1520 -1020 {lab=#net2}
N 1520 -1140 1520 -1120 {lab=VDD}
N 1420 -1140 1520 -1140 {lab=VDD}
N 1300 -1140 1300 -1120 {lab=VDD}
N 1420 -1160 1420 -1140 {lab=VDD}
N 1300 -1140 1420 -1140 {lab=VDD}
N 1300 -840 1360 -840 {lab=direct}
N 1240 -840 1240 -820 {lab=direct}
N 1360 -840 1360 -820 {lab=direct}
N 1240 -760 1240 -740 {lab=GND}
N 1300 -740 1360 -740 {lab=GND}
N 1360 -760 1360 -740 {lab=GND}
N 1300 -740 1300 -720 {lab=GND}
N 1240 -740 1300 -740 {lab=GND}
N 1520 -960 1520 -920 {lab=morb}
N 1520 -860 1520 -820 {lab=GND}
N 1300 -960 1300 -940 {lab=#net3}
N 1300 -880 1300 -840 {lab=direct}
N 1240 -840 1300 -840 {lab=direct}
C {devices/code_shown.sym} 80 -1370 0 0 {name=NGSPICE
only_toplevel=true 
value="
.param temp=27
.options savecurrents klu method=gear reltol=1e-4 abstol=1e-15 gmin=1e-15
.control

save all

* Transient Analysis
tran 1u 5m

* Plotting
plot direct morb
plot i(VDD)

*quit
.endc
"}
C {devices/launcher.sym} 740 -170 0 0 {name=h2
descr="Simulate" 
tclcommand="xschem save; xschem netlist; xschem simulate"
}
C {title-3.sym} 0 0 0 0 {name=l2 author="Julian Schwarz" rev=1.0 lock=true}
C {devices/launcher.sym} 740 -50 0 0 {name=h1
descr="Load waves" 
tclcommand="xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw tran"
}
C {devices/launcher.sym} 740 -110 0 0 {name=h3
descr="Annotate OP" 
tclcommand="set show_hidden_texts 1; xschem annotate_op"
}
C {devices/vsource.sym} 980 -790 0 1 {name=VDD spice_ignore=False value=1.5
}
C {devices/gnd.sym} 980 -740 0 0 {name=l26 lab=GND}
C {devices/code_shown.sym} 900 -160 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerHBT.lib hbt_typ
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
.lib cornerDIO.lib dio_tt
"}
C {isource.sym} 1300 -1090 0 0 {name=I0 value=1m}
C {isource.sym} 1520 -1090 0 0 {name=I1 value=1m}
C {vdd.sym} 980 -840 0 0 {name=l1 lab=VDD}
C {vdd.sym} 1420 -1160 0 0 {name=l3 lab=VDD}
C {sg13g2_pr/rhigh.sym} 1240 -790 0 0 {name=R1
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
 m=1
  mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {sg13g2_pr/rhigh.sym} 1360 -790 0 0 {name=R2
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
 m=1
  mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {sg13g2_pr/rhigh.sym} 1300 -990 0 0 {name=R3
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
 m=1
  mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {devices/gnd.sym} 1300 -720 0 0 {name=l4 lab=GND}
C {sg13g2_pr/rhigh.sym} 1520 -890 0 0 {name=R4
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
m=2
mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {sg13g2_pr/rhigh.sym} 1520 -990 0 0 {name=R6
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=1
m=1
mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {devices/gnd.sym} 1520 -820 0 0 {name=l5 lab=GND}
C {sg13g2_pr/rhigh.sym} 1300 -910 0 0 {name=R5
w=0.5e-6
l=0.96e-6
model=rhigh
body=sub!
spiceprefix=X
b=0
 m=1
  mm_ok=1
value="expr_eng(  ( 1.6e-4 / @w + 1360.0 * ( (@b + 1)* @l + ( 1.081*( @w - 0.04e-6 ) + 0.18e-6 )*@b ) / ( @w - 0.04e-6 ) ) / @m  )"
}
C {lab_wire.sym} 1360 -840 0 0 {name=p2 sig_type=std_logic lab=direct}
C {lab_wire.sym} 1520 -930 0 0 {name=p1 sig_type=std_logic lab=morb}
C {sg13g2_pr/ptap1.sym} 1750 -820 2 0 {name=R7
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {lab_pin.sym} 1750 -850 1 0 {name=p3 sig_type=std_logic lab=sub!}
C {devices/gnd.sym} 1750 -790 0 0 {name=l6 lab=GND}
