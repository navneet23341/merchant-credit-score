from openai import OpenAI
import os
from dotenv import load_dotenv
import time

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

models = [
    "liquid/lfm-2.5-2.6b:free",
    "z-ai/glm-5.2:free",
    "thinkingmachines/inkling-small:free",
    "poolside/laguna-xs-2.1:free",
    "minimax/minimax-m3:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-26b-a4b-it:free",
    "google/gemma-4-31b-it:free",
]

prompt = """
You are a financial advisor explaining credit scores
to Indian small business owners.

Merchant details:

Category: Grocery
City: Delhi
Credit Score: 720

Top positive factor:
revenue_consistency
(pushes score up 42 points)

Top negative factor:
chargeback_rate
(pulls score down 28 points)

Generate a friendly explanation in Hinglish
(mix of Hindi and English).

Keep it simple.
Keep it under 100 words.
Be encouraging but honest.

Start exactly with:
"Aapka score..."

Do not use markdown.
Do not use bullet points.
Do not invent financial information.
Do not mention that you are an AI.
"""

for model in models:

    print("\n" + "=" * 70)
    print("MODEL:", model)
    print("=" * 70)

    start = time.time()

    try:

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.6,
            max_tokens=200,
        )

        elapsed = time.time() - start

        text = response.choices[0].message.content

        print("TIME:", round(elapsed, 2), "seconds")
        print("OUTPUT:")
        print(text)

    except Exception as e:

        elapsed = time.time() - start

        print("FAILED")
        print("TIME:", round(elapsed, 2))
        print("ERROR:", e)