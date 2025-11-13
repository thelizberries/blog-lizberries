from googletrans import Translator
from pathlib import Path
import re

translator = Translator()

src_dir = Path("_posts")
dest_dir = Path("blog-en/_posts")
dest_dir.mkdir(parents=True, exist_ok=True)

for post in src_dir.glob("*.md"):
    dest_file = dest_dir / post.name

    # Salta se il file esiste già (già tradotto)
    if dest_file.exists():
        continue

    text = post.read_text(encoding="utf-8")

    # Separa front matter e contenuto
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = parts[1]
        content = parts[2]
    else:
        fm, content = "", text

    print(f"Translating: {post.name}")
    
    # Traduci il titolo nel front matter
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', fm)
    if title_match:
        original_title = title_match.group(1).strip()
        translated_title = translator.translate(original_title, src="it", dest="en").text
        fm = re.sub(r'(title:\s*["\']?)([^"\'\n]+)(["\']?)', 
                    rf'\1{translated_title}\3', fm)
    
    # Traduci il contenuto
    translated_content = translator.translate(content, src="it", dest="en").text

    dest_file.write_text(f"---{fm}---\n{translated_content}", encoding="utf-8")

print("✅ All posts translated and copied to English repo!")
