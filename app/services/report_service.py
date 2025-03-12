# app/services/report_service.py
from app.models.lm_handler import LMStudioHandler
from pathlib import Path

async def process_report(file_path: Path):
    """Process medical report, extract content and generate explanation"""
    try:
        # Initialize LMStudio handler
        lm_handler = LMStudioHandler()
        
        # Use LMStudio API to analyze image and extract content
        original_content = await lm_handler.process_medical_image(file_path)
        
        # Use LMStudio API to interpret content
        explanation = await lm_handler.interpret_medical_report(original_content)
        
        return original_content, explanation
    
    except Exception as e:
        raise Exception(f"Report processing failed: {str(e)}")
