# Findings and work-arounds for the ihp-sg13g2 pdk
This document is intended to help designers avoid mistakes that can get frustrating to troubleshoot

## IO pads: all 15 are LVS clean
```2026-08-10:``` every ```sg13g2_IOPad*``` passes LVS, 0 errors and 0 warnings. To rebuild everything from the shipped netlist and GDS and check the result, run this in the container:
```
bash IOPADS/verify.sh
```
It runs the five build steps and then re-checks each pad ```independently``` of the sweep's own tally, requiring the explicit PASS signature plus zero errors ```and``` zero warnings, because ```run_lvs.py``` reports PASS even when it aborted before comparing. Takes about three minutes. ```--quick``` re-checks the newest sweep without rebuilding. It reads only ```sg13g2_io.spi``` and ```sg13g2_io.gds``` and writes only new files; neither shipped file is modified.   
```On a failure``` it prints the ```lvs_report.py``` command that names the offending circuit.   
```To see it green in the GUI:``` open a pad from ```IOPADS/layout/``` in KLayout, open ```IOPADS/klayout_lvs/iopad_lvs.lvs``` in the Macro IDE and press Run. It picks the matching netlist from the open cell's name, so the same script serves all 15 pads. All 15 verified green.

## run_lvs.py reports PASS when it never compared (do not grep the log)
```run_lvs.py``` prints ```Status | PASS``` even when the run aborted before the comparison, alongside ```Errors | 1``` and ```Outcome: Comparison mode: completed (no explicit PASS/FAIL signature found)```. Grepping the log for PASS therefore reports success for runs that did nothing.   
```Ask the .lvsdb instead.``` It is KLayout's own record of what it compared. ```IOPADS/lvs_check.py``` does this and returns a real exit code: it requires that an ```.lvsdb``` exists, that it carries a cross-reference, that the ```schematic``` netlist is non-empty, and that every circuit pair matched including the expected top cell.   
```It also names the cause.``` Pointed at the old pre-fix runs it reports "the schematic netlist is empty, so it was never successfully read", which is exactly the root cause and is invisible in the log.

## implicit_nets joins same-named nets only, and it is doing real work
The list is split on commas and each entry becomes its ```own``` ```connect_implicit``` call:
```
nets_to_connect.each { |net_pattern| connect_implicit(net_pattern) }
```
So ```"iovss,iovdd,vss,vdd,..."``` is seven independent rules. It never joins one name to a ```different``` name: ```iovss``` and ```vdd``` cannot be shorted by it. ```sg13g2_IOPadVdd``` proves this, passing with ```iovss``` and ```vss``` still separate pins carrying separate taps.   
```But it is not cosmetic.``` In ```sg13g2_IOPadAnalog``` there are genuinely ```two``` nets labelled ```iovdd```, at different heights, connected to different things:

| net | y (um) | x (um) | connects to |
|---|---|---|---|
| ```iovdd``` | 52.46 - 91.50 | 0.00 - 80.00 | ```Clamp_P20N0D:iovdd```, ```DCPDiode:cathode``` |
| ```iovdd``` | 93.50 - 149.27 | ```-0.62 - 80.62``` | ```SecondaryProtection:plus``` |

They are 2um apart and never touch inside the pad. Only the upper one carries the ```+-0.62um``` overhang that abuts the neighbouring pad; the lower one stops exactly on the 80um pitch. So they are two rails running the length of the ring, and ```connect_implicit('iovdd')``` is what makes LVS treat them as one.   
```This cannot be verified from a single pad.``` Whether the two rails really are one node depends on what joins them in the assembled ring (a corner cell, a strap, or off-chip), and ```sg13g2_io.gds contains no assembled ring``` - there is no ```sg13g2_Gallery``` cell in it, only the individual pads. Treat the passing per-pad result as conditional on that assumption until a full ring is LVS'd.

## Why the pads pass in deep mode but not flat
In flat mode the cell hierarchy is gone, so labels from the sub-cells land on the same physical nets as the pad-level ones and the extractor gives them ```composite``` names:
```
anode|cathode|pad          anode|guard|iovss|minus          cathode|iovdd
```
```connect_implicit``` matches against the net ```name```, and the pattern ```iovdd``` no longer matches a net now called ```cathode,iovdd```. Every implicit rule silently stops applying, so the joins the pads depend on disappear and the comparison fails with ```iovdd,plus vs (none)```. Setting a different list does not help; flat fails with the full list, a reduced list, and no list at all.   
```Second hazard in flat:``` entries like ```anode``` and ```cathode``` are only safe while hierarchy keeps them inside their own cell. Flattened, ```connect_implicit('anode')``` would join ```DCNDiode```'s substrate-side anode to ```DCPDiode```'s pad-side anode, shorting the substrate to the pad.   
```Use deep mode.``` Per-circuit scope is what keeps both the names simple and the rules local.

## KLayout keeps Ruby globals alive between macro runs
The GUI's Ruby interpreter persists globals across runs of a ```.lvs``` or ```.drc``` macro. A macro written with ```||=``` therefore reuses whatever the ```previous``` run left behind:
```
$schematic ||= ...   # silently keeps last run's value, whatever you now have open
```
Run such a macro once against the wrong cell and every later run inherits the stale path, no matter which layout is open. The symptom is an error naming a file you never asked for, often under KLayout's own working directory ```/headless/.klayout```.   
```Rule:``` in a GUI macro, ```assign``` per-run values with ```=```, never ```||=```, and clear any switch the deck might read. Keep explicit user overrides under separate names that are read once.

## The LVS deck throws away its default report path
```sg13g2.lvs``` computes a default ```.lvsdb``` location and then does not use it:
```
report_path = layout_dir.join("#{source.cell_name}.lvsdb").to_s   # local
report_lvs($report_path)                                          # global, never set -> nil
```
So when ```$report``` is not passed, nothing is written to disk despite the log announcing "output at default location". In the GUI this happens to do the right thing (results land in the Netlist Browser); in batch the results are simply lost.   
```Workaround:``` always pass ```$report``` / ```--run_dir``` explicitly.
```The sections below record every defect found getting there.``` Most are upstream PDK bugs.
##  Schottky Diode
Needs the database units at 1nm for correct extraction/LVS pass.
## Taps/psub(sub!)
When working with devices that have a built-in guardring the use of the digisub layer is mandatory.   
```Example 1:``` The RF NMOS has a built-in guardring so the bulk connection of the pcell already corresponds to the Metal1 contact of the guardring. This, without the use of the digisub layer, causes the psub (sub!) net to be shorted to VSS.   
```Example 2:``` Schottky Diode has a TIE connection that already represents the Metal1 connection of the ptap and thus, without the use of the digisub layer, causes the psub (sub!) net to be shorted to VSS.   
```Workaround:``` Draw a digisub rectangle over the affected active area.   
```Known affected devices:```rf_cmim, rf_lv_nmos, rf_hv_nmos and schottky

## Vias
Vias are only drc clean when 3x1 or 2x2 or greater. The 2x1 are just short of being drc clean and the 1x1 are way off.

## IO pads: parallel devices are only tied together by the parent cell
The library cells inside the IO pads tie their parallel devices together with metal drawn in the ```parent``` cell, never inside the cell itself. Extraction therefore pushes every finger out as its own pin, while the shipped ```sg13g2_io``` netlist models the net as internal to the cell. The two can never match.   
```Example:``` ```sg13g2_Clamp_N43N43D4R``` extracts with 25 pins: ```gate```, ```iovss```, the bulk, and then ```pad```, ```pad$1``` ... ```pad$21```, one per NMOS finger. The parent ```sg13g2_IOPadVdd``` maps all 22 of them onto ```vdd```. The schematic declares 4 pins with a single internal ```pad```.   
```Also affected:``` ```sg13g2_DCNDiode```/```sg13g2_DCPDiode``` (two parallel ```dantenna```/```dpantenna``` fingers, giving ```cathode$1```/```anode$1```) and the pad-level supplies (```iovss$1```, ```iovdd$1```).   
```Note:``` the layout is not broken. Those devices really are connected. Only the level at which the connection happens disagrees between GDS and SPICE.   
```Workaround:``` flatten the affected cells in both netlists before comparison, see the ```--flatten_cells``` patch in ```lvs_patches/```.

## IO pads: device granularity differs between layout and netlist
Independently of the above, the layout merges parallel fingers into single wide devices while the netlist keeps them as individual instances. For ```sg13g2_IOPadVdd``` in deep mode: ```Clamp_N43N43D4R``` extracts 24 devices against 175 in the schematic, ```RCClampInverter``` 4 against 78, and ```RCClampResistor``` (26 devices) does not survive extraction at all.   
```Note:``` ```--combine_devices``` alone does not fix this, because the pin splitting above still blocks the compare.

## Per-pad LVS of the IO pads
Cutting a single pad out of ```sg13g2_io.gds``` and running LVS against the shipped netlist fails for every pad, for the two reasons above. Things that do ```not``` help:   
```Flat vs flat:``` the layout collapses further (the 22 clamp fingers merge geometrically into one ```W=756.8u``` device) so the mismatch gets worse, not better.   
```Preserving hierarchy on extraction:``` necessary, but not sufficient on its own. Drag out pads with ```SaveLayoutOptions.add_cell```, which takes the cell plus its whole child tree; dragging out a flattened cell additionally destroys the subcircuit correspondence.   
```Watch out:``` ```sg13g2_IOPadAnalog.gds``` cut out by hand had its top cell renamed to ```sg13g2_IoPadAnalog``` (lowercase o). With strict port mode there is then no schematic circuit to bind to and the failure looks like an ordinary mismatch.   
```Best known invocation:``` with the ```--flatten_cells``` patch applied:
```
run_lvs.py --combine_devices \
           --implicit_nets='iovss,iovdd,vss,vdd' \
           --flatten_cells='sg13g2_DCNDiode,sg13g2_DCPDiode,sg13g2_Clamp_*,sg13g2_RCClamp*,sg13g2_GuardRing_*'
```
This reduces ```sg13g2_IOPadVdd``` from 3 circuits with a 25-pin clamp and 22 split ```pad``` pins down to a single circuit with 4 devices and 3 pins, and the clamp's 172 schematic fingers of ```w=4.4um``` combine to exactly the ```W=756.8u``` the layout extracts. ```--implicit_nets``` is what resolves the top-level ```iovss```/```iovss$1``` split, which flattening cannot reach because the top cell itself cannot be flattened.   
```Still does not pass.``` See the substrate blocker below.

## sg13g2_io.spi is unreadable by the KLayout LVS deck (root cause)
The shipped IO netlist writes every device as a ```subcircuit call``` instead of a SPICE element:
```
Xdcdiode[0] anode cathode dantenna l=1.26um w=27.78um
```
KLayout reads that as a call to a circuit literally named ```DANTENNA(L=1.26U,W=27.78U)```. The custom reader only intercepts elements ```M C R Q L D``` (see ```globals.lvs```: ```CUSTOM_READER```), so ```X``` falls through to the default subcircuit path. The result is a schematic netlist containing ```zero devices```: every circuit is empty.   
```This is why every IO pad LVS run failed.``` The extracted side was fine and the structural analysis below is still valid, but there was never anything on the schematic side to compare against.   
```Symptom to recognise:``` in the ```.lvsdb```, ```xref.netlist_b()``` is empty and every circuit pair reports its schematic counterpart as ```(none)```. Check with ```IOPADS/lvs_report.py```.   
```Workaround:``` rewrite the devices with real element prefixes, ```D``` for diodes, ```M``` for MOS, ```R``` for resistors and taps. Verify with:
```
python3 -c "import pya; nl=pya.Netlist(); nl.read('x.spi', pya.NetlistSpiceReader()); \
  [print(c.name, [d.device_class().name for d in c.each_device()]) for c in nl.each_circuit()]"
```
If the device lists come back empty, the netlist will never match anything.

## sg13g2_RCClampResistor is missing its PolyRes marker (layout bug)
Running LVS with ```--topcell=sg13g2_RCClampResistor``` produces an ```empty``` extracted netlist: none of its 26 ```rppd``` fingers extract, while the schematic declares 26 devices. This is a ```layout``` bug, not a netlist one.   
```Cause:``` the cell has GatPoly, contacts, salblock (28/0), psd (14/0) and extblock (111/0), but no ```PolyRes``` (128/0) marker. ```rppd``` extraction needs it:
```
polyres_mk = polyres_drw.and(extblock_drw).interacting(gatpoly).not(polyres_exclude)
rppd_res   = polyres_mk.and(psd_drw).and(salblock_drw).not(nsd_block).not(nsd_drw)
```
```Scope:``` PolyRes exists in only ```two``` cells in the whole IO library, ```sg13g2_Clamp_N20N0D``` and ```sg13g2_Clamp_P20N0D```, one shape each. Theirs is the only ```rppd``` that ever extracted anywhere in the pads.   
```Red herring:``` the cell has 26 shapes on 63/0, one per finger, which looks like a per-device marker. They are ```rppd r=7.938k``` annotation texts and play no part in ```rppd``` extraction, which keys off 128/0 only. Do not conclude from this that 63/0 is inert, though: it is the tap label layer, see below.   
```Fix:``` add one PolyRes shape ```per finger```, as ```salblock AND (GatPoly MINUS Activ)```. Two traps here. A single rectangle spanning all 26 (the salblock's own shape) is ```not``` enough: it derives one core region with 52 ports, which the 2-terminal extractor cannot use, and the cell still extracts to nothing. And the ```MINUS Activ``` matters because salblock is also drawn over transistor gates for silicide blocking, so a plain ```salblock AND GatPoly``` can invent a resistor on a gate. Script: ```IOPADS/fix_polyres_marker.py```, which reads the netlist to decide which cells to touch and warns if the derived marker count does not equal the declared ```rppd``` count.   
```Result:``` the cell extracts as one series-combined ```rppd w=1u l=520u``` (26 x 20u) and passes LVS against the converted netlist.

## Audit: which cells declare rppd
Only four subckts in the whole IO netlist declare ```rppd```, and two of them were missing the marker:

| Cell | rppd declared | PolyRes 128/0 | |
|---|---|---|---|
| ```sg13g2_Clamp_N20N0D``` | 1 | 1 | ok |
| ```sg13g2_Clamp_P20N0D``` | 1 | 1 | ok |
| ```sg13g2_RCClampResistor``` | 26 | 0 | fixed, 26 markers added |
| ```sg13g2_SecondaryProtection``` | 1 | 0 | fixed, 1 marker added |

Fixed layout is written to ```layout/sg13g2_io_polyres.gds```; the input GDS is never modified. ```sg13g2_SecondaryProtection``` now extracts its ```R$3 pad core \$1 rppd w=1u l=2u```, matching the schematic.

## First IO cell to pass LVS
```sg13g2_DCNDiode``` passes with 0 errors and 0 warnings. See ```IOPADS/cell_tests/sg13g2_DCNDiode.spi```.
```
run_lvs.py --topcell=sg13g2_DCNDiode --run_mode=deep --implicit_nets='cathode' --combine_devices
```
It needed three changes: element prefixes (above), the substrate tap written in explicitly, and recognising that the shipped ```anode``` pin ```is``` the p-substrate node (```dantenna``` is n-diff to psub, so the diode anodes and the tap's ```WELL``` terminal are one net). The layout's ```anode``` ```label``` sits on the guard ring tie, which is a different net entirely.   
```--implicit_nets``` joins the cathode fingers, ```--combine_devices``` merges the two parallel ```dantenna``` into the ```m=2``` device the extractor produces.

## sg13g2_IOPadIOVss has a shorted DCNDiode upstream
In the ```shipped``` netlist, ```sg13g2_io.spice``` line 745:
```
Xdcndiode iovss iovss iovdd sg13g2_DCNDiode
```
```anode``` and ```cathode``` are both ```iovss```, so both ```dantenna``` fingers are shorted out and the instance contributes nothing. This is in the pristine PDK file, not a local edit. The neighbouring ```sg13g2_IOPadVss``` (line 169) is correct: ```iovss vss iovdd```.   
```Why it happens:``` the ```anode``` pin of ```sg13g2_DCNDiode``` is the ```p-substrate``` node, not a signal anode (```dantenna``` is n-diff to psub). The netlist models the substrate by tying that pin to whichever ground rail is nearby, so on a pad where the cathode is already that same rail the device collapses.   
```Fix:``` give the substrate its own net rather than aliasing it to a rail. The layout already has it that way, held apart from ```iovss``` and ```vss``` by ```ptap1``` devices, so ```psub -> pad``` is a real diode there. Any rename of ground rails in these subckts risks silently collapsing a diode, so check ```anode != cathode``` after editing.

## sg13g2_LevelDown's netlist does not describe its layout
The layout holds ```8``` transistors, the shipped netlist ```4```:

| | layout | netlist |
|---|---|---|
| ```sg13_hv_nmos``` | 2 x W=2.65u, 2 x W=1.3u | 1 x W=2.65u |
| ```sg13_hv_pmos``` | 2 x W=4.6u | 1 x W=```4.65u``` |
| ```sg13_lv_nmos/pmos``` | 1 each | 1 each |

The layout is pad -> secondary protection -> two IO-domain inverters -> a stack -> core inverter. The netlist models one hv inverter feeding one lv inverter, and even its surviving pmos width is wrong. Rewriting it means reverse-engineering the cell from the layout.   
```Blocks:``` ```IOPadIn``` and all three ```IOPadInOut*```.

## Pad bodies wire sub-blocks to vss where the layout has iovss
In ```sg13g2_IOPadVdd```, ```sg13g2_IOPadIOVdd``` and ```sg13g2_IOPadIOVss``` the clamp, RC inverter, guard ring and protection diodes are wired to ```vss```. The layout puts them on ```iovss```, alongside the large substrate tap; ```vss``` carries only the small tap.   
```Tell:``` the LVS cross-reference reports exactly two mismatching nets, ```iovss vs VSS``` and ```vss vs IOVSS```, with every subcircuit matching. That pattern means a rail swap, not a topology error.   
```Fix:``` move those instances to ```iovss``` and leave the taps alone. All three pads pass afterwards.

## Clamp gate antenna diodes are the wrong size in the shipped netlist
All seven ```sg13g2_Clamp_*``` cells ship with ```XDGATE ... l=0.64um w=0.48um```, which matches ```none``` of them. Sizes read back from the layout:

| Clamp | shipped | layout |
|---|---|---|
| ```N43N43D4R```, ```P2N2D```, ```P8N8D``` | 0.64 x 0.48 | ```0.48 x 0.48``` (```A=0.2304p P=1.92u```) |
| ```N2N2D```, ```N8N8D```, ```N15N15D```, ```P15N15D``` | 0.64 x 0.48 | ```0.78 x 0.78``` (```A=0.6084p P=3.12u```) |

```Note:``` ```A = l*w``` and ```P = 2*(l+w)```, so a wrong ```l```/```w``` is a device parameter mismatch, not a topology error, and shows up as an otherwise inexplicable single-device failure.

## Not every rppd body terminal is the substrate
The third terminal of an ```rppd``` is the region the poly sits over. For the ```P```-type clamps that is the ```nwell```, not psub: ```sg13g2_Clamp_P20N0D``` extracts as ```R iovdd \$6 iovdd rppd```. The shipped netlist already has this right.   
```Trap:``` a blanket "point every rppd body at the substrate" rewrite invents a connection that is not in the layout and breaks exactly the P-type clamps. Only rewrite where the netlist had aliased it to a ground rail (```iovss```/```vss```).

## dantenna anodes are always the substrate
```dantenna``` is n-diff to p-substrate, so its anode is the psub node and never a rail. ```dpantenna``` is p-diff to nwell and needs no such treatment. Applies to the ```XDGATE``` diodes in the clamps and to ```sg13g2_SecondaryProtection``` as well as to ```sg13g2_DCNDiode```.

## sg13g2_IOPadAnalog has a pin-count mismatch after local edits
```netlist/sg13g2_io.spi``` declares ```.subckt sg13g2_IOPadAnalog iovdd iovss pad padbare padres vdd vss``` (7 pins) while ```sg13g2_Gallery``` still calls it with 6 nets, and ```padbare``` appears nowhere else in the file. KLayout refuses to read the whole netlist:
```
Pin count mismatch between circuit definition and circuit call: 7 expected, got 6
```
The shipped ```sg13g2_io.spice``` is clean; this arrived with a local edit that added the pin without wiring it or updating the caller.   
```Consequence:``` any tool reading the ```complete``` file fails. Per-pad split netlists hide it because they exclude the Gallery.   
```Lint:``` compare each ```X``` call's net count against its ```.subckt``` pin count before trusting a netlist.

## Cell-level LVS cannot validate every cell standalone
```sg13g2_io_inv_x1``` extracts standalone with pins ```i|vdd nq vss```: the input and the supply merge into one net, because the cell's input routing is completed by metal in the parent. In a pad context the same cell extracts cleanly as ```i vss nq vdd \$5``` and matches.   
```So:``` a standalone cell failure is not proof of a netlist error. Check the cell inside a parent before chasing it.

## Taps are device-or-connectivity depending on a text label
Whether a well/substrate tie becomes an ```extracted device``` or plain ```connectivity``` is decided by a text label on layer 63/0 (```text_drw = labels(63, 0)```):
```
ntap1_lbl = text_drw.texts("well")     # case-insensitive
ptap1_lbl = text_drw.texts("sub!")
ntap1_mk  = nwell_drw.interacting(ntap1_lbl)
ntap      = nactiv.and(nwell_drw).not(ntap1_mk)...   # the complement
connect(nwell_drw, ntap)
```
```Labelled``` ties become ```ntap1```/```ptap1``` devices, which the schematic must then declare. ```Unlabelled``` ties are just connectivity: ```connect(nwell_drw, ntap)``` ties the well straight to its contact and no device appears on either side.   
```In the IO library:``` 64 ```sub!``` labels and ```zero``` ```well``` labels. So every psub ring extracts a ```ptap1``` device, and no ```ntap1``` exists anywhere.   
```This explains the two-rings-one-tap puzzle.``` ```sg13g2_Clamp_N43N43D4R``` really does contain two guard rings, an outer nwell ring with an inner psub ring around the MOSFETs. Only the psub one is labelled, so only it becomes a device. The empty ```sg13g2_GuardRing_N*``` subckt in the netlist is therefore ```correct``` and needs nothing added; only the ```P``` rings need a ```ptap1```.   
```Not a bug:``` this is a coherent choice by the library, not an oversight. Do not "fix" it by adding ```well``` labels unless you also add the matching ```ntap1``` devices to the netlist.

## IO pads: the GuardRing subckts do not exist in the layout
```sg13g2_io.gds``` contains 47 cells and not one of them is a ```sg13g2_GuardRing_*```. The guard rings exist only in the netlist, as empty subckts. Their geometry is drawn directly inside the parent cells, which is why the extracted ```ptap1``` devices show up in the parent circuits (```sg13g2_DCNDiode```, ```sg13g2_Clamp_*```, the pad tops) rather than in guard ring circuits of their own.   
```Consequence:``` the guard ring instance to tap device mapping is not 1:1 and cannot be reconstructed from the names. ```sg13g2_Clamp_N43N43D4R``` instantiates two guard rings and yields one tap; ```sg13g2_DCNDiode``` instantiates an ```N```-named ring and yields a ```ptap1```. Attach taps to the circuit the extraction puts them in, not to the guard ring subckts.   
```Also:``` the layout net labels do not always match the schematic pin names. ```sg13g2_DCNDiode```'s tap sits on a net labelled ```anode``` in the layout but corresponds to the schematic's ```guard``` pin, while the schematic's ```anode``` is unlabelled in the layout.   
```Data:``` ```IOPADS/tap_inventory.md``` lists every extracted tap with its circuit and its ```A```/```P```. Every tap is ```ptap1```; no ```ntap1``` appears anywhere in the IO pads. The values are constant per circuit, so they can be written into a netlist.   
```.GLOBAL works:``` KLayout's SPICE reader honours ```.GLOBAL sub``` and auto-adds the pin to every circuit that uses it, so a substrate net does not have to be threaded through by hand.

## IO pads: guard rings are empty subckts but extract as tap devices
The remaining blocker for per-pad LVS. The netlist models every ```sg13g2_GuardRing_*``` as an empty subckt, while the layout extracts ```ptap1```/```ntap1``` devices for them, so the layout always carries devices the schematic does not have.   
```--disable_tap_extraction``` removes them, but then nothing separates the rails that contact the substrate: ```iovss``` and ```vss``` collapse into a single ```iovss|vss``` net and the extracted top cell drops to 2 pins. With taps enabled they stay distinct, separated by the ```ptap1``` devices.   
```Note:``` this is the same underlying ```psub```/```sub!``` modelling gap as the Taps section above. Fixing per-pad LVS properly means either giving the guard ring subckts their tap devices in the netlist, or teaching the deck to treat guard ring taps as connectivity rather than devices.

## run_lvs.py reports PASS when it never compared
```run_lvs.py``` prints ```Status | PASS``` even when the run aborted before the comparison, alongside ```Errors | 1``` and ```Outcome: Comparison mode: completed (no explicit PASS/FAIL signature found)```.   
```Workaround:``` when scripting the runner, treat a run as passing only if the exit code is 0 ```and``` the error count is 0 ```and``` that "no explicit PASS/FAIL signature" string is absent.

## $PDK is not a safe default in the container
The IIC-OSIC-TOOLS container exports ```PDK``` as a bare name (```ihp-sg13g2```) and ```PDK_ROOT``` separately (```/foss/pdks```). Using ```$PDK``` alone resolves as a ```relative``` path against the current directory, which silently picks up any same-named checkout under the cwd. ```$PDK``` also changes when the PDK is switched mid-session, so a script that derives its rule deck from it can end up checking an sg13g2 design against another PDK entirely.   
```Workaround:``` hard-code the deck path in regression scripts rather than inheriting it.

## The IO ring bus bars are parallel bars, tied together inside the pads
Each rail is drawn as several parallel bars, not one: ```iovdd``` has 2 (```y``` 66.00-91.50 and 93.50-148.65), ```iovss``` has 3 (```y``` 6.00-32.50, 34.50-60.00, 65.00-140.17). ```sg13g2_Corner``` and every ```sg13g2_Filler*``` contain no via layers at all (no 19/0, 29/0, 49/0, 66/0, 125/0, 133/0), so they are pure pass-through metal and never join anything. The stitching is done by the pads:

| cell | ties iovdd A-B | ties iovss A-B-C |
|---|---|---|
| ```sg13g2_IOPadIOVss``` | yes | all three |
| ```sg13g2_IOPadIOVdd``` | yes | none |
| ```sg13g2_IOPadIn``` | yes | A-B |
| ```sg13g2_IOPadVss``` | yes | A-B |
| ```sg13g2_IOPadAnalog```, all ```Out```/```TriOut```/```InOut``` | none | A-C |
| ```sg13g2_IOPadVdd``` | none | none |
| ```sg13g2_Corner```, ```sg13g2_Filler*``` | none | none |

```Verified:``` a row assembled from corner + Analog + In + Out30mA + IOVdd + IOVss + Vdd + Vss + InOut16mA + filler + corner, flattened and extracted, gives ```one``` ```iovdd``` net and ```one``` ```iovss``` net spanning the whole row on all seven metal levels. A row with no supply pad at all still collapses to one of each, because ```IOPadIn``` ties ```iovdd``` A-B and the others tie ```iovss``` A-C.   
```Consequence:``` ```--implicit_nets``` is not hiding a disconnect. On an isolated pad it reproduces what abutment produces in a real ring. The only arrangement where it would be wrong is a row of nothing but ```sg13g2_IOPadVdd``` and fillers.

## The installed PDK's sg13g2_io.spi is stale and mis-ordered
Three generations of this netlist exist in the container and they are not interchangeable:

| file | subckts | ```ptap1``` | pin order vs xschem symbols |
|---|---|---|---|
| ```/foss/pdks/ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi``` | 45 | 65 | wrong on ```all 15``` pads |
| ```/foss/designs/IHP-Open-PDK/.../sg13g2_io.spi``` (```d4aa0fc2```, 2025-07-07) | 60 | 0 | correct on all 15 |
| ```IOPADS/netlist/sg13g2_io.spi``` (local, 2024-05-27, edited) | 60 | 0 | correct on 8, wrong on 7 |

The seven wrong ones in the local copy are exactly the pads that were edited by hand: ```Analog```, ```IOVdd```, ```IOVss```, ```In```, ```InOut30mA```, ```Out30mA```, ```Vdd```, ```Vss```.   
```Also in the installed PDK:``` 13 calls pass ```m=1``` to ```dantenna```/```dpantenna```, which take 5 formal parameters and not ```m```. ngspice aborts with ```Mismatch: 5 formal but 6 actual params``` before any analysis runs.

## The IO pad testbench does not work against the installed PDK
```libs.tech/xschem/sg13g2_tests/sg13g2_IOPad_tb.sch``` includes ```$PDK_ROOT/$PDK/libs.ref/sg13g2_io/spice/sg13g2_io.spi```. With the installed PDK it aborts on the ```m=1``` bug above; strip ```m=1``` and it runs but every pad is miswired, because the symbol pin order does not match the subckt pin order. Operating point, ```pad1``` driven to 1.5 V:

| node | installed PDK | current upstream | expected |
|---|---|---|---|
| ```padres1``` | 3.07 V | 1.49 V | ~1.49 V (```pad``` through the ~800 ohm ```rppd``` into 100k) |
| ```p2c1``` | 2.12 V | 1.54 V | core-level logic high |
| ```c2p1_pad``` | 3.08 V | 3.25 V | ```iovdd``` level |

```Fix:``` point the include at the current upstream netlist. Nothing in ```IOPADS/``` writes to ```/foss/pdks```, so this is independent of the LVS work.

## The LVS netlists are LVS-only and will never simulate
```IOPADS/netlist/sg13g2_io_devices.spi``` and ```sg13g2_io_sub.spi``` are built for KLayout's SPICE reader, which needs real element prefixes. ngspice needs the opposite: ```sg13_hv_nmos``` is a subcircuit, so ```M... sg13_hv_nmos``` fails with ```could not find a valid modelname```. ```ptap1``` written as an ```R``` and ```.GLOBAL sub``` are also LVS-only constructs.   
```Note:``` the ```input``` to that pipeline does not simulate either. ```IOPADS/netlist/sg13g2_io.spi``` fails with ```Too few parameters for subcircuit sg13g2_IOPadAnalog```, because the local edit gave that pad a seventh pin (```padbare```) the symbol does not have. That failure predates any of this work.

## The upstream netlist reaches 15/15 with three generic fixes
Running the same pipeline on the current upstream netlist instead of the local copy gives 9/15 straight away, and 15/15 after three additions to ```add_taps.py```. None of the local per-pad wiring corrections are needed: ```pad body nets fixed 0```, ```stray pins dropped 0```, because upstream never had the ```vss```/```iovss``` rename, the ```iovdd1``` scaffolding or the ```padbare``` pin.

| upstream defect | evidence | fix |
|---|---|---|
| all 7 clamp gate antenna diodes are ```l=0.64um w=0.48um``` (```A=0.3072p P=2.24u```) | layout has ```A=0.6084p P=3.12u``` for the ```N*``` clamps and ```A=0.2304p P=1.92u``` for ```N43N43D4R``` | ```GATE_DIODE_FIX``` extended from 4 to 7 entries |
| ```sg13g2_Clamp_P20N0D```'s off-resistor body is ```sub!``` | the resistor sits in an nwell; layout extracts ```R iovdd $6 iovdd rppd``` | ```RPPD_WELL``` |
| ```sg13g2_RCClampInverter```'s ground pin is named ```ground```, the layout labels it ```iovss``` | the tap hangs off a floating net, ```TAP0``` unmatched, ```net (none) vs IOVSS``` | ```TIE_ALIAS```, applied only when the layout name is not a pin and the alias is |

All three are no-ops on the local netlist, which still verifies 15/15. Upstream also spells the substrate ```sub!``` where ```add_taps.py``` declares ```.GLOBAL sub```; left alone those are two separate nets, so ```verify_upstream.sh``` renames it on the way in.   
```Note:``` the local copy had 3 of the 7 gate diodes corrected by hand and upstream does not, so on this point the edited local file was ```ahead``` of upstream.   
```Reproduce:``` ```bash IOPADS/verify_upstream.sh```

## Splitting the netlist per pad round-trips exactly
Recombining ```IOPADS/netlist/pads_sub/*.spi``` yields 52 subckt definitions with ```zero``` disagreements between pad files - every cell shared by several pads is defined identically in each. The 8 definitions present in the monolithic netlist but absent from the recombination are ```sg13g2_Corner```, the six ```sg13g2_Filler*``` and ```sg13g2_Gallery```, none of which any pad instantiates.   
```Proven end to end:``` splitting the ```upstream``` netlist (before ```convert_netlist.py```, so device calls are still subcircuit calls) and recombining it gives a netlist that drops straight into ```sg13g2_IOPad_tb``` and reproduces the monolithic operating point on all ```270``` nodes, bit for bit. So the split loses nothing; the pipeline's later stages are what make the result LVS-only.   
```Do not simulate the LVS form:``` splitting ```pads_sub``` and recombining that gives ```m.x1.xnclamp.mclamp_g0 ... could not find a valid modelname```, because ```sg13_hv_nmos``` is a subcircuit and the LVS form has rewritten the call as an ```M``` element. ```recombine_pads.py``` labels which of the two forms it produced in the file header.

  ```
  python3 split_pads.py     <upstream>.spi netlist/pads_sim
  python3 recombine_pads.py netlist/pads_sim netlist/sg13g2_io_sim_recombined.spi <upstream>.spi
  ```