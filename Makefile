.PHONY: publications install clean

# Install dependencies
install:
	pip install -r requirements.txt

# Generate publication list from BibTeX
publications:
	python scripts/generate_publications.py

# Clean generated files (if needed)
clean:
	@echo "Cleaning generated files..."
	@echo "Nothing to clean currently"

# Help
help:
	@echo "Available commands:"
	@echo "  make install       - Install Python dependencies"
	@echo "  make publications  - Generate publication list from BibTeX"
	@echo "  make clean         - Clean generated files"
	@echo "  make help          - Show this help message"
	@echo ""
	@echo "To add a new publication:"
	@echo "  1. Edit _data/publications.bib"
	@echo "  2. Run 'make publications'" 