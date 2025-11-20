# 🛡️ Guida al Ripristino del Blog

Questa guida ti spiega come ripristinare il blog in caso di modifiche accidentali o problemi.

---

## 📋 Indice

1. [Ripristino di un Singolo File](#ripristino-di-un-singolo-file)
2. [Ripristino da Backup Giornaliero](#ripristino-da-backup-giornaliero)
3. [Ripristino Completo del Repository](#ripristino-completo-del-repository)
4. [Verifica Permessi Collaboratori](#verifica-permessi-collaboratori)
5. [File Critici da Proteggere](#file-critici-da-proteggere)

---

## 🔧 Ripristino di un Singolo File

### Scenario: Un file è stato modificato o cancellato per errore

**Metodo 1: Via GitHub Web (più semplice)**

1. Vai su https://github.com/thelizberries/blog
2. Clicca sul file che vuoi ripristinare (o naviga nella cartella dove era)
3. Clicca su "History" (in alto a destra)
4. Trova la versione corretta del file
5. Clicca sui tre puntini `...` → "View file"
6. Copia il contenuto
7. Torna al file attuale → "Edit" → Incolla → "Commit changes"

**Metodo 2: Via Git Locale (più veloce)**

```bash
# 1. Vai nella cartella del blog
cd C:\Users\mamonza\Downloads\Liz\LizHubBlogIt\blog

# 2. Vedi la storia del file
git log --oneline -- path/to/file

# 3. Ripristina il file a una versione specifica
git checkout COMMIT_ID -- path/to/file

# Esempi pratici:
git checkout HEAD~1 -- _config.yml              # Versione precedente di _config.yml
git checkout abc1234 -- .github/workflows/translate-and-sync.yml  # Versione specifica del workflow

# 4. Verifica che il file sia corretto
# Poi fai commit e push
git add path/to/file
git commit -m "Ripristino file da versione precedente"
git push origin main
```

**Metodo 3: Ripristino Rapido (ultimo commit)**

```bash
# Annulla le modifiche non ancora committate
git restore path/to/file

# Oppure torna all'ultimo commit
git checkout HEAD -- path/to/file
```

---

## 📦 Ripristino da Backup Giornaliero

### Scenario: Hai bisogno di ripristinare il blog a una data specifica

Il sistema crea backup automatici ogni giorno alle 03:00 UTC. I backup sono disponibili come branch separati.

**Passo 1: Trova il backup che ti serve**

```bash
# Elenca tutti i backup disponibili (ultimi 30 giorni)
git fetch --all
git branch -r | grep 'origin/backup/'

# Output esempio:
# origin/backup/2025-11-20
# origin/backup/2025-11-19
# origin/backup/2025-11-18
```

**Passo 2: Verifica il contenuto del backup**

```bash
# Scarica il branch di backup localmente
git checkout backup/2025-11-19

# Visualizza le informazioni sul backup
cat .backup-info.txt

# Esplora i file e verifica che sia quello giusto
ls -la
```

**Passo 3a: Ripristina SINGOLI FILE dal backup**

```bash
# Torna al branch main
git checkout main

# Copia singoli file dal backup
git checkout backup/2025-11-19 -- _config.yml
git checkout backup/2025-11-19 -- .github/workflows/

# Fai commit delle modifiche
git add .
git commit -m "Ripristino file da backup del 2025-11-19"
git push origin main
```

**Passo 3b: Ripristina TUTTO dal backup (ATTENZIONE!)**

```bash
# ⚠️ ATTENZIONE: Questo sovrascrive TUTTO sul branch main!

# 1. Crea un branch temporaneo dal backup
git checkout backup/2025-11-19
git checkout -b restore-from-backup-2025-11-19

# 2. Verifica che TUTTO sia corretto
# Controlla file importanti, configurazioni, post, ecc.

# 3. SE SEI SICURO, sovrascrivi il main
git checkout main
git reset --hard restore-from-backup-2025-11-19

# 4. Forza il push (IRREVERSIBILE senza un altro backup!)
git push --force origin main

# 5. Pulisci il branch temporaneo
git branch -d restore-from-backup-2025-11-19
```

---

## 🚨 Ripristino Completo del Repository

### Scenario ESTREMO: Il repository è gravemente danneggiato

**Opzione 1: Ripristino da Backup Cloud GitHub**

```bash
# 1. Rinomina la cartella locale danneggiata
mv blog blog-danneggiato

# 2. Clona nuovamente il repository
git clone https://github.com/thelizberries/blog.git
cd blog

# 3. Se anche il repository remoto è danneggiato, usa il backup
git fetch --all
git checkout backup/2025-11-20
git checkout -b main-restored
git push --force origin main-restored:main
```

**Opzione 2: Ripristino da Backup Locale (se hai una copia)**

```bash
# Se hai fatto backup locali in altre cartelle
cp -r /path/to/backup/blog ./blog-restored
cd blog-restored
git remote add origin https://github.com/thelizberries/blog.git
git push --force origin main
```

---

## 👥 Verifica Permessi Collaboratori

### Come verificare che i collaboratori abbiano permessi corretti

**Via GitHub Web:**

1. Vai su https://github.com/thelizberries/blog/settings/access
2. Verifica che i collaboratori abbiano ruolo **"Write"** (non "Admin")
3. Solo tu dovresti avere ruolo "Admin" o "Owner"

**Permessi corretti:**
- ✅ **Write**: Possono aggiungere/modificare contenuti, NON possono modificare impostazioni
- ❌ **Admin**: Possono fare TUTTO, incluso cancellare il repository
- ❌ **Maintain**: Più permessi del necessario

**Per modificare i permessi:**
1. Vai su Settings → Collaborators
2. Clicca sull'ingranaggio accanto al nome del collaboratore
3. Seleziona "Write" dal menu a tendina
4. Salva

---

## 📁 File Critici da Proteggere

### File che NON dovrebbero essere modificati dai collaboratori

**Configurazioni Jekyll:**
- `_config.yml` - Configurazione principale del blog
- `Gemfile` - Dipendenze Ruby/Jekyll

**GitHub Actions (Workflow):**
- `.github/workflows/translate-and-sync.yml` - Traduzione automatica
- `.github/workflows/convert-images-to-webp.yml` - Ottimizzazione immagini
- `.github/workflows/daily-backup.yml` - Backup giornaliero
- `.github/scripts/translate_and_copy.py` - Script di traduzione

**Cloudflare Worker:**
- `wrangler.toml` - Configurazione Cloudflare
- `workers/upload.js` - Codice del worker di upload

**Layout e Template:**
- `_layouts/` - Template delle pagine
- `_includes/` - Componenti riutilizzabili

**File di sistema:**
- `.gitignore` - File da ignorare in Git
- `CNAME` - Configurazione dominio personalizzato

**Contenuti modificabili liberamente:**
- ✅ `_posts/` - Post del blog (OK modificare)
- ✅ `assets/images/posts/` - Immagini dei post (OK modificare)
- ✅ `README.md` - Documentazione (OK modificare con cautela)

---

## 🔍 Come Controllare le Modifiche Recenti

### Verifica cosa è stato modificato di recente

**Via GitHub Web:**
1. Vai su https://github.com/thelizberries/blog/commits/main
2. Vedi tutti i commit recenti con autore, data, file modificati

**Via Git Locale:**

```bash
# Vedi gli ultimi 10 commit
git log --oneline -10

# Vedi le modifiche degli ultimi 7 giorni
git log --since="7 days ago" --oneline --name-status

# Vedi chi ha modificato cosa
git log --pretty=format:"%h - %an, %ar : %s" --graph

# Vedi le modifiche a un file specifico
git log --follow -- path/to/file
```

---

## ⚡ Comandi Rapidi di Emergenza

```bash
# ANNULLA l'ultimo commit (non ancora pushato)
git reset --soft HEAD~1

# ANNULLA modifiche locali non committate
git restore .

# ANNULLA l'ultimo push (ATTENZIONE!)
git revert HEAD
git push origin main

# TORNA a un commit specifico (PERICOLOSO!)
git reset --hard COMMIT_ID
git push --force origin main

# VISUALIZZA differenze tra ora e backup
git diff main..backup/2025-11-20
```

---

## 📞 In Caso di Emergenza

Se qualcosa va storto e non sai come risolvere:

1. **NON FARE PANIC** - Git salva tutto, nulla è veramente perso
2. **NON FARE altri push** - Ferma le modifiche
3. **Controlla i backup disponibili**: `git branch -r | grep backup`
4. **Contatta Mattia** - Meglio chiedere che rischiare di peggiorare
5. **Ultima risorsa**: Ripristina da ultimo backup giornaliero

---

## 🎯 Checklist di Sicurezza

- [ ] Backup automatico attivo (controlla che il workflow giri ogni giorno)
- [ ] Collaboratori hanno permessi "Write" (non "Admin")
- [ ] Hai verificato che sai come ripristinare un file
- [ ] Hai testato il ripristino da un backup
- [ ] Sai dove trovare i backup (branch `backup/YYYY-MM-DD`)
- [ ] Hai spiegato ai collaboratori quali file NON modificare

---

**Ultimo aggiornamento**: Novembre 2025  
**Autore**: Mattia (Team Tecnico Lizberries)
