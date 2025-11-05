import os
from dotenv import load_dotenv

load_dotenv()

try:
    import openai
except Exception:
    openai = None

class LLMAdapter:
    """Simple adapter that uses OpenAI if an API key is present, otherwise returns mock responses.

    Usage:
        adapter = LLMAdapter(model="gpt-3.5-turbo")
        response = adapter.chat(messages)
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_mock = os.getenv("USE_MOCK_LLM", "").lower() in ("1", "true") or not bool(self.api_key)
        if not self.use_mock and openai is not None:
            # Configure the OpenAI client
            try:
                openai.api_key = self.api_key
            except Exception:
                pass

    def chat(self, messages, temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Call the LLM or return a mock response if no API key.

        messages should be a list of dicts with 'role' and 'content'.
        """
        if self.use_mock:
            # Build a compact mock reply that is useful for local testing.
            user_texts = [m.get("content", "") for m in messages if m.get("role") in ("user", "system")]
            joined = " | ".join([t.strip() for t in user_texts if t.strip()])
            sample = joined[:800]
            return f"[MOCK RESPONSE]\nBased on: {sample}\n\n(Enable real LLM by setting OPENAI_API_KEY or USE_MOCK_LLM=0)"

        if openai is None:
            return "Error: openai package not available. Install openai or set USE_MOCK_LLM=1"

        # Try multiple OpenAI client patterns to support different SDK versions.
        try:
            # If the newer OpenAI client class is available, use it.
            if hasattr(openai, "OpenAI"):
                client = openai.OpenAI(api_key=self.api_key)
                resp = client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                # response shape: resp.choices[0].message.content
                choice = resp.choices[0]
                if hasattr(choice, "message"):
                    return getattr(choice.message, "content", "") if not isinstance(choice.message, dict) else choice.message.get("content", "")

            # Fallback to older style
            if hasattr(openai, "ChatCompletion"):
                resp = openai.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                choice = resp.choices[0]
                # older responses sometimes provide `message` or `text`
                if isinstance(choice, dict):
                    if "message" in choice and isinstance(choice["message"], dict):
                        return choice["message"].get("content", "")
                    return choice.get("text", "")
                # attribute access
                if hasattr(choice, "message"):
                    return getattr(choice.message, "content", "")

            # If we reach here, the SDK didn't match expected patterns
            return "Error calling OpenAI: unsupported openai SDK interface. Set USE_MOCK_LLM=1 to use mock responses."
        except Exception as e:
            # On any runtime error, return a helpful message instead of crashing.
            return f"Error calling OpenAI: {e}"
