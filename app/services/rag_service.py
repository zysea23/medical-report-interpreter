# app/services/rag_service.py
from app.models.rag_handler import RAGHandler


class RAGService:
    def __init__(self):
        """Initialize the RAG service"""
        self.rag_handler = RAGHandler()
    
    async def process_with_rag(self, medical_report, question=None):
        """
        Process medical report with RAG
        
        Args:
            medical_report: Medical report text
            question: Optional specific question
            
        Returns:
            dict: Contains enhanced explanation and references
        """
        try:
            result = self.rag_handler.enhance_explanation(
                medical_text=medical_report,
                question=question,
                k=8
            )
            
            return {
                "success": True,
                "enhanced_explanation": result["enhanced_explanation"],
                "references": result["references"][:5]  # Return only the top 5 most relevant references
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"RAG processing failed: {str(e)}"
            }
    
    async def answer_medical_question(self, question):
        """
        Answer medical questions using RAG
        
        Args:
            question: Medical question
            
        Returns:
            dict: Contains answer and references
        """
        try:
            # For definition questions, modify the prompt to request natural language
            if question.lower().startswith("what is") or question.lower().startswith("define"):
                question = f"{question}? Please provide a clear definition and explanation in natural language."
            
            result = self.rag_handler.answer_medical_question(
                question=question,
                k=16
            )
            
            return {
                "success": True,
                "answer": result["answer"],
                "references": result["references"][:5]  # Return only the top 5 most relevant references
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to answer medical question: {str(e)}"
            }


# Create a singleton instance to avoid repeated initialization of RAG system
rag_service = RAGService()