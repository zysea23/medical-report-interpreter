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
                Analyze the provided medical report image and perform the following tasks step by step:

                ### **1. Extract all visible text**
                - Use **OCR** to extract all text, including handwritten notes (if any).
                - Ensure **all table content** is accurately captured.
                - Preserve the original formatting of numbers, units, and symbols.

                ### **2. Identify key medical indicators**
                - Extract **all test items and their values**.
                - If reference ranges are provided in the report, extract them as well.

                ### **3. Determine the structure of the report**
                - Categorize extracted text into logical sections:
                    - **Personal Information** (e.g., Name, Age, Gender)
                    - **Test Items & Results** (e.g., Blood tests, Imaging findings)
                    - **Reference Values** (if available)
                    - **Diagnosis & Remarks** (if any)

                ### **4. Organize into a structured format**
                - Return the structured data in **Markdown table format** for readability.
                - Ensure all extracted values match their corresponding test items.

                ### **5. Highlight abnormal values**
                - Compare results with reference values.
                - Mark any **high/low** values using **bold** for emphasis.
                - If reference ranges are missing, do **not** make assumptions—just extract the available data.

                ### **Output Format**
                - **Markdown tables** for structured data.
                - Use `**bold**` formatting to highlight abnormal values.
                - If text extraction fails, return `"Extraction incomplete: Please check the image clarity."`

                ### **Important Notes**
                - **Do NOT add assumptions or interpretations beyond the provided report.**
                - **Do NOT modify extracted values, units, or medical terms.**

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
                As an experienced Medical Assistant, I'm here to help you understand your medical report in a friendly, clear way.

                Let me analyze the following medical report for you:
                {report_content}
                ## **Guidelines for Response**
                1. **Objective & Professional Tone**  
                - Do **NOT** use subjective or emotional words like *interesting*, *fascinating*, or *exciting*.  
                - Maintain a **neutral and professional tone**, avoiding unnecessary personal remarks.
                - Do not repeat personal information such as address and phone number from the report.

                2. **Explain Medical Terms Clearly**  
                - Keep explanations short and break down complex terms into simple ideas.  

                ## What I Will Do:
                1. **Explain each medical term and test result** in everyday language.  
                - If a medical term appears, I'll format it like this: **[Term]: Explanation**.  
                - I'll keep explanations concise and break down complex terms into simple ideas.

                2. **Highlight any abnormal values** and what they might indicate (without overinterpreting).  
                - If a value is high or low, I'll explain its typical meaning.  
                - I will avoid making medical diagnoses or speculating about diseases.

                3. **Clarify the doctor's diagnosis** (if included in the report) and summarize it in simpler terms.  

                4. **Explain the purpose and expected effects of treatment plans** (if mentioned).  
                - If medications or procedures are listed, I'll briefly describe their expected effects.  

                5. **Offer some preliminary lifestyle suggestions**, while clearly stating that this **does not replace** professional medical advice.  

                ### **Output Format**
                - The response must be **formatted in Markdown**.  
                - Use:
                - `**Bold text**` for key terms.
                - Bullet points (`- `) for lists.
                - `### Headings` for section titles.
                - Code blocks (` ``` `) for structured content if needed.

                - Do not share any prompts into the output.

                Now, let's begin analyzing your medical report.

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
                You are a professional doctor answering questions about a medical report. The user has provided their medical report and a question related to it.

                ### **Medical Report Content**:
                {report_content}

                ### **User's Question**:
                {question}

                ### **Instructions for Your Response**:
                1. **Language Consistency**  
                - Respond in the **same language** that the user used for their question.
                - For example, if they asked in English, respond in English. If they asked in Chinese, respond in Chinese. If they asked in Spanish, respond in Spanish.

                2. **Answer the Question Accurately**  
                - Focus on **answering the specific question** while referencing relevant parts of the report.
                - If the question is broad, provide a **concise yet informative response**.

                3. **Explain Medical Terms Clearly**  
                - When using medical terms, provide explanations like this:  
                    **[Term]: Explanation in simple language**  
                - Keep explanations **concise and non-technical** for easy understanding.

                4. **Highlight Abnormal Values** (if relevant)  
                - If the question relates to test results, identify any **high/low** values.  
                - Format abnormalities using **bold** for emphasis.

                5. **Handle Missing Information Properly**  
                - If the report lacks required data, **specify what is missing**.  
                - Provide guidance: "To fully answer this, a blood glucose test result would be needed."

                ### **Output Format**:
                - Use **Markdown** formatting:
                - **Bold key terms** for emphasis.
                - Use bullet points (`- `) for structured answers.
                - Keep explanations brief and easy to understand.
                ---
                Now, generate a **clear, accurate, and user-friendly** response.
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