import json
import urllib.request
import urllib.error

class DeepSeekClient:
    def __init__(self, model_name="deepseek-chat"):
        """
        Initializes the client for DeepSeek.
        DeepSeek API is OpenAI-compatible natively.
        """
        self.model_name = model_name
        self.base_url = "https://api.deepseek.com/chat/completions"

    def ask(self, api_key: str, contents: list, system_instruction: dict = None) -> dict:
        """
        Acts as an adapter. Accepts exactly the same parameters as Gemini v00.
        Translates schema, executes natively via urllib, and returns an identical dictionary structure.
        """
        if not api_key:
            raise ValueError("Clé API DeepSeek manquante.")

        # --- 1. Schema Translation (Gemini format to DeepSeek/OpenAI format) ---
        messages = []
        
        # Translate system instruction
        if system_instruction:
            try:
                # v00 passes system_instruction as {"parts": [{"text": "..."}]}
                sys_text = system_instruction["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                sys_text = str(system_instruction)
            messages.append({"role": "system", "content": sys_text})
            
        # Translate chat history
        for msg in contents:
            role = "assistant" if msg.get("role") == "model" else "user"
            try:
                text = msg["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                text = str(msg)
            messages.append({"role": role, "content": text})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "thinking": {"type": "enabled"},
            "reasoning_effort": "high"
        }

        data = json.dumps(payload).encode('utf-8')
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method='POST')

        # --- 2. Network Execution ---
        try:
            with urllib.request.urlopen(req, timeout=300) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                # --- [ARCHITECTURAL PROOF] ---
                returned_model = result.get("model", "unknown_model")
                print(f"\n[DEEPSEEK API TELEMETRY] The server processed this request using model: '{returned_model}'\n")

                # --- 3. Pure Passthrough (No Regex/Sanitization) ---
                try:
                    raw_answer = result["choices"][0]["message"]["content"]
                except (KeyError, IndexError):
                    raise ValueError(f"Format de réponse inattendu de DeepSeek: {result}")

                # --- 4. Accurate Token Metric Extraction & Calculation ---
                usage = result.get("usage", {})
                prompt_tokens = usage.get("prompt_tokens", 0)
                cache_hit = usage.get("prompt_cache_hit_tokens", 0)
                
                # Calculate miss safely to ensure (hit + miss) perfectly equals billed prompt_tokens
                cache_miss = usage.get("prompt_cache_miss_tokens", prompt_tokens - cache_hit)
                out_tokens = usage.get("completion_tokens", 0)
                
                return {
                    "answer": raw_answer, # Untouched text to allow frontend Markdown parsing
                    "model_proof": returned_model, # Safely exposed for potential future frontend UI badges
                    "usage": {
                        "in": prompt_tokens,     # Total input tokens
                        "out": out_tokens,       # Total output tokens
                        "cache": cache_hit,      # Cache hits explicitly tracked
                        "cache_miss": cache_miss # Cache misses for precise billing alignment
                    }
                }
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise ConnectionError(f"HTTP {e.code}: {error_body}") from e
        except Exception as e:
            raise ConnectionError(f"Erreur réseau DeepSeek: {e}") from e
