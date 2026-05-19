# Makefile for an Open-Source Analog-Mixed Signal Chip Design Template for the ihp-sg13g2 Open-PDK.
#
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# Johannes Kepler University, Department for Integrated Circuits
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# ========================================================================

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

RUN_TAG = $(shell ls -1 $(LIBRELANE_DIR)/runs 2>/dev/null | tail -n 1)

# Variables
TOP = chip_top

.DEFAULT_GOAL := help

# Cell name for verification targets (default: top-level cell)
# Override with: make <target> CELL=<cellname>
CELL ?= $(TOP)

# PEX mode (1 = C-decoupled, 2 = C-coupled, 3 = full-RC)
# Override with: make <target> EXT_MODE=<1|2|3>
EXT_MODE ?= 1

# Floating-point precision (significant digits) for Xschem's ev function
# Override with: make <target> EV_PRECISION=<digits>
EV_PRECISION ?= 5

# Version for release target
# Override with: make <target> VERSION=<version>
VERSION ?= 1.0.0

# Folder structure
XSCHEM_SCH_DIR  := schematic
LAY_DIR         := gds
NET_SCH_DIR     := netlist/schematic
NET_LAY_DIR     := netlist/layout
NET_PEX_DIR     := netlist/pex
NET_PNL_DIR     := netlist/pnl
NET_NL_DIR      := netlist/nl
NET_SPICE_DIR   := netlist/spice
LVS_RPT_DIR     := verification/lvs
DRC_RPT_DIR     := verification/drc
REPORT_DIR      := verification/reports
LIBRELANE_DIR   := flow/librelane
FLOW_FINAL_DIR  := flow/final


# Help Target
help: ## Show this help message
	@echo 'Usage: make <target> [CELL=<cellname>] [EXT_MODE=<1|2|3>] [EV_PRECISION=<digits>] [WAVEFORM_VIEWER=<gtkwave|surfer>] [VERSION=<version>]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z0-9_.-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ''
	@echo 'CELL defaults to $(TOP). Override to verify subcells.'
	@echo 'EXT_MODE defaults to 3 (full-RC). 1=C-decoupled, 2=C-coupled.'
	@echo 'EV_PRECISION defaults to 5 significant digits for Xschem ev function.'
	@echo 'WAVEFORM_VIEWER defaults to gtkwave. Use surfer to launch Surfer instead.'
	@echo 'VERSION defaults to $(VERSION). Used by the release target.'
.PHONY: help
# ================================================================================================


# Git Submodule Target
init-submodules: ## Initialize and update git submodules (e.g. flow/artistic)
	git -C $(MAKEFILE_DIR) submodule update --init
.PHONY: init-submodules
# ================================================================================================


copy-gds: ## Copy and compress final GDS from the last LibreLane run to layout/ (no logo & filler)
	rm -f $(LAY_DIR)/$(TOP).gds.gz
	mkdir -p $(LAY_DIR)/
	cp -r $(FLOW_FINAL_DIR)/gds/$(TOP).gds $(LAY_DIR)/$(TOP).gds
	gzip $(LAY_DIR)/$(TOP).gds
.PHONY: copy-gds

copy-netlist: ## Copy final spice, pnl and nl netlists from the last LibreLane run to netlist/
	rm -rf $(NET_SPICE_DIR)/
	mkdir -p $(NET_SPICE_DIR)/
	cp -r $(FLOW_FINAL_DIR)/spice/$(TOP).spice $(NET_SPICE_DIR)/$(TOP).spice

	rm -rf $(NET_PNL_DIR)/
	mkdir -p $(NET_PNL_DIR)/
	cp -r $(FLOW_FINAL_DIR)/pnl/$(TOP).pnl.v $(NET_PNL_DIR)/$(TOP).pnl.v

	rm -rf $(NET_NL_DIR)/
	mkdir -p $(NET_NL_DIR)/
	cp -r $(FLOW_FINAL_DIR)/nl/$(TOP).nl.v $(NET_NL_DIR)/$(TOP).nl.v
.PHONY: copy-netlist


# LVS Targets
klayout-lvs-netlist: ## Export CDL schematic netlist from Xschem for KLayout LVS (usage: make klayout-lvs-netlist [CELL=<cellname>] [EV_PRECISION=<digits>])
	mkdir -p $(NET_SCH_DIR)
	xschem -s -r -x -q --rcfile $(XSCHEM_SCH_DIR)/xschemrc --command ' \
		set spiceprefix 1; \
		set lvs_netlist 1; \
		set top_is_subckt 1; \
		set lvs_ignore 0; \
		set ev_precision $(EV_PRECISION); \
		set netlist_dir $(NET_SCH_DIR); \
		xschem set netlist_name [file tail [file rootname [xschem get current_name]]]_klayout.cdl; \
		xschem netlist \
	' $(XSCHEM_SCH_DIR)/$(CELL).sch
.PHONY: klayout-lvs-netlist

klayout-lvs: ## Run KLayout LVS of the CELL cell (usage: make klayout-lvs [CELL=<cellname>])
	$(MAKE) klayout-lvs-netlist CELL=$(CELL)
	mkdir -p $(LVS_RPT_DIR)
	mkdir -p $(NET_LAY_DIR)
	python3 $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/lvs/run_lvs.py \
		--layout=$(LAY_DIR)/$(CELL).gds.gz \
		--netlist=$(NET_SCH_DIR)/$(CELL)_klayout.cdl \
		--topcell=$(CELL) \
		--run_dir=$(LVS_RPT_DIR) \
		--run_mode=deep
	mv $(LVS_RPT_DIR)/$(CELL)_extracted.cir $(NET_LAY_DIR)/$(CELL)_klayout.cir
	sleep 4
.PHONY: klayout-lvs

magic-lvs-netlist: ## Export SPICE schematic netlist from Xschem for Magic + Netgen LVS (usage: make magic-lvs-netlist [CELL=<cellname>] [EV_PRECISION=<digits>])
	mkdir -p $(NET_SCH_DIR)
	xschem -s -r -x -q --rcfile $(XSCHEM_SCH_DIR)/xschemrc --command ' \
		set spiceprefix 1; \
		set lvs_netlist 0; \
		set top_is_subckt 1; \
		set lvs_ignore 1; \
		set ev_precision $(EV_PRECISION); \
		set netlist_dir $(NET_SCH_DIR); \
		xschem set netlist_name [file tail [file rootname [xschem get current_name]]]_magic.spice; \
		xschem netlist \
	' $(XSCHEM_SCH_DIR)/$(CELL).sch
.PHONY: magic-lvs-netlist

magic-lvs: ## Run Magic + Netgen LVS of the CELL cell (usage: make magic-lvs [CELL=<cellname>])
	mkdir -p $(LVS_RPT_DIR)
	mkdir -p $(NET_LAY_DIR)
	$(MAKE) magic-lvs-netlist CELL=$(CELL)
	sak-lvs.sh -d -w $(LVS_RPT_DIR) -s $(NET_SCH_DIR)/$(CELL)_magic.spice -l $(LAY_DIR)/$(CELL).gds.gz -c $(CELL)
# 	Alternative using sak-lvs.sh for netlist export and LVS in one step (replaces magic-lvs-netlist target):
#   sak-lvs.sh -d -w $(LVS_RPT_DIR) -s $(XSCHEM_SCH_DIR)/$(CELL).sch -l $(LAY_DIR)/$(CELL).gds.gz -c $(CELL)
	mv $(LVS_RPT_DIR)/$(CELL).ext.spc $(NET_LAY_DIR)/$(CELL)_magic.ext.spc
	rm -f $(LVS_RPT_DIR)/$(CELL).sch.spc
	rm -f $(LVS_RPT_DIR)/ext_$(CELL).tcl
	rm -f $(LVS_RPT_DIR)/*.ext
	sleep 4
.PHONY: magic-lvs
# ================================================================================================


# DRC Targets
klayout-drc-minimum: ## Run minimum pre-check KLayout DRC of the TOP cell with logo and filler
	mkdir -p $(DRC_RPT_DIR)
	python3 $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/run_drc.py \
		--path=$(LAY_DIR)/$(TOP)_logo_fill.gds.gz \
		--topcell=$(TOP) \
		--run_dir=$(DRC_RPT_DIR) \
		--precheck_drc \
		--mp=32 \
		--no_offgrid \
		--density_thr=32 \
		--no_angle \
		--disable_extra_rules \
		--no_recommended
	sleep 4
.PHONY: klayout-drc-minimum

klayout-drc-regular: ## Run regular KLayout DRC of the TOP cell with logo and filler
	mkdir -p $(DRC_RPT_DIR)
	python3 $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/run_drc.py \
		--path=$(LAY_DIR)/$(TOP)_logo_fill.gds.gz \
		--topcell=$(TOP) \
		--run_dir=$(DRC_RPT_DIR) \
		--mp=32 \
		--density_thr=32
	sleep 4
.PHONY: klayout-drc-regular

klayout-drc: ## Run KLayout DRC of the CELL cell (usage: make klayout-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	python3 $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/run_drc.py \
		--path=$(LAY_DIR)/$(CELL).gds.gz \
		--topcell=$(CELL) \
		--run_dir=$(DRC_RPT_DIR) \
		--no_feol \
		--no_density \
		--disable_extra_rules \
		--mp=32 \
		--density_thr=32
	sleep 4
.PHONY: klayout-drc

magic-drc: ## Run Magic DRC of the CELL cell (usage: make magic-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -m -f "*" -w $(DRC_RPT_DIR) $(LAY_DIR)/$(CELL).gds.gz $(CELL)
	rm -f $(DRC_RPT_DIR)/drc_$(CELL).tcl
	sleep 4
.PHONY: magic-drc
# ================================================================================================


# Verify Targets
klayout-verify: ## Verify CELL cell with KLayout (usage: make klayout-verify [CELL=<cellname>])
	$(MAKE) klayout-lvs CELL=$(CELL)
	$(MAKE) klayout-drc CELL=$(CELL)
.PHONY: klayout-verify

klayout:
	$(MAKE) klayout-verify CELL=$(CELL)
.PHONY: KLayout

magic-verify: ## Verify CELL cell with Magic (usage: make magic-verify [CELL=<cellname>])
	$(MAKE) magic-lvs CELL=$(CELL)
	$(MAKE) magic-drc CELL=$(CELL)
.PHONY: magic-verify

magic:
	$(MAKE) magic-verify CELL=$(CELL)
.PHONY: magic
# ================================================================================================


# Simulate, Build and Verify All Target
all: ## Simulate, build and verify the chip
	$(MAKE) sim-all
	$(MAKE) build-all
	$(MAKE) magic-drc CELL=$(TOP)
	$(MAKE) magic-drc CELL=$(TOP)_logo_fill
#	$(MAKE) klayout-verify
#	$(MAKE) magic-verify
.PHONY: all
# ================================================================================================