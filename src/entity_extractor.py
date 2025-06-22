"""
Entity extraction using LLM prompts
"""

import json
import re
from typing import Dict, Any, Optional

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class EntityExtractor:
    """Entity extraction using OpenAI GPT or local models"""
    
    def __init__(self, model="gpt-3.5-turbo", api_key: Optional[str] = None):
        self.model = model
        self.use_openai = api_key is not None and OPENAI_AVAILABLE
        
        if self.use_openai:
            self.client = OpenAI(api_key=api_key)
        
        # Document type specific field mappings
        self.field_mappings = {
            "invoice": [
                "invoice_number", "date", "due_date", "vendor_name", 
                "customer_name", "total_amount", "subtotal", "tax_amount"
            ],
            "receipt": [
                "store_name", "date", "time", "transaction_id", 
                "total_amount", "payment_method", "items"
            ],
            "contract": [
                "contract_date", "parties", "term_duration", 
                "compensation", "termination_clause"
            ],
            "purchase_order": [
                "po_number", "date", "vendor", "ship_to", 
                "total_amount", "delivery_date", "items"
            ],
            "report": [
                "report_period", "company_name", "revenue", 
                "key_metrics", "outlook"
            ]
        }
    
    async def extract_entities(self, text: str, document_type: str) -> Dict[str, Any]:
        """Extract entities from text based on document type"""
        
        if self.use_openai:
            return await self._extract_with_openai(text, document_type)
        else:
            return self._extract_with_regex(text, document_type)
    
    async def _extract_with_openai(self, text: str, document_type: str) -> Dict[str, Any]:
        """Extract entities using OpenAI GPT"""
        
        fields = self.field_mappings.get(document_type, ["key_information"])
        field_list = ", ".join(fields)
        
        prompt = f"""Given the following text extracted from a document of type '{document_type}',
extract these fields: {field_list}.
Return your response as a valid JSON object with no additional text.
If a field is not found, use null as the value.

Document Text:
{text[:2000]}"""  # Limit text length for API
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a document processing assistant that extracts structured data from text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                entities = json.loads(content)
                return entities
            except json.JSONDecodeError:
                # Try to extract JSON from response
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {"error": "Failed to parse LLM response"}
                    
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}
    
    def _extract_with_regex(self, text: str, document_type: str) -> Dict[str, Any]:
        """Extract entities using regex patterns (fallback method)"""
        
        entities = {}
        text_lower = text.lower()
        
        # Common patterns
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\w+ \d{1,2}, \d{4}\b'
        amount_pattern = r'\$[\d,]+\.?\d*'
        
        # Extract dates
        dates = re.findall(date_pattern, text)
        if dates:
            entities["date"] = dates[0]
        
        # Extract amounts
        amounts = re.findall(amount_pattern, text)
        if amounts:
            entities["total_amount"] = amounts[-1]  # Usually the last amount is total
        
        # Document type specific extractions
        if document_type == "invoice":
            # Invoice number
            inv_match = re.search(r'invoice\s*#?:?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
            if inv_match:
                entities["invoice_number"] = inv_match.group(1)
            
            # Vendor name (usually first company mentioned)
            company_match = re.search(r'^([A-Z][A-Za-z\s&]+(?:Corp|Corporation|Inc|LLC|Ltd))', text, re.MULTILINE)
            if company_match:
                entities["vendor_name"] = company_match.group(1).strip()
        
        elif document_type == "receipt":
            # Store name
            store_match = re.search(r'store name:?\s*([^\n]+)', text, re.IGNORECASE)
            if store_match:
                entities["store_name"] = store_match.group(1).strip()
            
            # Transaction ID
            trans_match = re.search(r'transaction\s*id:?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
            if trans_match:
                entities["transaction_id"] = trans_match.group(1)
        
        elif document_type == "purchase_order":
            # PO Number
            po_match = re.search(r'po\s*number:?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
            if po_match:
                entities["po_number"] = po_match.group(1)
        
        return entities

# Fallback for when OpenAI API is not available
class LocalEntityExtractor(EntityExtractor):
    """Local entity extraction without external APIs"""
    
    def __init__(self):
        super().__init__(api_key=None)
    
    async def extract_entities(self, text: str, document_type: str) -> Dict[str, Any]:
        return self._extract_with_regex(text, document_type)