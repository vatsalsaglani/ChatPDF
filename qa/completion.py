import openai

class Completion:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def __call__(self, message: str, system_prompt: str, model: str):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]
        try:
            for resp in openai.ChatCompletion.create(
                model=model, messages=messages, stream=True, temperature=0.2, max_tokens=2_000
            ):
                content = resp.get("choices")[0].get("delta", {}).get("content")
                if content is not None:
                    yield content
        except Exception as err:
            print(err)
            pass
