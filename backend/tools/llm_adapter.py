import os
import logging
import traceback
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
            # First, prefer the newer `openai.OpenAI` class if it's available.
            if hasattr(openai, "OpenAI"):
                try:
                    # Some SDK versions expect no args in constructor; others accept api_key.
                    try:
                        client = openai.OpenAI()
                    except TypeError:
                        # Last-resort: set global api key and instantiate without args
                        if hasattr(openai, "api_key"):
                            openai.api_key = self.api_key
                        else:
                            os.environ["OPENAI_API_KEY"] = self.api_key
                        client = openai.OpenAI()

                    # If client has an attribute to set api_key, do it.
                    if hasattr(client, "api_key"):
                        try:
                            client.api_key = self.api_key
                        except Exception:
                            # ignore if not settable
                            pass

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

                except TypeError:
                    # Fall through to legacy path if constructor signature mismatches
                    pass

            # If the newer OpenAI client is not available, do not attempt to access
            # the removed `openai.ChatCompletion` symbol directly because newer
            # `openai` packages raise an explanatory error when that attribute is
            # referenced. Instead, provide a clear message advising migration or
            # pinning to an older client.
            if not hasattr(openai, "OpenAI"):
                return (
                    "Error calling OpenAI: detected openai-python SDK that does not expose\n"
                    "the modern `OpenAI` client. Please either run `openai migrate` to\n"
                    "upgrade your codebase to the 1.0+ interface or pin the older\n"
                    "client with `pip install openai==0.28`.\n"
                    "See https://github.com/openai/openai-python/discussions/742 for details."
                )

            # If we've fallen through and the newer client existed but something
            # else failed, return a generic error (caught by outer except).
            return "Error calling OpenAI: unable to call OpenAI client (see inner error)."
        except Exception as e:
            # Log the full exception and stacktrace to server logs for debugging.
            logging.exception("OpenAI client call failed")
            # If DEBUG_LLM is set, return a short, non-sensitive inner error to help
            # debugging during development. Do NOT enable in production.
            debug_mode = os.getenv("DEBUG_LLM", "0").lower() in ("1", "true")
            if debug_mode:
                short = f"{type(e).__name__}: {str(e)}"
                # Truncate to avoid huge dumps
                return f"Error calling OpenAI: {short[:1000]}"

            # Avoid returning raw exception traces to users (may contain sensitive info).
            return "Error calling OpenAI: unable to call OpenAI client (see server logs for details)."
