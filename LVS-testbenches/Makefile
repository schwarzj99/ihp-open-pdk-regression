# Makefile for an Open-Source Analog-Mixed Signal Chip Design Template for the ihp-sg13g2 Open-PDK.
#
# SPDX-FileCopyrightText: 2026 Simon Dorrer and Harald Pretl
# Johannes Kepler University, Department for Integrated Circuits
# SPDX-License-Identifier: Apache-2.0 WITH SHL-2.1
# ========================================================================

MAKEFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

RUN_TAG = $(shell ls -1 $(LIBRELANE_DIR)/runs 2>/dev/null | tail -n 1)


.DEFAULT_GOAL := help

# Cell name for verification targets (default: top-level cell)
# Override with: make <target> CELL=<cellname>
CELL ?= sg13_lv_nmos_tap

# Floating-point precision (significant digits) for Xschem's ev function
# Override with: make <target> EV_PRECISION=<digits>
EV_PRECISION ?= 5

# Folder structure
XSCHEM_SCH_DIR  := schematic
LAY_DIR         := gds
NET_SCH_DIR     := netlist/schematic
NET_LAY_DIR     := netlist/layout
LVS_RPT_DIR     := verification/lvs
DRC_RPT_DIR     := verification/drc

# Auto-discovered cells from all .gds files in $(LAY_DIR)/
GDS_CELLS := $(patsubst $(LAY_DIR)/%.gds,%,$(wildcard $(LAY_DIR)/*.gds))


# Help Target
help: ## Show this help message
	@echo 'Usage: make <target> [CELL=<cellname>] [EV_PRECISION=<digits>] [VERSION=<version>]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z0-9_.-]+:.*## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-20s %s\n", $$1, $$2}'
	@echo ''
	@echo 'CELL defaults to $(TOP). Override to verify subcells.'
	@echo 'EV_PRECISION defaults to 5 significant digits for Xschem ev function.'
	@echo 'VERSION defaults to $(VERSION). Used by the release target.'
.PHONY: help
# ================================================================================================

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
		--layout=$(LAY_DIR)/$(CELL).gds \
		--netlist=$(NET_SCH_DIR)/$(CELL)_klayout.cdl \
		--topcell=$(CELL) \
		--run_dir=$(LVS_RPT_DIR) \
		--run_mode=deep \
		; echo $$? > $(LVS_RPT_DIR)/.$(CELL)_lvs_rc
	-mv $(LVS_RPT_DIR)/$(CELL)_extracted.cir $(NET_LAY_DIR)/$(CELL)_klayout.cir
	@rc=`cat $(LVS_RPT_DIR)/.$(CELL)_lvs_rc`; \
	if [ "$$rc" -ne 0 ]; then exit $$rc; fi; \
	grep -q "Congratulations! Netlists match" $(LVS_RPT_DIR)/$(CELL).log 2>/dev/null || exit 1
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
#	sak-lvs.sh -d -w $(LVS_RPT_DIR) -s $(NET_SCH_DIR)/$(CELL)_magic.spice -l $(LAY_DIR)/$(CELL).gds -c $(CELL)
# 	Alternative using sak-lvs.sh for netlist export and LVS in one step (replaces magic-lvs-netlist target):
	sak-lvs.sh -d -w $(LVS_RPT_DIR) -s $(XSCHEM_SCH_DIR)/$(CELL).sch -l $(LAY_DIR)/$(CELL).gds -c $(CELL)
	mv $(LVS_RPT_DIR)/$(CELL).ext.spc $(NET_LAY_DIR)/$(CELL)_magic.ext.spc
#	rm -f $(LVS_RPT_DIR)/$(CELL).sch.spc
#	rm -f $(LVS_RPT_DIR)/ext_$(CELL).tcl
#	rm -f $(LVS_RPT_DIR)/*.ext
.PHONY: magic-lvs

lvs: ## Run KLayout and Magic LVS of the CELL cell (usage: make lvs [CELL=<cellname>])
	$(MAKE) klayout-lvs CELL=$(CELL)
	$(MAKE) magic-lvs CELL=$(CELL)
.PHONY: lvs

klayout-lvs-regression: ## Run klayout-lvs for every .gds in $(LAY_DIR)/
	@failed=""; \
	for cell in $(GDS_CELLS); do \
		echo "[REGRESSION] Running klayout-lvs for: $$cell"; \
		$(MAKE) klayout-lvs CELL=$$cell; \
		rc=$$?; \
		if [ $$rc -ne 0 ]; then \
			echo "[REGRESSION] FAILED: $$cell (KLAYOUT-LVS)"; \
			failed="$$failed $$cell(KLAYOUT-LVS)"; \
		else \
			echo "[REGRESSION] PASSED: $$cell"; \
		fi; \
	done; \
	echo ""; \
	echo "========================================"; \
	if [ -n "$$failed" ]; then \
		echo "[REGRESSION] SUMMARY: FAILED cells:$$failed"; \
		echo "========================================"; \
		exit 1; \
	else \
		echo "[REGRESSION] SUMMARY: All cells PASSED"; \
		echo "========================================"; \
	fi
.PHONY: klayout-lvs-regression
# ================================================================================================


# DRC Targets
klayout-drc: ## Run KLayout DRC of the CELL cell (usage: make klayout-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	python3 $(PDK_ROOT)/$(PDK)/libs.tech/klayout/tech/drc/run_drc.py \
		--path=$(LAY_DIR)/$(CELL).gds \
		--topcell=$(CELL) \
		--run_dir=$(DRC_RPT_DIR) \
		--no_feol \
		--no_density
		#--disable_extra_rules \
#		--table=all \
#		--run_mode="deep"
.PHONY: klayout-drc

magic-drc: ## Run Magic DRC of the CELL cell (usage: make magic-drc [CELL=<cellname>])
	mkdir -p $(DRC_RPT_DIR)
	sak-drc.sh -d -m -f "*" -w $(DRC_RPT_DIR) $(LAY_DIR)/$(CELL).gds $(CELL)
	rm -f $(DRC_RPT_DIR)/drc_$(CELL).tcl
.PHONY: magic-drc
# ================================================================================================


# Verify Targets
klayout-verify: ## Verify CELL cell with KLayout (usage: make klayout-verify [CELL=<cellname>])
	$(MAKE) klayout-lvs CELL=$(CELL)
	$(MAKE) klayout-drc CELL=$(CELL)
.PHONY: klayout-verify

magic-verify: ## Verify CELL cell with Magic (usage: make magic-verify [CELL=<cellname>])
	$(MAKE) magic-lvs CELL=$(CELL)
	$(MAKE) magic-drc CELL=$(CELL)
.PHONY: magic-verify

verify:
	$(MAKE) magic-verify CELL=$(CELL)
	$(MAKE) klayout-verify CELL=$(CELL)
.PHONY: verify

verify1: ## Verify CELL cell with klayout lvs and Magic drc (usage: make verify1 [CELL=<cellname>})
	$(MAKE) klayout-lvs CELL=$(CELL)
	$(MAKE) magic-drc CELL=$(CELL)
.PHONY: verify1
# ================================================================================================


# Regression Targets - auto-run over all .gds files in $(LAY_DIR)/

regression1: ## Run verify1 (klayout-lvs + magic-drc) for every .gds in $(LAY_DIR)/ (semi-fast mode)
	@failed=""; \
	for cell in $(GDS_CELLS); do \
		echo "[REGRESSION] Running verify1 for: $$cell"; \
		cell_tools=""; \
		$(MAKE) klayout-lvs CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }KLAYOUT-LVS"; \
		$(MAKE) magic-drc CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }MAGIC-DRC"; \
		if [ -n "$$cell_tools" ]; then \
			echo "[REGRESSION] FAILED: $$cell ($$cell_tools)"; \
			failed="$$failed $$cell($$cell_tools)"; \
		else \
			echo "[REGRESSION] PASSED: $$cell"; \
		fi; \
	done; \
	echo ""; \
	echo "========================================"; \
	if [ -n "$$failed" ]; then \
		echo "[REGRESSION] SUMMARY: FAILED cells:$$failed"; \
		echo "========================================"; \
		exit 1; \
	else \
		echo "[REGRESSION] SUMMARY: All cells PASSED"; \
		echo "========================================"; \
	fi
.PHONY: regression1

regression-klayout: ## Run klayout-verify (klayout-lvs + klayout-drc) for every .gds in $(LAY_DIR)/
	@failed=""; \
	for cell in $(GDS_CELLS); do \
		echo "[REGRESSION] Running klayout-verify for: $$cell"; \
		cell_tools=""; \
		$(MAKE) klayout-lvs CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }KLAYOUT-LVS"; \
		$(MAKE) klayout-drc CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }KLAYOUT-DRC"; \
		if [ -n "$$cell_tools" ]; then \
			echo "[REGRESSION] FAILED: $$cell ($$cell_tools)"; \
			failed="$$failed $$cell($$cell_tools)"; \
		else \
			echo "[REGRESSION] PASSED: $$cell"; \
		fi; \
	done; \
	echo ""; \
	echo "========================================"; \
	if [ -n "$$failed" ]; then \
		echo "[REGRESSION] SUMMARY: FAILED cells:$$failed"; \
		echo "========================================"; \
		exit 1; \
	else \
		echo "[REGRESSION] SUMMARY: All cells PASSED"; \
		echo "========================================"; \
	fi
.PHONY: regression-klayout

regression-magic: ## Run magic-verify (magic-lvs + magic-drc) for every .gds in $(LAY_DIR)/
	@failed=""; \
	for cell in $(GDS_CELLS); do \
		echo "[REGRESSION] Running magic-verify for: $$cell"; \
		cell_tools=""; \
		$(MAKE) magic-lvs CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }MAGIC-LVS"; \
		$(MAKE) magic-drc CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }MAGIC-DRC"; \
		if [ -n "$$cell_tools" ]; then \
			echo "[REGRESSION] FAILED: $$cell ($$cell_tools)"; \
			failed="$$failed $$cell($$cell_tools)"; \
		else \
			echo "[REGRESSION] PASSED: $$cell"; \
		fi; \
	done; \
	echo ""; \
	echo "========================================"; \
	if [ -n "$$failed" ]; then \
		echo "[REGRESSION] SUMMARY: FAILED cells:$$failed"; \
		echo "========================================"; \
		exit 1; \
	else \
		echo "[REGRESSION] SUMMARY: All cells PASSED"; \
		echo "========================================"; \
	fi
.PHONY: regression-magic

regression: ## Run full verify (klayout-verify + magic-verify) for every .gds in $(LAY_DIR)/
	@failed=""; \
	for cell in $(GDS_CELLS); do \
		echo "[REGRESSION] Running verify for: $$cell"; \
		cell_tools=""; \
		$(MAKE) klayout-lvs CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }KLAYOUT-LVS"; \
		$(MAKE) klayout-drc CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }KLAYOUT-DRC"; \
		$(MAKE) magic-lvs CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }MAGIC-LVS"; \
		$(MAKE) magic-drc CELL=$$cell || cell_tools="$${cell_tools:+$$cell_tools, }MAGIC-DRC"; \
		if [ -n "$$cell_tools" ]; then \
			echo "[REGRESSION] FAILED: $$cell ($$cell_tools)"; \
			failed="$$failed $$cell($$cell_tools)"; \
		else \
			echo "[REGRESSION] PASSED: $$cell"; \
		fi; \
	done; \
	echo ""; \
	echo "========================================"; \
	if [ -n "$$failed" ]; then \
		echo "[REGRESSION] SUMMARY: FAILED cells:$$failed"; \
		echo "========================================"; \
		exit 1; \
	else \
		echo "[REGRESSION] SUMMARY: All cells PASSED"; \
		echo "========================================"; \
	fi
.PHONY: regression
# ================================================================================================