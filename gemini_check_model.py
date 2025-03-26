import os
import google.generativeai as genai

def list_gemini_models():
  """Lists available Gemini models."""
  # Configure the API key
  GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
  if not GOOGLE_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set.")
    return
  
  genai.configure(api_key=GOOGLE_API_KEY)
  for m in genai.list_models():
      if 'generateContent' in m.supported_generation_methods:
         print(f"{m.name}: {m.description}")

if __name__ == "__main__":
   list_gemini_models()