from googletrans import Translator
from pathlib import Path
import re
import shutil

translator = Translator()

src_dir = Path("_posts")
dest_dir = Path("blog-en/_posts")
dest_dir.mkdir(parents=True, exist_ok=True)

# Directory per le immagini
src_images_dir = Path("assets/images/posts")
dest_images_dir = Path("blog-en/assets/images/posts")
dest_images_dir.mkdir(parents=True, exist_ok=True)

def slugify_english(text):
    """Converte testo in slug URL-friendly"""
    # Rimuovi caratteri speciali e converti in minuscolo
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Sostituisci spazi con trattini
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

def extract_images_from_post(post_content, front_matter):
    """Estrae la lista di immagini referenziate nel post"""
    images = set()
    
    # Cerca immagini nel front matter (campo image:)
    image_match = re.search(r'image:\s*["\']?(/assets/images/posts/[^"\'\n]+)["\']?', front_matter)
    if image_match:
        image_path = image_match.group(1).strip()
        image_name = image_path.replace('/assets/images/posts/', '')
        images.add(image_name)
    
    # Cerca immagini nel contenuto markdown (![alt](/assets/images/posts/...))
    content_images = re.findall(r'!\[.*?\]\((/assets/images/posts/[^)]+)\)', post_content)
    for img_path in content_images:
        image_name = img_path.replace('/assets/images/posts/', '')
        images.add(image_name)
    
    return images

def copy_images_from_post(post_content, front_matter):
    """Copia le immagini referenziate nel post e nel front matter"""
    images_to_copy = extract_images_from_post(post_content, front_matter)
    
    # Copia le immagini
    for image_name in images_to_copy:
        src_image = src_images_dir / image_name
        dest_image = dest_images_dir / image_name
        
        if src_image.exists():
            if not dest_image.exists():
                shutil.copy2(src_image, dest_image)
                print(f"   📸 Copied image: {image_name}")
        else:
            print(f"   ⚠️  Warning: Image not found: {image_name}")
    
    return images_to_copy

# Ottieni lista dei post italiani
italian_posts = set(post.name for post in src_dir.glob("*.md"))

# Raccogli tutte le immagini usate nei post italiani esistenti
def get_all_used_images():
    """Restituisce il set di tutte le immagini utilizzate nei post esistenti"""
    used_images = set()
    for post in src_dir.glob("*.md"):
        text = post.read_text(encoding="utf-8")
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                content = parts[2]
                images = extract_images_from_post(content, fm)
                used_images.update(images)
    return used_images

# Ottieni tutte le immagini attualmente in uso
images_in_use = get_all_used_images()

# Rimuovi i post inglesi che non hanno più corrispondenza in italiano
print("🔍 Checking for deleted posts...")
for en_post in dest_dir.glob("*.md"):
    # Leggi il front matter per trovare original_file
    text = en_post.read_text(encoding="utf-8")
    original_match = re.search(r'original_file:\s*["\']?([^"\'\n]+)["\']?', text)
    
    if original_match:
        original_file = original_match.group(1).strip()
        if original_file not in italian_posts:
            print(f"🗑️  Deleting post: {en_post.name} (original {original_file} no longer exists)")
            
            # Estrai le immagini dal post prima di cancellarlo
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = parts[1]
                    content = parts[2]
                    images = extract_images_from_post(content, fm)
                    
                    # Cancella le immagini SOLO se non sono usate in altri post
                    for image_name in images:
                        if image_name not in images_in_use:
                            # Cancella dal blog inglese
                            dest_image = dest_images_dir / image_name
                            if dest_image.exists():
                                dest_image.unlink()
                                print(f"   🗑️  Deleted image from blog-en: {image_name}")
                            
                            # Cancella dal blog italiano
                            src_image = src_images_dir / image_name
                            if src_image.exists():
                                src_image.unlink()
                                print(f"   🗑️  Deleted image from blog: {image_name}")
                        else:
                            print(f"   ⚠️  Image {image_name} still in use, keeping it")
            
            # Cancella il post
            en_post.unlink()
    elif en_post.name not in italian_posts:
        # Fallback per vecchi post senza original_file
        print(f"🗑️  Deleting: {en_post.name} (no longer exists in Italian)")
        en_post.unlink()

# Traduci i nuovi post
print("🔄 Translating new posts...")
for post in src_dir.glob("*.md"):
    text = post.read_text(encoding="utf-8")
    
    # Controlla se il post è già stato tradotto cercando original_file
    already_translated = False
    for en_post in dest_dir.glob("*.md"):
        en_text = en_post.read_text(encoding="utf-8")
        original_match = re.search(r'original_file:\s*["\']?([^"\'\n]+)["\']?', en_text)
        if original_match and original_match.group(1).strip() == post.name:
            already_translated = True
            break
    
    if already_translated:
        continue

    # Separa front matter e contenuto
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = parts[1]
        content = parts[2]
    else:
        fm, content = "", text

    print(f"📝 Translating: {post.name}")
    
    # Traduci il titolo nel front matter
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', fm)
    translated_title = ""
    if title_match:
        original_title = title_match.group(1).strip()
        translated_title = translator.translate(original_title, src="it", dest="en").text
        fm = re.sub(r'(title:\s*["\']?)([^"\'\n]+)(["\']?)', 
                    rf'\1{translated_title}\3', fm)
    
    # Aggiungi original_file al front matter
    fm = fm.rstrip() + f'\noriginal_file: "{post.name}"\n'
    
    # Traduci il contenuto
    translated_content = translator.translate(content, src="it", dest="en").text
    
    # Copia le immagini referenziate nel post
    copy_images_from_post(content, fm)
    
    # Crea il nuovo nome del file con slug inglese
    # Estrai la data dal nome del file (YYYY-MM-DD)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', post.name)
    if date_match and translated_title:
        date_prefix = date_match.group(1)
        english_slug = slugify_english(translated_title)
        new_filename = f"{date_prefix}-{english_slug}.md"
    else:
        new_filename = post.name  # Fallback al nome originale
    
    dest_file = dest_dir / new_filename
    dest_file.write_text(f"---{fm}---\n{translated_content}", encoding="utf-8")
    print(f"   ✓ Created: {new_filename}")

print("✅ All posts synchronized with English repo!")
