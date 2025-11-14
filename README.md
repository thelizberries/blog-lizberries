# Lizberries Blog - Guida per la Creazione dei Post

Benvenuto nella guida per creare e pubblicare post sul blog dei Lizberries! Questa guida ti accompagnerà passo dopo passo nella creazione di nuovi articoli.

---

## ⚡ GUIDA RAPIDA - Per chi non è pratico di GitHub

**Il modo più semplice per scrivere e pubblicare un post:**

### 1️⃣ Vai su https://prose.io/
### 2️⃣ Clicca "Authorize on GitHub" e fai login
### 3️⃣ Seleziona il repository "thelizberries/blog"
### 4️⃣ Clicca sulla cartella "_posts"
### 5️⃣ Clicca "New File" (in alto a destra)
### 6️⃣ Scrivi il contenuto del post nell'editor
### 7️⃣ Clicca sull'icona dei metadati (📋) a destra e compila:
   - **Title**: Titolo del post
   - **Date**: Data (formato: 2025-11-15)
   - (opzionale) **Image**: /assets/images/nome-immagine.estenzione_immagine
### 8️⃣ Clicca "Save" (💾 in alto a destra)
### 9️⃣ **Fatto!** Il post verrà pubblicato automaticamente

**📸 Per aggiungere immagini:**

**IMPORTANTE**: Prose.io non permette di scegliere la cartella di destinazione per le immagini. 

**Metodo consigliato per caricare immagini con Prose.io:**

1. **Prima di scrivere il post**, carica le immagini:
   - Vai su https://github.com/thelizberries/blog
   - Naviga nella cartella `assets/images/`
   - Clicca "Add file" → "Upload files"
   - Trascina le tue immagini (qualsiasi formato: `.jpg`, `.jpeg`, `.png`)
   - Clicca "Commit changes"

2. **Attendi 1-2 minuti**: Le immagini verranno **convertite automaticamente in formato `.webp`** (ottimizzato per il web)

3. **Poi scrivi il post in Prose.io** e referenzia le immagini convertite:
   - Nel campo "Image" dei metadati: `/assets/images/nome-immagine.webp` (usa l'estensione `.webp` anche se hai caricato `.jpg`)

**Nota**: Le immagini verranno copiate automaticamente anche nel blog inglese durante la traduzione!

**⏱️ Tempi di pubblicazione:**
- Il post appare sul blog italiano in 1-2 minuti
- Dopo altri 1-2 minuti appare tradotto automaticamente sul blog inglese

---

## 📝 Struttura del Blog (Per Utenti Tecnici)

Il blog è costruito con Jekyll e GitHub Pages. I post vengono scritti in formato Markdown e pubblicati automaticamente su:
- **Blog Italiano**: https://blog.lizberries.thelizards.it
- **Blog Inglese**: https://blog-en.lizberries.thelizards.it (tradotto automaticamente)

## 🚀 Come Creare un Nuovo Post

### 1. Creare il File del Post

I post vanno creati nella cartella `_posts/` con questa convenzione di naming:

```
YYYY-MM-DD-titolo-del-post.md
```

**Esempio**: `2025-11-15-nuovo-concerto-milano.md`

⚠️ **Importante**: 
- La data deve essere in formato `YYYY-MM-DD` (anno-mese-giorno)
- Il titolo deve usare trattini `-` al posto degli spazi
- L'estensione deve essere `.md`

### 2. Struttura del Post

Ogni post deve iniziare con il **front matter** (metadati racchiusi tra `---`):

#### Post SENZA immagine:

```markdown
---
layout: post
title: "Titolo del Post"
date: 2025-11-15
---

Inserisci qui il testo del post...

<!--more-->

Continua con il resto del contenuto...
```

#### Post CON immagine:

```markdown
---
layout: post
title: "Titolo del Post"
date: 2025-11-15
image: /assets/images/nome-immagine.webp
---

Inserisci qui il testo del post...

<!--more-->

Continua con il resto del contenuto...
```

### 3. Componenti del Front Matter

- **layout**: Sempre `post` (obbligatorio)
- **title**: Il titolo del post tra virgolette (obbligatorio)
- **date**: La data nel formato `YYYY-MM-DD` (obbligatorio)
- **image**: Percorso dell'immagine di anteprima (opzionale)

### 4. Tag `<!--more-->`

Il tag `<!--more-->` separa l'anteprima (excerpt) dal resto del contenuto:
- Il testo **prima** del tag appare nella home del blog come anteprima
- Il testo **dopo** il tag appare solo nell'articolo completo

## 🖼️ Gestione delle Immagini

### Aggiungere un'Immagine al Post

1. **Salva l'immagine** nella cartella `assets/images/`
2. **Formati supportati**: `.jpg`, `.jpeg`, `.png` (verranno convertiti automaticamente in `.webp`)
3. **Naming**: Usa nomi descrittivi con trattini, es: `concerto-milano-2025.jpg`
4. **Conversione automatica**: Dopo 1-2 minuti dal caricamento, l'immagine sarà disponibile in formato `.webp`
5. **Aggiungi nel front matter** (usa sempre `.webp` come estensione): 
   ```yaml
   image: /assets/images/nome-immagine.webp
   ```

### Immagine di Default

Se non specifichi un'immagine, verrà usato automaticamente il logo dei Lizberries.

## 📤 Pubblicare il Post

### Metodo 1: Tramite Git (Command Line)

1. **Aggiungi il file al repository**:
   ```bash
   git add _posts/2025-11-15-nuovo-concerto-milano.md
   ```

2. **Se hai aggiunto immagini**:
   ```bash
   git add assets/images/nome-immagine.webp
   ```

3. **Crea il commit**:
   ```bash
   git commit -m "Aggiungi post: Nuovo concerto a Milano"
   ```

4. **Pusha su GitHub**:
   ```bash
   git push origin main
   ```

### Metodo 2: Tramite GitHub Web Interface

1. Vai su https://github.com/thelizberries/blog
2. Naviga nella cartella `_posts/`
3. Clicca su "Add file" → "Upload files"
4. Carica il file `.md` del post
5. Scrivi un messaggio di commit
6. Clicca su "Commit changes"

## 🌐 Traduzione Automatica

Quando pubblichi un post in italiano:

1. **GitHub Actions** rileva il nuovo post
2. Lo **traduce automaticamente** in inglese
3. **Copia automaticamente le immagini** dal post italiano al blog inglese
4. Lo pubblica sul blog inglese con:
   - Titolo tradotto
   - Contenuto tradotto
   - Nome file tradotto (SEO-friendly)
   - Immagini copiate in `assets/images/`
   - Link al post originale italiano

⏱️ La traduzione richiede circa 1-2 minuti dopo il push.

**Nota**: Non devi fare nulla per le immagini! Se le hai caricate in `assets/images/` nel blog italiano, verranno copiate automaticamente nel blog inglese.

## ✏️ Formattazione Markdown

Ecco alcuni esempi di formattazione che puoi usare nei post:

### Titoli
```markdown
## Titolo di Sezione
### Sottotitolo
```

### Testo
```markdown
**Grassetto**
*Corsivo*
[Link](https://www.example.com)
```

### Liste
```markdown
- Elemento 1
- Elemento 2
- Elemento 3
```

### Liste Numerate
```markdown
1. Primo punto
2. Secondo punto
3. Terzo punto
```

### Citazioni
```markdown
> Questa è una citazione
```

### Immagini nel Contenuto
```markdown
![Descrizione immagine](/assets/images/nome-immagine.webp)
```

## 🔄 Workflow Completo

1. ✍️ Scrivi il post in Markdown
2. 📁 Salva il file in `_posts/` con il formato `YYYY-MM-DD-titolo.md`
3. 🖼️ (Opzionale) Aggiungi immagini in `assets/images/`
4. 💾 Fai commit e push su GitHub
5. ⏳ Attendi 1-2 minuti per la build di GitHub Pages
6. ✅ Il post appare sul blog italiano
7. 🌍 Dopo altri 1-2 minuti, appare tradotto sul blog inglese

## 📋 Esempio Completo di Post

```markdown
---
layout: post
title: "Nuovo Concerto a Milano - 20 Dicembre 2025"
date: 2025-11-15
image: /assets/images/concerto-milano.webp
---

Siamo entusiasti di annunciare il nostro prossimo concerto a Milano!

<!--more-->

Il 20 dicembre 2025 saremo al **Fabrique** per una serata speciale dedicata ai brani più iconici dei Cranberries.

## Dettagli dell'Evento

- **Data**: 20 Dicembre 2025
- **Ora**: 21:00
- **Luogo**: Fabrique, Milano
- **Biglietti**: Disponibili su TicketOne

Non vediamo l'ora di vedervi! 🎸
```

## ❓ Domande Frequenti

### Come modifico un post già pubblicato?

1. Modifica il file in `_posts/`
2. Fai commit e push
3. Il post verrà aggiornato automaticamente

### Come elimino un post?

1. Elimina il file dalla cartella `_posts/`
2. Fai commit e push
3. Il post verrà rimosso sia dal blog italiano che da quello inglese

### Posso usare HTML nel post?

Sì! Markdown supporta anche HTML, quindi puoi usare tag HTML quando necessario.

### Come vedo l'anteprima prima di pubblicare?

Puoi usare un editor Markdown online come:
- https://dillinger.io/
- https://stackedit.io/

---

Per qualsiasi dubbio o problema, contatta il team tecnico (Mattia)! 🎵