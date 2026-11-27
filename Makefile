PYTHON ?= python3
PANDOC ?= pandoc
DOCX_TEMPLATE ?= matrix/templates/DNS-Abuse-Techniques-Matrix.docx
MATRIX_DIR := matrix
BUILD_DIR := build/matrix
REPORT_MD := $(BUILD_DIR)/report.md
REPORT_PDF := $(BUILD_DIR)/DNS-Abuse-Techniques-Matrix.pdf
DRAFT_REPORT_PDF := $(BUILD_DIR)/DNS-Abuse-Techniques-Matrix-draft.pdf

.PHONY: import validate tables assemble pdf pdf-check pdf-test draft-pdf check-tools clean

import:
	$(PYTHON) $(MATRIX_DIR)/scripts/import_docx.py "$(DOCX_TEMPLATE)" --out $(BUILD_DIR)/imported

validate:
	$(PYTHON) $(MATRIX_DIR)/scripts/validate_matrix.py $(MATRIX_DIR)

tables: validate
	$(PYTHON) $(MATRIX_DIR)/scripts/build_tables.py $(MATRIX_DIR)

assemble: tables
	mkdir -p $(BUILD_DIR)
	$(PYTHON) $(MATRIX_DIR)/scripts/assemble_report.py $(MATRIX_DIR) --out $(REPORT_MD)

pdf: validate
	$(PYTHON) $(MATRIX_DIR)/scripts/build_docx_pdf.py --matrix-dir "$(MATRIX_DIR)" --template "$(DOCX_TEMPLATE)" --out "$(REPORT_PDF)"

pdf-check:
	$(PYTHON) $(MATRIX_DIR)/scripts/check_pdf_layout.py --matrix-dir "$(MATRIX_DIR)" --template "$(DOCX_TEMPLATE)" --pdf "$(REPORT_PDF)"

pdf-test:
	$(PYTHON) -m unittest discover -s $(MATRIX_DIR)/tests -p 'test_*.py'

# Historical alternative, kept only for work on the structured reference data.
draft-pdf: assemble check-tools
	$(PANDOC) $(REPORT_MD) --from markdown+raw_attribute --to typst --template $(MATRIX_DIR)/templates/dns-abuse-report.typ --pdf-engine=typst -o $(DRAFT_REPORT_PDF)

check-tools:
	command -v $(PANDOC)
	command -v typst

clean:
	rm -rvf $(BUILD_DIR) $(MATRIX_DIR)/generated

