#!/usr/bin/env python3
"""Create a sample invoice image for OCR testing"""

from PIL import Image, ImageDraw, ImageFont
import sys
from pathlib import Path

def create_invoice_image():
    # Create a white image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a basic font
    try:
        font_large = ImageFont.truetype("arial.ttf", 24)
        font_medium = ImageFont.truetype("arial.ttf", 16)
        font_small = ImageFont.truetype("arial.ttf", 12)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Invoice content
    y = 50
    
    # Header
    draw.text((50, y), "INVOICE", fill='black', font=font_large)
    y += 60
    
    # Company info
    company_info = [
        "ABC Corporation",
        "123 Business Street",
        "New York, NY 10001",
        "Phone: (555) 123-4567"
    ]
    
    for line in company_info:
        draw.text((50, y), line, fill='black', font=font_medium)
        y += 25
    
    y += 30
    
    # Bill to
    draw.text((50, y), "BILL TO:", fill='black', font=font_medium)
    y += 30
    
    bill_to = [
        "XYZ Company",
        "456 Client Avenue", 
        "Los Angeles, CA 90210"
    ]
    
    for line in bill_to:
        draw.text((50, y), line, fill='black', font=font_small)
        y += 20
    
    y += 30
    
    # Invoice details
    details = [
        "Invoice #: INV-2024-001",
        "Date: January 15, 2024",
        "Due Date: February 15, 2024"
    ]
    
    for line in details:
        draw.text((50, y), line, fill='black', font=font_medium)
        y += 25
    
    y += 40
    
    # Table header
    draw.text((50, y), "DESCRIPTION", fill='black', font=font_medium)
    draw.text((300, y), "QTY", fill='black', font=font_medium)
    draw.text((400, y), "RATE", fill='black', font=font_medium)
    draw.text((500, y), "AMOUNT", fill='black', font=font_medium)
    y += 30
    
    # Draw line
    draw.line([(50, y), (600, y)], fill='black', width=1)
    y += 20
    
    # Table content
    items = [
        ("Professional Services", "40", "$150.00", "$6,000.00"),
        ("Software License", "1", "$500.00", "$500.00"),
        ("Technical Support", "10", "$75.00", "$750.00")
    ]
    
    for item in items:
        draw.text((50, y), item[0], fill='black', font=font_small)
        draw.text((300, y), item[1], fill='black', font=font_small)
        draw.text((400, y), item[2], fill='black', font=font_small)
        draw.text((500, y), item[3], fill='black', font=font_small)
        y += 25
    
    y += 30
    
    # Totals
    totals = [
        ("SUBTOTAL:", "$7,250.00"),
        ("TAX (8.5%):", "$616.25"),
        ("TOTAL:", "$7,866.25")
    ]
    
    for label, amount in totals:
        draw.text((400, y), label, fill='black', font=font_medium)
        draw.text((500, y), amount, fill='black', font=font_medium)
        y += 25
    
    y += 40
    
    # Footer
    footer = [
        "Payment Terms: Net 30 days",
        "Thank you for your business!"
    ]
    
    for line in footer:
        draw.text((50, y), line, fill='black', font=font_small)
        y += 20
    
    # Save the image
    output_path = Path(__file__).parent / "sample_invoice.png"
    image.save(output_path)
    print(f"Sample invoice created: {output_path}")
    return output_path

if __name__ == "__main__":
    create_invoice_image()