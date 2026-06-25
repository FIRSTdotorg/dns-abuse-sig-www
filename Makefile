PYTHON ?= python3
PANDOC ?= pandoc
DOCX_SOURCE ?= ../DNS Abuse Techniques Matrix.docx
MATRIX_DIR := matrix
BUILD_DIR := build/matrix
REPORT_MD := $(BUILD_DIR)/report.md
REPORT_PDF := $(BUILD_DIR)/DNS-Abuse-Techniques-Matrix.pdf

.PHONY: import validate tables assemble pdf check-tools clean

import:
	$(PYTHON) $(MATRIX_DIR)/scripts/import_docx.py "$(DOCX_SOURCE)" --out $(MATRIX_DIR)

validate:
	$(PYTHON) $(MATRIX_DIR)/scripts/validate_matrix.py $(MATRIX_DIR)

tables: validate
	$(PYTHON) $(MATRIX_DIR)/scripts/build_tables.py $(MATRIX_DIR)

assemble: tables
	mkdir -p $(BUILD_DIR)
	$(PYTHON) $(MATRIX_DIR)/scripts/assemble_report.py $(MATRIX_DIR) --out $(REPORT_MD)

pdf: assemble check-tools
	$(PANDOC) $(REPORT_MD) --from markdown+raw_attribute --to typst --template $(MATRIX_DIR)/templates/dns-abuse-report.typ --pdf-engine=typst -o $(REPORT_PDF)

check-tools:
	command -v $(PANDOC)
	command -v typst

clean:
	rm -rf $(BUILD_DIR) $(MATRIX_DIR)/generated

