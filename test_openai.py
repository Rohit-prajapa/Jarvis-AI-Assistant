from openai import OpenAI
from config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY
)


try:
    print("Testing OpenAI API...")

    response = client.responses.create(
        model="gpt-4.1-mini",
        input="What is machine learning?"
    )

    print("\nSUCCESS!")
    print(response.output_text)

except Exception as e:
    print("\nOPENAI API FAILED")
    print("Error Type:", type(e).__name__)
    print("Error:", e)