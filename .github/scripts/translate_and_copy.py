try:
    import argostranslate.package
    import argostranslate.translate
except ImportError as exc:
    raise SystemExit(
        "Missing dependency 'argostranslate'. Install it with: pip install argostranslate"
    ) from exc
from pathlib import Path
import re
import shutil
import hashlib
import json
import os
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

class TranslationResult:
    def __init__(self, text):
        self.text = text


class DeepLApiTranslator:
    """Traduttore DeepL API opzionale con fallback su backend locale."""

    def __init__(self, api_key, timeout_seconds=20):
        self.api_key = api_key.strip()
        self.timeout_seconds = timeout_seconds
        # Le API key Free tipicamente terminano con ':fx'
        if self.api_key.endswith(":fx"):
            self.endpoint = "https://api-free.deepl.com/v2/translate"
        else:
            self.endpoint = "https://api.deepl.com/v2/translate"

    def translate(self, text, src="it", dest="en"):
        if text is None or text == "":
            return TranslationResult(text)

        payload = urllib_parse.urlencode(
            {
                "text": text,
                "source_lang": src.upper(),
                "target_lang": dest.upper(),
            }
        ).encode("utf-8")

        req = urllib_request.Request(
            self.endpoint,
            data=payload,
            headers={"Authorization": f"DeepL-Auth-Key {self.api_key}"},
            method="POST",
        )

        with urllib_request.urlopen(req, timeout=self.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))

        translated = data["translations"][0]["text"]
        return TranslationResult(translated)


class FreeOfflineTranslator:
    """Traduttore offline gratuito basato su Argos Translate."""

    def __init__(self):
        self._translation_cache = {}

    def _ensure_model_installed(self, src, dest):
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((lang for lang in installed_languages if lang.code == src), None)
        to_lang = next((lang for lang in installed_languages if lang.code == dest), None)

        if from_lang and to_lang:
            try:
                from_lang.get_translation(to_lang)
                return
            except Exception:
                pass

        print(f"⬇️ Installing Argos model {src}->{dest} (first run only)...")
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        package_to_install = next(
            (
                pkg
                for pkg in available_packages
                if pkg.from_code == src and pkg.to_code == dest
            ),
            None,
        )

        if package_to_install is None:
            raise RuntimeError(f"No Argos model available for {src}->{dest}")

        downloaded_path = package_to_install.download()
        argostranslate.package.install_from_path(downloaded_path)

    def _get_translation(self, src, dest):
        cache_key = (src, dest)
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]

        self._ensure_model_installed(src, dest)
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((lang for lang in installed_languages if lang.code == src), None)
        to_lang = next((lang for lang in installed_languages if lang.code == dest), None)

        if not from_lang or not to_lang:
            raise RuntimeError(f"Argos languages not installed for {src}->{dest}")

        translation = from_lang.get_translation(to_lang)
        self._translation_cache[cache_key] = translation
        return translation

    def _split_text(self, text, max_chars=1800):
        if len(text) <= max_chars:
            return [text]

        parts = re.split(r"(\n{2,})", text)
        chunks = []
        current = ""

        for part in parts:
            if len(current) + len(part) <= max_chars:
                current += part
                continue

            if current:
                chunks.append(current)

            if len(part) <= max_chars:
                current = part
            else:
                for i in range(0, len(part), max_chars):
                    chunks.append(part[i : i + max_chars])
                current = ""

        if current:
            chunks.append(current)

        return chunks

    def translate(self, text, src="it", dest="en"):
        if text is None or text == "":
            return TranslationResult(text)

        translation = self._get_translation(src, dest)
        chunks = self._split_text(text)
        translated_text = "".join(translation.translate(chunk) for chunk in chunks)
        return TranslationResult(translated_text)


class HybridTranslator:
    """Usa DeepL se configurato; in caso di errore ripiega su Argos offline."""

    def __init__(self, primary_translator, fallback_translator):
        self.primary_translator = primary_translator
        self.fallback_translator = fallback_translator

    def translate(self, text, src="it", dest="en"):
        try:
            return self.primary_translator.translate(text, src=src, dest=dest)
        except (urllib_error.URLError, urllib_error.HTTPError, TimeoutError, KeyError, ValueError):
            return self.fallback_translator.translate(text, src=src, dest=dest)
        except Exception:
            return self.fallback_translator.translate(text, src=src, dest=dest)


argos_translator = FreeOfflineTranslator()
deepl_api_key = os.getenv("DEEPL_API_KEY", "").strip()

if deepl_api_key:
    print("🌐 DeepL API key found: hybrid mode enabled (DeepL -> Argos fallback)")
    translator = HybridTranslator(
        primary_translator=DeepLApiTranslator(deepl_api_key),
        fallback_translator=argos_translator,
    )
else:
    print("🧠 No DEEPL_API_KEY set: using Argos offline mode")
    translator = argos_translator

src_dir = Path("_posts")
dest_dir = Path("blog-en/_posts")
dest_dir.mkdir(parents=True, exist_ok=True)

def protect_html_tags(text):
    """Estrae i tag HTML, traduce il contenuto, e li ricostruisce"""
    import re
    html_pattern = r'<a([^>]*)>(.*?)</a>'
    
    def translate_link_content(match):
        attributes = match.group(1)  # Gli attributi del tag (href, target, ecc.)
        link_text = match.group(2)   # Il testo dentro il tag
        
        # Traduce solo il testo, non gli attributi
        try:
            translated_text = translator.translate(link_text, src="it", dest="en").text
        except:
            translated_text = link_text  # Fallback se la traduzione fallisce
        
        # Aggiorna il locale nel link se presente
        if 'locale=it_IT' in attributes:
            attributes = attributes.replace('locale=it_IT', 'locale=en_US')
        
        # Normalizza gli spazi tra gli attributi (assicura uno spazio prima di ogni attributo)
        attributes = re.sub(r'(\S)(href|target|rel|style|class|id)=', r'\1 \2=', attributes)
        
        # Ricostruisce il tag con il testo tradotto
        return f'<a{attributes}>{translated_text}</a>'
    
    # Applica la traduzione a tutti i tag <a>
    translated_text = re.sub(html_pattern, translate_link_content, text, flags=re.DOTALL)
    
    # Ritorna il testo tradotto e un dizionario vuoto (per compatibilità con il codice esistente)
    return translated_text, {}

def restore_html_tags(text, placeholders):
    """Non più necessario - la traduzione avviene direttamente in protect_html_tags"""
    return text

def fix_spacing(text):
    """Sistema gli spazi dopo la punteggiatura"""
    import re
    # Aggiunge spazio dopo . ! ? se seguito da lettera maiuscola
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
    # Sistema spazi multipli
    text = re.sub(r' +', ' ', text)
    return text

APOSTROPHE_VARIANTS = "’‘‛`´ʻʼʹʽʾʿˈˊˋʺ＇"

def normalize_single_quotes(text):
    """Normalizza tutti i tipi di apostrofo nel carattere ASCII singolo (')."""
    if not text:
        return text
    translation_table = str.maketrans({ch: "'" for ch in APOSTROPHE_VARIANTS})
    normalized = text.translate(translation_table)
    # Evita sequenze come '' o anche '   ' che possono creare problemi di parsing YAML
    normalized = re.sub(r"'(\s*)'", "'", normalized)
    normalized = re.sub(r"'{2,}", "'", normalized)
    # Rimuove apostrofi orfani usati come quote isolate prima di una parola
    normalized = re.sub(r"(^|\s)'\s+(?=\w)", r"\1", normalized)
    return normalized

def read_front_matter_value(fm, key):
    """Legge un valore one-line dal front matter YAML per la chiave richiesta."""
    match = re.search(rf'^{key}:\s*(.*)$', fm, re.MULTILINE)
    if not match:
        return None
    raw_value = match.group(1).strip()
    if len(raw_value) >= 2 and ((raw_value[0] == '"' and raw_value[-1] == '"') or (raw_value[0] == "'" and raw_value[-1] == "'")):
        raw_value = raw_value[1:-1]
    return raw_value.strip()

def write_front_matter_value(fm, key, value):
    """Scrive un valore one-line nel front matter YAML con escaping sicuro."""
    safe_value = value.replace('\\', '\\\\').replace('"', '\\"')
    return re.sub(rf'^{key}:\s*.*$', f'{key}: "{safe_value}"', fm, count=1, flags=re.MULTILINE)

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
                        print(f"   🔍 Checking image: {image_name}")
                        print(f"   📋 Images in use: {images_in_use}")
                        if image_name not in images_in_use:
                            # Cancella dal blog inglese
                            dest_image = dest_images_dir / image_name
                            if dest_image.exists():
                                dest_image.unlink()
                                print(f"   🗑️  Deleted image from blog-en: {image_name}")
                            else:
                                print(f"   ⚠️  Image not found in blog-en: {image_name}")
                            
                            # Cancella dal blog italiano
                            src_image = src_images_dir / image_name
                            if src_image.exists():
                                src_image.unlink()
                                print(f"   🗑️  Deleted image from blog: {image_name}")
                            else:
                                print(f"   ⚠️  Image not found in blog: {image_name}")
                        else:
                            print(f"   ⚠️  Image {image_name} still in use, keeping it")
            
            # Cancella il post
            en_post.unlink()
    elif en_post.name not in italian_posts:
        # Fallback per vecchi post senza original_file
        print(f"🗑️  Deleting: {en_post.name} (no longer exists in Italian)")
        en_post.unlink()

# Traduci i nuovi post e aggiorna quelli modificati
print("🔄 Translating new posts and updating modified ones...")
for post in src_dir.glob("*.md"):
    text = post.read_text(encoding="utf-8")
    
    # Controlla se il post è già stato tradotto cercando original_file
    existing_en_post = None
    for en_post in dest_dir.glob("*.md"):
        en_text = en_post.read_text(encoding="utf-8")
        original_match = re.search(r'original_file:\s*["\']?([^"\'\n]+)["\']?', en_text)
        if original_match and original_match.group(1).strip() == post.name:
            existing_en_post = en_post
            break
    
    # Separa front matter e contenuto
    if text.startswith("---"):
        parts = text.split("---", 2)
        fm = parts[1]
        content = parts[2]
    else:
        fm, content = "", text

    # Se esiste già, controlla se è stato modificato
    if existing_en_post:
        # Calcola l'hash del contenuto italiano corrente
        current_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
        
        # Leggi l'hash salvato nel post inglese
        en_text = existing_en_post.read_text(encoding="utf-8")
        saved_hash_match = re.search(r'source_hash:\s*["\']?([^"\'\n]+)["\']?', en_text)
        
        if saved_hash_match and saved_hash_match.group(1).strip() == current_hash:
            # Il contenuto non è cambiato, salta la traduzione
            continue
        else:
            print(f"🔄 Updating: {post.name}")
            # Cancella il vecchio file (verrà ricreato con il nome aggiornato)
            existing_en_post.unlink()
            print(f"🗑️ Deleted old version: {existing_en_post.name}")
    else:
        print(f"📝 Translating: {post.name}")
    
    # Traduci il titolo nel front matter
    translated_title = ""
    original_title = read_front_matter_value(fm, "title")
    if original_title:
        translated_title = translator.translate(original_title, src="it", dest="en").text
        translated_title = normalize_single_quotes(translated_title)
        fm = write_front_matter_value(fm, "title", translated_title)
    
    # Traduci la descrizione nel front matter (REGEX CORRETTA)
    # Usa una regex che cattura tutto tra i delimitatori, anche con virgolette tipografiche interne
    original_description = read_front_matter_value(fm, "description")
    if original_description:
        translated_description = translator.translate(original_description, src="it", dest="en").text
        translated_description = normalize_single_quotes(translated_description)
        fm = write_front_matter_value(fm, "description", translated_description)
    
    # Aggiungi original_file e hash del sorgente al front matter
    current_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    fm = fm.rstrip() + f'\noriginal_file: "{post.name}"\nsource_hash: "{current_hash}"\n'
    
    # Proteggi i tag HTML prima della traduzione
    protected_content, html_placeholders = protect_html_tags(content)
    
    # Traduci il contenuto
    translated_content = translator.translate(protected_content, src="it", dest="en").text
    
    # Ripristina i tag HTML
    translated_content = restore_html_tags(translated_content, html_placeholders)
    
    # Sistema gli spazi dopo la punteggiatura
    translated_content = fix_spacing(translated_content)
    
    # Copia le immagini referenziate nel post
    copy_images_from_post(content, fm)
    
    # Crea il nuovo nome del file con slug inglese
    # Estrai la data dal nome del file (YYYY-MM-DD)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', post.name)
    if date_match and translated_title:
        date_prefix = date_match.group(1)
        # Rimuovi gli apostrofi normalizzati prima di creare lo slug
        title_for_slug = normalize_single_quotes(translated_title).replace("'", "")
        english_slug = slugify_english(title_for_slug)
        new_filename = f"{date_prefix}-{english_slug}.md"
    else:
        new_filename = post.name  # Fallback al nome originale
    
    dest_file = dest_dir / new_filename
    dest_file.write_text(f"---{fm}---\n{translated_content}", encoding="utf-8")
    print(f"   ✓ Created: {new_filename}")

print("✅ All posts synchronized with English repo!")
