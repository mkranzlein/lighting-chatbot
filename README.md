# lighting-chatbot
Chatbot prototype for providing users with lighting product information

![architecture diagram for lighting chatbot](assets/Architecture.svg)

## Setup
### Environment
#### pyenv

```bash
pyenv virtualenv 3.13 lighting-chatbot
```

```bash
pyenv activate lighting-chatbot
```

#### venv
```bash
python3 -m venv lighting-chatbot
```

```bash
source lighting-chatbot/bin/activate
```

### Install dependencies and `lighting-chatbot`
```bash
pip install -r requirements.txt
```

```bash
pip install .
```

### Ollama
1. Install [Ollama](https://ollama.com/) for running OLMoE locally.

    MacOS:
    ```bash
    brew install ollama
    ```

    Bash
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
2. Start Ollama in a separate terminal window.
    ```bash
    ollama serve
    ```

3. Pull [OLMoE model](https://huggingface.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF).
    ```bash
    ollama pull hf.co/allenai/OLMoE-1B-7B-0125-Instruct-GGUF:Q4_K_M
    ```

## Running the chatbot
```bash
python scripts/run_chatbot.py
```

## Running from scratch
The chatbot is directly runnable after setup. However, if you'd like, you can delete the `chroma_db` directory and `spec_sheets_text` directory in `./data/`. To recreate these deleted directories, run:

```bash
python scripts/extract_text_from_pdfs.py
```

And then:

```bash
python scripts/embed_extracted_text.py
```

Finally, with the text extracted and embeddings saved, the chatbot can be run as before:

```bash
python scripts/run_chatbot.py
```