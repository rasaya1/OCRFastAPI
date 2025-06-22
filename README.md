# Advanced OCR Document Processing System

A comprehensive document processing system with OCR, vector-based classification, entity extraction, and web interface.

## Project Overview

This system provides end-to-end document processing capabilities:

- **OCR Processing**: Extract text from PDFs and images using Tesseract and EasyOCR
- **Document Classification**: Classify documents into 5 types using FAISS vector similarity
- **Entity Extraction**: Extract structured data using LLM prompts with regex fallback
- **Web Interface**: User-friendly upload interface for batch document processing
- **REST API**: FastAPI endpoints for system integration
- **Batch Processing**: Handle multiple documents simultaneously

### Supported Document Types
- **Invoice**: Invoice numbers, dates, amounts, vendor details
- **Receipt**: Store information, transaction details, payment methods
- **Contract**: Agreement terms, parties, compensation details
- **Purchase Order**: PO numbers, items, delivery information
- **Report**: Business metrics, financial data, key insights

### Supported File Formats
PDF, PNG, JPG, JPEG, TIFF, BMP

## Project Structure

```
aimltest/
├── src/                    # Core modules
│   ├── main.py            # OCR processor (Tesseract + EasyOCR)
│   ├── vector_db.py       # FAISS vector database
│   ├── api.py             # FastAPI REST API
│   ├── entity_extractor.py # LLM entity extraction
│   └── web_interface.py   # Web upload interface
├── templates/             # HTML templates
│   ├── upload.html        # Document upload form
│   └── results.html       # Processing results display
├── tests/                 # Test suite
│   ├── test_single.py     # OCR testing
│   └── test_api_simple.py # API testing
├── examples/              # Usage examples
├── demos/                 # Demo scripts
├── utils/                 # Utility scripts
├── output/                # Sample documents
├── requirements.txt       # All dependencies
├── run_all_tests.py      # Comprehensive test runner
├── start_web_app.py      # Web interface startup
├── start_api.py          # API server startup
└── config.py             # System configuration
```

## Installation Instructions

### 1. System Dependencies

**Windows:**
- Install Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki
- Install Poppler from: https://blog.alivate.com.au/poppler-windows/

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils

# macOS
brew install tesseract poppler
```

### 2. Python Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Or use make
make install
```

### 3. Verify Installation

```bash
# Check system dependencies
python config.py

# Run comprehensive test suite
python run_all_tests.py
```

## Configuration Guidelines

### Environment Variables (Optional)

**For enhanced entity extraction with OpenAI:**

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your-actual-api-key-here
   ```

3. Or set environment variable directly:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

**Note:** The system works without OpenAI API key using local regex-based extraction.

### System Paths

The system automatically detects Tesseract and Poppler installations. If needed, modify paths in `config.py`:

```python
TESSERACT_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
POPPLER_PATH = "C:\\path\\to\\poppler\\bin"
```

### Vector Database

Initialize the vector database with sample documents:

```bash
python demos/fresh_vector_demo.py
```

## API Documentation

### Base URL
- **Development**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1750621639.16
}
```

#### Database Statistics
```http
GET /stats
```

**Response:**
```json
{
  "total_documents": 5,
  "document_types": {
    "invoice": 2,
    "receipt": 1,
    "contract": 1,
    "purchase_order": 1
  },
  "embedding_dimension": 384
}
```

#### Document Processing
```http
POST /extract_entities/
Content-Type: multipart/form-data
```

**Request:**
```bash
curl -X POST "http://localhost:8000/extract_entities/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_invoice.pdf"
```

**Response:**
```json
{
  "document_type": "invoice",
  "confidence": 0.85,
  "entities": {
    "invoice_number": "INV-2024-001",
    "date": "January 15, 2024",
    "due_date": "February 15, 2024",
    "vendor_name": "ABC Corporation",
    "customer_name": "XYZ Company",
    "total_amount": "$7,866.25",
    "subtotal": "$7,250.00",
    "tax_amount": "$616.25"
  },
  "processing_time": "1.25s"
}
```

#### Web Interface
```http
GET /
```
Returns HTML upload form for interactive document processing.

```http
POST /upload
Content-Type: multipart/form-data
```
Processes uploaded files and returns formatted HTML results.

### Error Responses

**400 Bad Request - Invalid File Format:**
```json
{
  "detail": "Unsupported file format. Allowed: .pdf, .png, .jpg, .jpeg, .tiff, .bmp"
}
```

**422 Unprocessable Entity - No Text Extracted:**
```json
{
  "detail": "No text extracted from document"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Processing error: [error details]"
}
```

## Testing Procedures

### Comprehensive Test Suite

```bash
# Run all 6 tests
python run_all_tests.py
```

**Expected Output:**
- Configuration Check ✓
- Vector Database Demo ✓
- Document Search ✓
- API Functionality ✓
- Web Interface ✓
- OCR Processing ✓

### Individual Component Tests

```bash
# OCR processing
python tests/test_single.py

# API endpoints
python tests/test_api_simple.py

# Web interface
python test_web_interface.py

# Vector database
python demos/fresh_vector_demo.py

# Document search
python utils/search_documents.py "invoice payment"
```

### Manual Testing

#### Web Interface
```bash
# Start web application
python start_web_app.py

# Visit http://localhost:8000
# Upload documents and verify results
```

#### API Testing
```bash
# Start API server
python start_api.py

# Test endpoints
curl -X GET "http://localhost:8000/health"
curl -X GET "http://localhost:8000/stats"
```

## Usage Examples

### Web Interface Usage

1. **Start Application:**
   ```bash
   python start_web_app.py
   ```

2. **Access Interface:** http://localhost:8000

3. **Upload Documents:** Select multiple PDF/image files

4. **View Results:** Formatted display with document types and extracted entities

### API Integration

#### Python Example
```python
import requests

# Process document
with open('invoice.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/extract_entities/',
        files=files
    )
    result = response.json()
    print(f"Document Type: {result['document_type']}")
    print(f"Entities: {result['entities']}")
```

#### JavaScript Example
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/extract_entities/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('Document Type:', data.document_type);
    console.log('Entities:', data.entities);
});
```

### Command Line Usage

```bash
# Process single document
python src/main.py document.pdf

# Search similar documents
python utils/search_documents.py "contract terms"

# Batch processing via API
for file in *.pdf; do
    curl -X POST "http://localhost:8000/extract_entities/" \
         -F "file=@$file"
done
```

## Example Requests and Responses

### Invoice Processing

**Request:**
```bash
curl -X POST "http://localhost:8000/extract_entities/" \
  -F "file=@sample_invoice.pdf"
```

**Response:**
```json
{
  "document_type": "invoice",
  "confidence": 0.92,
  "entities": {
    "invoice_number": "INV-12345",
    "date": "2024-01-01",
    "due_date": "2024-01-31",
    "vendor_name": "ABC Corp",
    "customer_name": "XYZ Ltd",
    "total_amount": "$450.00",
    "subtotal": "$400.00",
    "tax_amount": "$50.00"
  },
  "processing_time": "1.25s"
}
```

### Receipt Processing

**Request:**
```bash
curl -X POST "http://localhost:8000/extract_entities/" \
  -F "file=@receipt.jpg"
```

**Response:**
```json
{
  "document_type": "receipt",
  "confidence": 0.88,
  "entities": {
    "store_name": "Tech Solutions",
    "date": "March 10, 2024",
    "time": "14:30",
    "transaction_id": "TXN-789",
    "total_amount": "$125.50",
    "payment_method": "Credit Card"
  },
  "processing_time": "0.95s"
}
```

### Contract Processing

**Request:**
```bash
curl -X POST "http://localhost:8000/extract_entities/" \
  -F "file=@contract.pdf"
```

**Response:**
```json
{
  "document_type": "contract",
  "confidence": 0.91,
  "entities": {
    "contract_date": "March 1, 2024",
    "parties": "TechCorp Solutions, ClientCorp Inc.",
    "term_duration": "twelve (12) months",
    "compensation": "$15,000 monthly",
    "termination_clause": "sixty (60) days written notice"
  },
  "processing_time": "1.45s"
}
```

### Batch Processing Response

**Request:**
```bash
# Multiple files via web interface
POST /upload
files: [invoice1.pdf, receipt1.jpg, contract1.pdf]
```

**Response:** HTML page with formatted results for each document showing classification, confidence scores, and extracted entities.

## Performance Metrics

- **Processing Time**: 1-3 seconds per document
- **Classification Accuracy**: 85%+ confidence scores
- **Supported Formats**: 6 file types (PDF, PNG, JPG, JPEG, TIFF, BMP)
- **Concurrent Processing**: Async handling for multiple files
- **Memory Efficiency**: Optimized for batch processing

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `pip install -r requirements.txt`
2. **OCR Failures**: Verify Tesseract installation with `python config.py`
3. **API Errors**: Check server logs and ensure all dependencies installed
4. **Vector DB Issues**: Re-run `python demos/fresh_vector_demo.py`

### System Requirements

- **Python**: 3.8+
- **Memory**: 4GB+ RAM recommended
- **Storage**: 2GB+ free space
- **OS**: Windows, Linux, macOS

## License

RCSAS License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

---

**Status: ✅ Production Ready** - Complete document processing system with web interface and API access!