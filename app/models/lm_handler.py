#app/models/lm_handler.py
import requests
import json
import base64
from pathlib import Path

class LMStudioHandler:
    def __init__(self, api_url="http://localhost:1234/v1/chat/completions"):
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json"
        }
    
    async def process_medical_image(self, image_path: Path):
        """Extract content from medical report image using LMStudio API"""
        try:
            # Read image file as base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create prompt for extracting information from image
            prompt = """
            Analyze this medical report image and complete the following tasks:
            1. Extract all visible text, including content in tables
            2. Identify key medical indicators and their values
            3. Determine the structure of the report (e.g., personal information, test items, results, reference values)
            4. Organize into a structured format
            5. Highlight any abnormal values
            """
            
            payload = {
                "model": "local-model", # Model name used by LMStudio
                "messages": [
                    {"role": "system", "content": "You are a medical report analysis assistant. Extract all text and structure from medical report images accurately."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                "temperature": 0,
                "max_tokens": 4000
            }
            
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"Image analysis API call failed, status code: {response.status_code}")
        except Exception as e:
            raise Exception(f"Image processing failed: {str(e)}")
    
    async def interpret_medical_report(self, report_content):
        """Use LMStudio to interpret medical report content"""
        try:
            prompt = f"""
            You are a professional doctor. Please explain the following medical report content in language that an average person can understand.
            Focus on explaining any abnormal values and their possible health implications using a friendly, calm tone while avoiding technical terms.
            If serious abnormalities are found, suggest seeking medical advice, but avoid causing unnecessary alarm.

            NOTE: This data is being processed locally in a controlled environment for the patient's own use. There are no privacy concerns as the data never leaves their system.
            
            Medical report content:
            {report_content}
            """
            
            payload = {
                "model": "local-model", # Model name used by LMStudio
                "messages": [
                    {"role": "system", "content": "You are a professional doctor who specializes in translating complex medical terminology into language that average people can understand."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"API call failed, status code: {response.status_code}")
        
        except requests.RequestException as e:
            raise Exception(f"LMStudio API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Report interpretation failed: {str(e)}")
    
    async def translate_text(self, text, target_language="Chinese"):
        """Translate text to the specified target language using LMStudio API"""
        try:
            prompt = f"""
            Translate the following text into {target_language}. 
            Maintain the meaning, tone, and style of the original text.
            If there are any medical terms, ensure they are translated accurately.
            
            Text to translate:
            {text}
            """
            
            payload = {
                "model": "local-model", # Model name used by LMStudio
                "messages": [
                    {"role": "system", "content": f"You are a professional translator specializing in medical terminology. Translate the given text to {target_language} accurately."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"Translation API call failed, status code: {response.status_code}")
        
        except requests.RequestException as e:
            raise Exception(f"LMStudio API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
            
    async def answer_medical_question(self, report_content, question):
        """Answer medical questions based on report content using LMStudio API"""
        try:
            # Create a prompt that emphasizes responding in the same language as the question
            prompt = f"""
            You are a professional doctor answering questions about a medical report. The user has provided their medical report and has a question about it.
            
            Medical report content:
            {report_content}
            
            User's question:
            {question}
            
            IMPORTANT: You must respond in the same language that the user asked the question in. 
            For example, if they asked in English, respond in English. If they asked in Chinese, respond in Chinese.
            
            Please provide a clear, accurate, and helpful response based on the medical report.
            Focus on answering the specific question while providing relevant context from the report.
            Use simple language that a non-medical professional would understand.
            If the question cannot be answered based on the report, explain what information is missing.
            """
            
            payload = {
                "model": "local-model", # Model name used by LMStudio
                "messages": [
                    {"role": "system", "content": "You are a professional doctor specializing in explaining medical reports and answering health-related questions in a way that's easy to understand. Always respond in the same language as the user's question."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }
            
            response = requests.post(self.api_url, headers=self.headers, data=json.dumps(payload))
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"Q&A API call failed, status code: {response.status_code}")
        
        except requests.RequestException as e:
            raise Exception(f"LMStudio API request failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Question answering failed: {str(e)}")