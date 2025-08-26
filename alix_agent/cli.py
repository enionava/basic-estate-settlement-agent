import argparse
import json
import os
from typing import List
from .router import process_pdf
from rich.console import Console

console = Console()

def iter_pdfs(input_path: str) -> List[str]:
    if os.path.isdir(input_path):
        out = []
        for root, _, files in os.walk(input_path):
            for f in files:
                if f.lower().endswith(".pdf"):
                    out.append(os.path.join(root, f))
        return sorted(out)
    else:
        return [input_path]

def main():
    parser = argparse.ArgumentParser(description="Alix Agent CLI")
    parser.add_argument("--input", required=True, help="PDF file or folder")
    args = parser.parse_args()

    pdfs = iter_pdfs(args.input)
    if not pdfs:
        console.print("[red]No PDFs found in the folder[/red]")
        return

    for p in pdfs:
        try:
            result = process_pdf(p)
            console.print_json(json.dumps(result))
        except Exception as e:
            console.print({"path": p, "error": str(e)})

if __name__ == "__main__":
    main()