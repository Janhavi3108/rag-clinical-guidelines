import time
import ollama

MODEL = "qwen2.5:3b"
QUESTION = "Explain in three sentences what cervical cancer screening is."

for run in (1, 2):
    start = time.time()
    r = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": QUESTION}],
        options={"num_ctx": 2048, "num_predict": 200},
    )
    print(f"run {run}: {time.time() - start:.1f} s")

print(r["message"]["content"])