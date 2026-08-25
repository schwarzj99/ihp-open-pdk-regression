# Extracted substrate taps per circuit

Generated from lvs_sweep/20260803_141940 (deep, taps enabled).
Every tap is ptap1; no ntap1 appears anywhere in the IO pads.
A/P are constant per circuit, so they can be written into a netlist.

NOTE: the net column is the LAYOUT label, which does not always match the
schematic pin name. sg13g2_DCNDiode's tap is labelled 'anode' in the layout
but corresponds to the schematic's 'guard' pin.

| Circuit | Layout net | A | P |
|---|---|---|---|
| sg13g2_Clamp_N15N15D | iovss | A=55.7736p | P=328.08u |
| sg13g2_Clamp_N20N0D | iovss | A=55.7736p | P=328.08u |
| sg13g2_Clamp_N2N2D | iovss | A=55.7736p | P=328.08u |
| sg13g2_Clamp_N43N43D4R | iovss | A=65.6472p | P=386.16u |
| sg13g2_Clamp_N8N8D | iovss | A=55.7736p | P=328.08u |
| sg13g2_Clamp_P15N15D | iovss | A=67.0344p | P=394.32u |
| sg13g2_Clamp_P20N0D | iovss | A=67.0344p | P=394.32u |
| sg13g2_Clamp_P2N2D | iovss | A=67.0344p | P=394.32u |
| sg13g2_Clamp_P8N8D | iovss | A=67.0344p | P=394.32u |
| sg13g2_DCNDiode | anode | A=141.2964p | P=221.76u |
| sg13g2_DCPDiode | guard | A=33.5104p | P=197.12u |
| sg13g2_IOPadAnalog | iovss | A=4273.4p | P=593.62u |
| sg13g2_IOPadAnalog | vss | A=23.85p | P=159.6u |
| sg13g2_IOPadIOVdd | iovss$1 | A=1997.9154p | P=411.58u |
| sg13g2_IOPadIOVdd | vss | A=24p | P=160.6u |
| sg13g2_IOPadIOVss | iovss | A=5379.0466p | P=677.04u |
| sg13g2_IOPadIOVss | vss | A=24p | P=160.6u |
| sg13g2_IOPadIn | iovss$1 | A=5379.0466p | P=677.04u |
| sg13g2_IOPadIn | vss | A=21.981p | P=147.74u |
| sg13g2_IOPadInOut16mA | iovss | A=4313.4p | P=594.62u |
| sg13g2_IOPadInOut16mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadInOut30mA | iovss | A=4319.178p | P=671.66u |
| sg13g2_IOPadInOut30mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadInOut4mA | iovss | A=4319.178p | P=671.66u |
| sg13g2_IOPadInOut4mA | vss | A=21.981p | P=147.74u |
| sg13g2_IOPadOut16mA | iovss | A=4313.4p | P=594.62u |
| sg13g2_IOPadOut16mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadOut30mA | iovss | A=4319.178p | P=671.66u |
| sg13g2_IOPadOut30mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadOut4mA | iovss | A=4319.178p | P=671.66u |
| sg13g2_IOPadOut4mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadTriOut16mA | iovss | A=4313.4p | P=594.62u |
| sg13g2_IOPadTriOut16mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadTriOut30mA | iovss | A=4313.4p | P=594.62u |
| sg13g2_IOPadTriOut30mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadTriOut4mA | iovss | A=4313.4p | P=594.62u |
| sg13g2_IOPadTriOut4mA | vss | A=24p | P=160.6u |
| sg13g2_IOPadVdd | iovss$1 | A=1997.6623p | P=411.58u |
| sg13g2_IOPadVdd | vss | A=24p | P=160.6u |
| sg13g2_IOPadVss | iovss$1 | A=5379.0466p | P=677.04u |
| sg13g2_IOPadVss | vss | A=24p | P=160.6u |
| sg13g2_LevelDown | iovss | A=0.804p | P=5.96u |
| sg13g2_LevelDown | vss | A=2.019p | P=14.06u |
| sg13g2_LevelUp | vss | A=0.9135p | P=6.69u |
| sg13g2_LevelUpInv | vss | A=1.053p | P=7.62u |
| sg13g2_RCClampInverter | iovss | A=69.122p | P=406.6u |
| sg13g2_SecondaryProtection | minus | A=9.0304p | P=53.12u |
| sg13g2_io_inv_x1 | vss | A=0.624p | P=4.76u |
| sg13g2_io_nand2_x1 | vss | A=0.657p | P=4.98u |
| sg13g2_io_nor2_x1 | vss | A=0.657p | P=4.98u |
| sg13g2_io_tie | vss | A=0.6255p | P=4.77u |
