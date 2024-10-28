from huggingface_hub import InferenceClient


model = "mistralai/Mistral-Nemo-Instruct-2407"
client = InferenceClient(api_key="")
META_PROMPT = "Based on the user's partial input, predict and generate a possible full question or topic the user might be asking. The completion should be natural and relevant to the partial text. Remember not to generate any thing else except for the guess, no extra english."


def generate_response(prompt):
    response = client.chat_completion(
        model=model,
        messages=[
            {"role": "system", "content": META_PROMPT},
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=20,
        stream=False,
        temperature=0.2,
    )

    return response["choices"][0]["message"]["content"]
