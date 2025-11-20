# Lizberries Blog - Guida per la Creazione dei Post

Benvenuto nella guida per creare e pubblicare post sul blog dei Lizberries! Questa guida ti accompagnerà passo dopo passo nella creazione di nuovi articoli.

---

## 📑 Indice

- [⚡ Guida Rapida](#-guida-rapida---per-chi-non-è-pratico-di-github)
- [📸 Caricamento Immagini](#-per-aggiungere-immagini)

- [📝 Struttura del Blog](#-struttura-del-blog-per-utenti-tecnici)
- [🚀 Come Creare un Nuovo Post](#-come-creare-un-nuovo-post)
- [🖼️ Gestione delle Immagini](#️-gestione-delle-immagini)
- [📤 Pubblicare il Post](#-pubblicare-il-post)
- [🌐 Traduzione Automatica](#-traduzione-automatica-e-sincronizzazione)
- [✏️ Formattazione Markdown](#️-formattazione-markdown)
- [🔄 Workflow Completo](#-workflow-completo)
- [❓ Domande Frequenti](#-domande-frequenti)
- [🛡️ Backup e Ripristino](#️-backup-e-ripristino)
- [🔧 Informazioni Tecniche](#-informazioni-tecniche-solo-per-amministratori)

---

## ⚡ GUIDA RAPIDA - Per chi non è pratico di GitHub

**Il modo più semplice per scrivere e pubblicare un post:**

### Metodo 1: Editor Unificato (CONSIGLIATO) 🎯

**Crea post e carica immagini in un solo posto!**

1. **Vai su**: https://blog.lizberries.thelizards.it/upload.html
2. **Carica l'immagine** (opzionale):
   - Seleziona un file `.jpg`, `.jpeg` o `.png`
   - Vedrai l'anteprima dell'immagine
3. **Compila il post**:
   - **Titolo**: es. "Nuovo Concerto a Milano"
   - **Data**: Seleziona la data di pubblicazione (anche futura per programmare)
   - **Contenuto**: Scrivi il testo usando Markdown
   - Usa i pulsanti della toolbar per formattare (grassetto, corsivo, link, ecc.)
4. **Vedi l'anteprima** in tempo reale mentre scrivi
5. **Inserisci la password** (richiedila al team tecnico)
6. **Clicca "Pubblica Post + Immagine"**
7. **Fatto!** Il post e l'immagine vengono caricati insieme

✅ **Vantaggi**:
- Tutto in un solo posto
- Anteprima live mentre scrivi
- Nessun account GitHub necessario
- Ottimizzazione immagini automatica
- 100% gratuito (Cloudflare Workers: 100.000 richieste/giorno)

---

### Metodo 2: Prose.io (per modificare post esistenti)

Usa questo metodo solo se devi **modificare un post già pubblicato**:

1. **Vai su** https://prose.io/
2. **Clicca "Authorize on GitHub"** e fai login
3. **Seleziona il repository "blog"**
4. **Clicca sulla cartella "_posts"**
5. **Clicca sul post** che vuoi modificare
6. **Modifica il contenuto**
7. **Clicca "Save"** (💾 in alto a destra)

---

**⏱️ Tempi di pubblicazione:**
- Il post appare sul blog italiano in 1-2 minuti (se la data è oggi o passata)
- Dopo altri 1-2 minuti appare tradotto automaticamente sul blog inglese
- **Post programmati**: I post con data futura verranno pubblicati automaticamente il giorno indicato

---

## 📸 Caricamento Immagini (Metodo Manuale)

Se preferisci caricare solo le immagini separatamente (senza creare il post):

1. **Vai al link**: https://blog.lizberries.thelizards.it/upload.html
2. **Inserisci la password** (chiedila al team tecnico)
3. **Seleziona l'immagine** (formati supportati: `.jpg`, `.jpeg`, `.png`)
4. **Clicca "Carica Immagine"**
5. **Copia il nome del file WebP** mostrato nel messaggio di successo
6. **Usa questo nome** nel post (es: `/assets/images/posts/nome-file.webp`)

---

## DOCUMENTAZIONE PER UTENTI TECNICI 

## 📝 Struttura del Blog

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
image: /assets/images/posts/nome-immagine.webp
---

Inserisci qui il testo del post...

<!--more-->

Continua con il resto del contenuto...
```

### 3. Componenti del Front Matter

- **layout**: Sempre `post` (obbligatorio)
- **title**: Il titolo del post tra virgolette (obbligatorio)
- **date**: La data nel formato `YYYY-MM-DD` (obbligatorio)
  - Puoi usare date future per programmare la pubblicazione
  - I post con data futura non appariranno sul blog fino a quel giorno
- **image**: Percorso dell'immagine di anteprima (opzionale)

### 4. Tag `<!--more-->`

Il tag `<!--more-->` separa l'anteprima (excerpt) dal resto del contenuto:
- Il testo **prima** del tag, seguito da una riga di spazio, appare nella home del blog come anteprima
- Il testo **dopo** il tag appare solo nell'articolo completo

## 🖼️ Gestione delle Immagini

### Caricare Immagini - Metodo Form di Upload (Consigliato)

**Il modo più semplice per caricare immagini:**

1. **Vai su**: https://blog.lizberries.thelizards.it/upload.html
2. **Inserisci la password** (richiedila al team tecnico se non ce l'hai)
3. **Seleziona l'immagine** dal tuo computer
   - Formati supportati: `.jpg`, `.jpeg`, `.png`
   - Nome file: usa nomi descrittivi con trattini (es: `concerto-milano-2025.jpg`)
   - Dimensioni: qualsiasi (verranno ottimizzate automaticamente)
4. **Visualizza l'anteprima** e le dimensioni del file
5. **Clicca "Carica Immagine"**
6. **Attendi 1-2 minuti**: L'immagine viene caricata e automaticamente:
   - Ridimensionata a max **900x600px** (mantenendo proporzioni)
   - Convertita in formato **WebP** ottimizzato
   - Compressa a circa **30-40KB** per caricamento veloce
7. **Copia il nome WebP** mostrato nel messaggio di successo (es: `concerto-milano-2025.webp`)
8. **Usa nel post** il percorso: `/assets/images/posts/concerto-milano-2025.webp`

✅ **Vantaggi**:
- Non serve account GitHub
- Interfaccia semplice e intuitiva
- Anteprima prima del caricamento
- **Ottimizzazione automatica** (ridimensionamento + compressione)
- Controllo duplicati automatico
- Conversione WebP automatica
- **100% gratuito**: Cloudflare Workers offre 100.000 richieste/giorno senza limiti di credito

---

### Caricare Immagini - Metodo GitHub (Alternativo)

1. **Salva l'immagine** nella cartella `assets/images/posts/` tramite GitHub
2. **Formati supportati**: `.jpg`, `.jpeg`, `.png`
3. **Naming**: Usa nomi descrittivi con trattini, es: `concerto-milano-2025.jpg`
4. **Ottimizzazione automatica**: Dopo 1-2 minuti dal caricamento:
   - Ridimensionamento a max 900x600px
   - Conversione in formato WebP
   - Compressione a ~30-40KB
5. **Aggiungi nel front matter** (usa sempre `.webp` come estensione): 
   ```yaml
   image: /assets/images/posts/concerto-milano-2025.webp
   ```

**Nota**: Le immagini vengono ottimizzate automaticamente per garantire caricamento rapido del blog.

---

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
   git add assets/images/posts/nome-immagine.webp
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

## 🌐 Traduzione Automatica e Sincronizzazione

Quando lavori con i post in italiano, il sistema gestisce **automaticamente** la traduzione e la sincronizzazione con il blog inglese.

### ✨ Creazione di un Nuovo Post

Quando pubblichi un post in italiano:

1. **GitHub Actions** rileva il nuovo post
2. Lo **traduce automaticamente** in inglese usando Google Translate
3. **Copia automaticamente le immagini** referenziate nel post al blog inglese
4. Lo pubblica sul blog inglese con:
   - Titolo tradotto
   - Contenuto tradotto
   - Nome file tradotto (SEO-friendly slug inglese)
   - Immagini copiate in `assets/images/posts/`
   - Campo `original_file` che traccia il post italiano di origine

⏱️ La traduzione richiede circa 1-2 minuti dopo il push.

### 🔄 Modifica di un Post Esistente

**Tutto viene aggiornato automaticamente!** Quando modifichi un post italiano esistente:

1. Il sistema **rileva la modifica** confrontando la lunghezza del contenuto
2. **Cancella il vecchio post inglese** (qualsiasi fosse il nome)
3. **Crea un nuovo post inglese** con:
   - Nuovo titolo tradotto (se lo hai modificato)
   - Nuova data (se l'hai modificata nel filename)
   - Contenuto aggiornato e tradotto
   - Immagini aggiornate (se le hai cambiate)

**Esempi:**
- Modifichi solo il **contenuto** → il post inglese viene aggiornato mantenendo stesso nome
- Modifichi il **titolo** → il post inglese viene rinominato con il nuovo slug tradotto
- Modifichi la **data** nel filename → il post inglese viene rinominato con la nuova data
- Modifichi **tutto insieme** → il post inglese viene completamente rigenerato

⚠️ **Importante**: Il sistema usa il campo `original_file` nel front matter del post inglese per tracciare quale post italiano corrisponde. Anche se cambi titolo o data, il sistema trova sempre il post inglese corretto da aggiornare.

### 🗑️ Cancellazione di un Post

Quando elimini un post italiano:

1. Il post inglese corrispondente viene **cancellato automaticamente**
2. Le **immagini associate** vengono **cancellate automaticamente** sia dal blog italiano che da quello inglese
3. **SOLO SE** l'immagine non è usata in altri post (controllo di sicurezza)

**Gestione Intelligente delle Immagini:**
- Se un'immagine è referenziata da più post, viene mantenuta anche se ne elimini uno
- Vengono cancellate solo le immagini che non sono più utilizzate da nessun post
- La cancellazione avviene in entrambi i repository (italiano e inglese)

### 📸 Sincronizzazione delle Immagini

**Le immagini vengono gestite automaticamente!** Non devi copiarle manualmente.

- Quando carichi un'immagine in `assets/images/posts/` nel blog italiano
- E la referenzi in un post (nel front matter o nel contenuto)
- Viene **automaticamente copiata** nel blog inglese durante la traduzione
- Se modifichi l'immagine nel post italiano, viene aggiornata anche nel post inglese
- Se elimini il post, l'immagine viene rimossa da entrambi i blog (se non usata altrove)

**Nota**: Non modificare manualmente i post o le immagini nel repository blog-en! Tutto viene gestito automaticamente dal workflow di traduzione.

## ✏️ ESEMPI DI FORMATTAZIONE MARKDOWN

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
![Descrizione immagine](/assets/images/posts/nome-immagine.webp)
```

## 🔄 Workflow Completo

### Creare un Nuovo Post

1. ✍️ Scrivi il post in Markdown
2. 📁 Salva il file in `_posts/` con il formato `YYYY-MM-DD-titolo.md`
3. 🖼️ (Opzionale) Aggiungi immagini in `assets/images/posts/`
4. 💾 Fai commit e push su GitHub
5. ⏳ Attendi 1-2 minuti per la pubblicazione
6. ✅ Il post appare sul **blog italiano**
7. 🌍 Dopo altri 1-2 minuti, appare **tradotto automaticamente** sul blog inglese

### Modificare un Post Esistente

1. ✏️ Modifica il file del post in `_posts/` (titolo, data, contenuto, immagini)
2. 💾 Fai commit e push su GitHub
3. ⏳ Attendi 1-2 minuti
4. ✅ Il post viene **aggiornato** sul blog italiano
5. 🔄 Il sistema **rileva la modifica** e aggiorna automaticamente:
   - Il post inglese con contenuto tradotto aggiornato
   - Il filename inglese (se hai cambiato titolo o data)
   - Le immagini copiate nel blog inglese

### Eliminare un Post

1. 🗑️ Elimina il file del post da `_posts/`
2. 💾 Fai commit e push su GitHub
3. ⏳ Attendi 1-2 minuti
4. ✅ Il post viene **rimosso** dal blog italiano
5. 🔄 Il sistema elimina automaticamente:
   - Il post inglese corrispondente
   - Le immagini associate (se non usate in altri post) da entrambi i blog
**Metodo 1 - Form di Upload (consigliato):**
1. 📤 Vai su https://blog.lizberries.thelizards.it/upload.html
2. 🔐 Inserisci la password
3. 🖼️ Seleziona e carica l'immagine (qualsiasi dimensione)
4. ⏳ Attendi 1-2 minuti: viene ridimensionata (max 900x600px), convertita in WebP e compressa (~30-40KB)
5. 📝 Usa il nome WebP nel post

**Metodo 2 - Via GitHub:**
1. 📤 Carica l'immagine in `assets/images/posts/` tramite GitHub
2. ⏳ Attendi 1-2 minuti: viene ottimizzata automaticamente (ridimensionamento + WebP + compressione)
3. 📝 Referenziala nel post usando `.webp` come estensione

**Metodo 2 - Via GitHub:**
1. 📤 Carica l'immagine in `assets/images/posts/` tramite GitHub
2. ⏳ Attendi 1-2 minuti: viene convertita automaticamente in `.webp`
3. 📝 Referenziala nel post usando `.webp` come estensione

**Aggiornamento:**
- Modifica l'immagine referenziata nel post italiano
- Fai push (o ricarica via form)
- L'immagine viene automaticamente aggiornata nel blog inglese

**Eliminazione:**
- Elimina il post che usa l'immagine
- L'immagine viene cancellata automaticamente da entrambi i blog
- Solo se non è usata in altri post!

## 📋 Esempio Completo di Post

```markdown
---
layout: post
title: "Nuovo Concerto a Milano - 20 Dicembre 2025"
date: 2025-11-15
image: /assets/images/posts/concerto-milano.webp
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

## ❓ FAQ: Domande Frequenti

### Come modifico un post già pubblicato?

1. Modifica il file in `_posts/` (puoi cambiare titolo, data, contenuto, immagini)
2. Fai commit e push
3. Il post verrà aggiornato automaticamente **sia nel blog italiano che in quello inglese**
4. Se hai modificato il titolo o la data, il post inglese verrà rinominato automaticamente

**Nota**: Non serve toccare il blog inglese, tutto viene sincronizzato automaticamente!

### Come elimino un post?

1. Elimina il file dalla cartella `_posts/`
2. Fai commit e push
3. Il post verrà rimosso **automaticamente** sia dal blog italiano che da quello inglese
4. Le immagini associate verranno cancellate da entrambi i blog (se non usate in altri post)
### Posso usare HTML nel post?

Sì! Markdown supporta anche HTML, quindi puoi usare tag HTML quando necessario.

### Posso programmare post per il futuro?

Sì! Puoi impostare una data futura nel front matter del post (es: `date: 2025-12-25`). Il post verrà pubblicato automaticamente il giorno indicato. Fino a quella data, il post non sarà visibile sul blog, ma sarà già presente nel repository GitHub.

### Come vedo l'anteprima prima di pubblicare?

Puoi usare un editor Markdown online come:
- https://dillinger.io/
- https://stackedit.io/

### Come ottengo la password per il form di upload delle immagini?

La password per il form di upload è **riservata ai membri del team** che devono caricare immagini per i post. Contatta il team tecnico (Mattia) per ottenerla. La password è configurata in modo sicuro sul server e non è visibile pubblicamente.

---

## 🛡️ Backup e Ripristino

### Sistema di Protezione Automatica

Il blog è protetto da un sistema di backup automatico che:
- ✅ Crea un backup completo ogni giorno alle 03:00 UTC
- ✅ Mantiene gli ultimi 30 giorni di backup
- ✅ Permette ripristino rapido in caso di problemi
- ✅ Salva tutta la storia delle modifiche (Git History)

### File Critici da NON Modificare

**⚠️ ATTENZIONE**: Questi file sono essenziali per il funzionamento del blog. **Non modificarli** a meno che tu non sappia esattamente cosa stai facendo:

- `_config.yml` - Configurazione principale
- `.github/workflows/` - Automazioni (traduzione, ottimizzazione immagini, backup)
- `.github/scripts/` - Script di traduzione
- `wrangler.toml` e `workers/upload.js` - Sistema di upload immagini
- `_layouts/` e `_includes/` - Template del sito
- `CNAME` - Configurazione dominio

**✅ File che PUOI modificare liberamente:**
- `_posts/` - I tuoi post del blog
- `assets/images/posts/` - Le immagini dei post
- `README.md` - Questa documentazione (con cautela)

### Come Ripristinare in Caso di Problemi

Se qualcosa va storto, consulta la **[Guida Completa al Ripristino](RIPRISTINO.md)** che spiega:
- Come ripristinare singoli file modificati per errore
- Come usare i backup giornalieri automatici
- Come verificare i permessi dei collaboratori
- Comandi rapidi di emergenza

**Link rapido**: [RIPRISTINO.md](RIPRISTINO.md)

---

## 🔧 Informazioni Tecniche (Solo per Amministratori)

### Form di Upload Immagini

Il sistema di upload è implementato con:
- **Frontend**: Form HTML accessibile su https://blog.lizberries.thelizards.it/upload.html
- **Backend**: Cloudflare Worker serverless (https://lizberries-blog-upload.lizberries.workers.dev)
- **Autenticazione**: Password protetta tramite variabile d'ambiente `UPLOAD_PASSWORD`
- **Storage**: GitHub API - carica direttamente nel repository `thelizberries/blog`
- **Ottimizzazione immagini**:
  - Ridimensionamento automatico a max 900x600px (mantenendo proporzioni)
  - Conversione in formato WebP
  - Compressione con qualità 75 e metodo 6 (massima compressione)
  - Dimensione finale: ~30-40KB per caricamento rapido
- **Sicurezza**: 
  - Validazione formato file server-side
  - Controllo duplicati automatico
  - Token GitHub con scope limitato (`repo` only)
  - Password hash non committata nel repository
- **Vantaggi Cloudflare**:
  - 100% gratuito: 100.000 richieste/giorno senza limiti di credito
  - Nessuna carta di credito richiesta
  - Deploy globale su edge network
  - Zero downtime

**Configurazione variabili d'ambiente su Cloudflare**:
1. Dashboard Cloudflare: Workers & Pages → lizberries-blog-upload → Settings → Variables
2. `UPLOAD_PASSWORD`: Password per il form di upload → Encrypt → Save
3. `GITHUB_TOKEN`: Personal Access Token con scope `repo` (token name "Blog Image Upload") → Encrypt → Save

**Manutenzione**:
- Per cambiare la password: Cloudflare Dashboard → Workers & Pages → lizberries-blog-upload → Settings → Variables
- Per rigenerare il token GitHub: https://github.com/settings/tokens
- Per modificare il codice: Cloudflare Dashboard → Workers & Pages → lizberries-blog-upload → Edit Code

---

Per qualsiasi dubbio o problema, contatta il team tecnico (Mattia)! 🎵