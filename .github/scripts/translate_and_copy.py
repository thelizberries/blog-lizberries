from googletrans import Translator
from pathlib import Path

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
    translated = translator.translate(content, src="it", dest="en").text

    dest_file.write_text(f"---{fm}---\n{translated}", encoding="utf-8")

print("✅ All posts translated and copied to English repo!")
