# Makefile for Advanced OCR Text Extraction

.PHONY: help install test clean run-examples check-deps

# Default target
help:
	@echo "Advanced OCR Text Extraction - Available Commands"
	@echo "================================================="
	@echo "install      - Install Python dependencies"
	@echo "test         - Run all tests"
	@echo "check-deps   - Check system dependencies"
	@echo "run-examples - Run usage examples"
	@echo "clean        - Clean output and cache files"
	@echo "setup        - Complete setup (install + check)"
	@echo ""
	@echo "Usage Examples:"
	@echo "  make install"
	@echo "  make test"
	@echo "  python ocr_tool.py document.pdf"

# Install Python dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "[OK] Dependencies installed"

# Run all tests
test:
	@echo "Running test suite..."
	python run_tests.py

# Check system dependencies
check-deps:
	@echo "Checking system dependencies..."
	python config.py

# Run examples
run-examples:
	@echo "Running usage examples..."
	python examples/basic_usage.py

# Clean output and cache files
clean:
	@echo "Cleaning output and cache files..."
	@if exist output\\*.txt del /q output\\*.txt
	@if exist test_output rmdir /s /q test_output
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist src\\__pycache__ rmdir /s /q src\\__pycache__
	@if exist tests\\__pycache__ rmdir /s /q tests\\__pycache__
	@echo "✅ Cleaned"

# Complete setup
setup: install check-deps
	@echo "[OK] Setup complete! Run 'make test' to verify installation."

# Vector database demo
vector-demo:
	@echo "Running vector database demo..."
	python demos/quick_vector_demo.py

# Document search
search:
	@echo "Running document search demo..."
	python utils/search_documents.py

# Full demo
full-demo: vector-demo search
	@echo "All demos completed!"

# Start API server
start-api:
	@echo "Starting FastAPI server..."
	python start_api.py

# Test API
test-api:
	@echo "Testing API endpoints..."
	python tests/test_api_simple.py

# Run all tests
test-all:
	@echo "Running comprehensive test suite..."
	python run_all_tests.py

# Quick start
quick-start:
	@echo "Quick Start Guide"
	@echo "================"
	@echo "1. Install system dependencies:"
	@echo "   - Tesseract OCR (automatically added to PATH)"
	@echo "   - Poppler utilities"
	@echo ""
	@echo "2. Install Python dependencies:"
	@echo "   make install"
	@echo ""
	@echo "3. Test installation:"
	@echo "   make test"
	@echo ""
	@echo "4. Process your first document:"
	@echo "   python ocr_tool.py your_document.pdf"