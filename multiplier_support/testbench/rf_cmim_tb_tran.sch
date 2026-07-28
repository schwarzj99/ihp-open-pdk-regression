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
N 1300 -1060 1300 -1020 {lab=vcapx}
N 1520 -1060 1520 -1020 {lab=vcapm}
N 1520 -1140 1520 -1120 {lab=VDD}
N 1420 -1140 1520 -1140 {lab=VDD}
N 1300 -1140 1300 -1120 {lab=VDD}
N 1420 -1160 1420 -1140 {lab=VDD}
N 1300 -1140 1420 -1140 {lab=VDD}
N 1300 -870 1300 -860 {lab=GND}
N 1520 -870 1520 -860 {lab=GND}
N 1420 -945 1460 -945 {lab=GND}
N 1420 -945 1420 -920 {lab=GND}
N 1200 -945 1240 -945 {lab=GND}
N 1200 -945 1200 -920 {lab=GND}
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
plot vcapx vcapm
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
C {sg13_rf_cmim_2x.sym} 1250 -1040 0 0 {name=x1}
C {isource.sym} 1300 -1090 0 0 {name=I0 value=1m}
C {isource.sym} 1520 -1090 0 0 {name=I1 value=1m}
C {vdd.sym} 980 -840 0 0 {name=l1 lab=VDD}
C {vdd.sym} 1420 -1160 0 0 {name=l3 lab=VDD}
C {devices/gnd.sym} 1300 -860 0 0 {name=l4 lab=GND}
C {devices/gnd.sym} 1520 -860 0 0 {name=l5 lab=GND}
C {lab_wire.sym} 1300 -1040 0 0 {name=p1 sig_type=std_logic lab=vcapx}
C {lab_wire.sym} 1520 -1040 0 0 {name=p2 sig_type=std_logic lab=vcapm}
C {sg13_rf_cmim_m2.sym} 1470 -1040 0 0 {name=x2}
C {devices/gnd.sym} 1420 -920 0 0 {name=l6 lab=GND}
C {devices/gnd.sym} 1200 -920 0 0 {name=l7 lab=GND}
