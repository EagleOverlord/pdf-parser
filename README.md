# PDF OCR & Summarisation Pipeline

A Python-based tool that converts PDF documents to images, performs OCR (Optical Character Recognition) using local LLM models via Ollama, and optionally summarises the extracted text.

## Features

- **PDF to Image Conversion** — Converts multi-page PDFs into individual JPEG images
- **OCR Processing** — Extracts text from images using vision-capable LLMs (default: `deepseek-ocr`)
- **Text Summarisation** — Optionally summarises extracted text using a configurable LLM (default: `granite4`)
- **Configurable Settings** — All model and processing options controlled via `settings.ini`
- **Logging** — Tracks processing times and errors

## Requirements

### Python Dependencies

```
pdf2image
Pillow
lmstudio
ollama
```

Install with:
```bash
pip install -r requirements.txt
```

### System Dependencies

- **Poppler** — Required by `pdf2image` for PDF rendering
  - macOS: `brew install poppler`
  - Ubuntu/Debian: `apt install poppler-utils`
  - Windows: Download from [poppler releases](https://github.com/osber/poppler-for-windows/releases) and add to PATH

- **Ollama** — Required for running local LLM models
  - Install from [ollama.ai](https://ollama.ai)
  - Pull required models:
    ```bash
    ollama pull deepseek-ocr:latest
    ollama pull granite4:latest
    ```

## Configuration

Edit `config/settings.ini` to customise behaviour:

```ini
[Summarisation]
enable_summarisation = True          # Toggle summarisation on/off
sum_model_name = granite4:latest     # Ollama model for summarisation
sum_context_length = 32000           # Context window size

[OCR]
ocr_service = ollama                 # OCR service provider
ocr_model_name = deepseek-ocr:latest # Ollama model for OCR
ocr_context_length = 8000            # Context window size
ocr_file_format = .txt               # Output file format
ocr_output_directory = ./output      # Directory containing images to OCR
```

## Usage

1. Place your PDF files in the `./input` directory

2. Run the pipeline:
   ```bash
   cd src
   python main.py
   ```

3. Find your results in:
   - `./output/` — Converted page images
   - `./output/text/` — Extracted text from each page
   - `./output/summarise/` — Summarised versions (if enabled)

## Processing Pipeline

1. **Initialisation** — Creates required directories and log file
2. **PDF → Image** — Each PDF page becomes a separate JPEG in `./output/`
3. **Image → Text** — OCR model processes each image, saves text to `./output/text/`
4. **Text → Summary** — (Optional) Summarisation model condenses each text file

## Logging

Processing logs are written to `./log/log.txt`, including:
- Start timestamp
- Import confirmation
- Directory creation status
- Processing times for each stage
- Any errors encountered

## Troubleshooting

**Model not found error**: The tool will prompt you to install missing Ollama models automatically.

**Poppler not found**: Ensure Poppler is installed and accessible in your system PATH.

**Out of memory**: Reduce `context_length` values in `settings.ini` or use smaller models.

## License

This project is provided as-is for personal and educational use.
