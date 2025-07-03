---
language:
- en
- fr
- de
- es
- pt
- it
- ja
- ko
- ru
- zh
- ar
- fa
- id
- ms
- ne
- pl
- ro
- sr
- sv
- tr
- uk
- vi
- hi
- bn
license: apache-2.0
library_name: llama.ccp
inference: false
base_model:
- mistralai/Magistral-Small-2506
extra_gated_description: >-
  If you want to learn more about how we process your personal data, please read
  our <a href="https://mistral.ai/terms/">Privacy Policy</a>.
pipeline_tag: text2text-generation
---


> [!Note]
> At Mistral, we don't yet have too much experience with providing GGUF-quantized checkpoints
> to the community, but want to help improving the ecosystem going forward.
> If you encounter any problems with the provided checkpoints here, please open a discussion or pull request


# Magistral-Small-2506 (gguf)

Building upon Mistral Small 3.1 (2503), **with added reasoning capabilities**, undergoing SFT from Magistral Medium traces and RL on top, it's a small, efficient reasoning model with 24B parameters.

Magistral-Small-2506_gguf is a GGUF (quantized) version of [Magistral-Small-2506](https://huggingface.co/mistralai/Magistral-Small-2506).

Learn more about Magistral in our [blog post](https://mistral.ai/news/magistral).


## Key Features:
- **Reasoning**:  Capable of long chains of reasoning traces before providing an answer.
- **lightweight**: with its compact size of just 24 billion parameters, Magistral is light enough to run on a single RTX 4090 or a Mac with 32GB RAM once quantized, making it an appropriate model for local deployment and on-device use.
- **Apache 2.0 License**: Open license allowing usage and modification for both commercial and non-commercial purposes.
- **Context Window**: We recommend setting the context window to **40k**. We converted the original weights to gguf with this requirement. Theoretically, an even larger 128k context window is supported but untested.
- **Tokenizer**: Utilizes a Tekken tokenizer with a 131k vocabulary size.

## Benchmarks Results

Please see the [original model card](https://huggingface.co/mistralai/Magistral-Small-2506#benchmark-results) for benchmarks results.

## Usage

We recommend to use **Magistral-Small-2506_gguf** with [llama.ccp](https://github.com/ggml-org/llama.cpp). Follow the install or build instructions to get started.


**`Magistral-Small-2506_gguf` does not support function calling.**

In the rest of this usage guide, we assume you have the `llama-cli` and `llama-server` binaries available.

### Download the model

Download the weights from the huggingface hub using the `huggingface-cli`:

```sh
pip install -U "huggingface_hub[cli]"

huggingface-cli download \
"mistralai/Magistral-Small-2506_gguf" \
--local-dir "mistralai/Magistral-Small-2506_gguf/"
```

### llama-cli

You can interact with the model using the `llama-cli`'s llama.ccp tool. Make sure to add `--jinja` to use our tokenizer.
It uses the default system prompt for Magistral. 

The default system prompt is in English, but you can customize it if you want by passing the `-sys "your_system_prompt"` argument to `llama-cli`.

By default, the context size of llama.ccp is 4096, but you can increase it to 40,960. We also recommend to set the temperature to `0.7` and the top_p to `0.95`.

```bash
llama-cli --jinja \
-m mistralai/Magistral-Small-2506_gguf/Magistral-Small-2506_Q8_0.gguf \
--ctx-size 40960 \
--temp 0.7 \
--top_p 0.95
# -sys "your_system_prompt" \
```

Now you can pass to the model the [prompt examples](#prompt-examples) or your own prompts !

### llama-server

You can also use the `llama-server` to run the model as a server. Make sure to add `--jinja` to use our tokenizer and increase the context size to 40,960.

We also recommend to set the temperature to `0.7` and the top_p to `0.95`.


```bash
llama-server --jinja \
-m mistralai/Magistral-Small-2506_gguf/Magistral-Small-2506_Q8_0.gguf \
--ctx-size 40960
```


Now you can interact with the model directly where it is served in the browser, via curl or by using the OpenAI client.

```python
from huggingface_hub import hf_hub_download
import openai

client = openai.OpenAI(
    base_url="http://<your-url>:8080/v1",
    api_key="not-needed",
)

def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    return system_prompt

SYSTEM_PROMPT = load_system_prompt("mistralai/Magistral-Small-2506_gguf", "SYSTEM_PROMPT.txt")

completion = client.chat.completions.create(
  model="Magistral-Small-2506_Q8_0.gguf",
  messages=[
	# The following line is not required if you use the default system prompt.
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "How many 'r' are in strawberry?"}
  ],
  temperature=0.7,
  top_p=0.95,
  stream=True
)

print("client: Start streaming chat completions...")
printed_content = False

for chunk in completion:
  content = None
  if hasattr(chunk.choices[0].delta, "content"):
    content = chunk.choices[0].delta.content

  if content is not None:
    if not printed_content:
        printed_content = True
        print("\ncontent:", end="", flush=True)
    # Extract and print the content
    print(content, end="", flush=True)
```

Use the [prompt examples](#prompt-examples) or your own prompts !

## Prompt Examples

Here is a list of questions to help you test the model.

1. `How many "r" are in strawberry?`
	
	The answer is `3`.

2. `John is one of 4 children. The first sister is 4 years old. Next year, the second sister will be twice as old as the first sister. The third sister is two years older than the second sister. The third sister is half the age of her older brother. How old is John?`

	The answer is `22`.

3. `9.11 and 9.8, which is greater?`
	
	The answer is `9.8`.
