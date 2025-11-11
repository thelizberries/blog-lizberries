from googletrans import Translator
import os
from pathlib import Path

translator = Translator()

src_dir = Path("_posts")
dest_dir = Path("en/_posts")
dest_dir.mkdir(parents=True, exist_ok=True)

for post in src_dir.glob("*.md"):
    dest_file = dest_dir / post.name

    # Salta i post già tradotti
    if dest_file.exists():
        continue

    text = post.read_text(encoding="utf-8")

    # Separa il front matter (--- ... ---)
    if text.startswith("---"):
        parts = text.split("---", 2)
        front_matter = parts[1]
        content = parts[2]
    else:
        front_matter = ""
        content = text

    translated_content = translator.translate(content, src="it", dest="en").text
    result = f"---{front_matter}---\n{translated_content}"
    dest_file.write_text(result, encoding="utf-8")

print("✅ All posts translated successfully!")
