// Cloudflare Worker per gestire upload immagini e creazione post su GitHub
// Gestisce autenticazione con password e upload sicuro

export default {
  async fetch(request, env) {
    // Abilita CORS
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // Gestisci preflight request
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Accetta solo POST
    if (request.method !== 'POST') {
      return new Response(
        JSON.stringify({ error: 'Method not allowed' }),
        { 
          status: 405,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        }
      );
    }

    try {
      const requestData = await request.json();
      const { action, password } = requestData;

      // Verifica password (configurata come variabile d'ambiente su Cloudflare)
      if (password !== env.UPLOAD_PASSWORD) {
        return new Response(
          JSON.stringify({ error: 'Password non corretta' }),
          { 
            status: 401,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' }
          }
        );
      }

      // GitHub API setup
      const GITHUB_TOKEN = env.GITHUB_TOKEN;
      const GITHUB_OWNER = 'thelizberries';
      const GITHUB_REPO = 'blog-lizberries';

      // Route basato sull'action
      if (action === 'upload_image') {
        return await handleImageUpload(requestData, GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, corsHeaders);
      } else if (action === 'create_post') {
        return await handlePostCreation(requestData, GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, corsHeaders);
      } else {
        // Compatibilità con vecchia versione (senza action)
        return await handleImageUpload(requestData, GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, corsHeaders);
      }

    } catch (error) {
      console.error('Worker error:', error);
      return new Response(
        JSON.stringify({ 
          error: 'Errore del server',
          details: error.message 
        }),
        { 
          status: 500,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        }
      );
    }
  }
};

// Funzione per gestire l'upload delle immagini
async function handleImageUpload(data, GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, corsHeaders) {
  const { filename, fileContent } = data;

  // Verifica che il file sia un'immagine
  const allowedExtensions = ['.jpg', '.jpeg', '.png'];
  const fileExt = filename.toLowerCase().substring(filename.lastIndexOf('.'));
  if (!allowedExtensions.includes(fileExt)) {
    return new Response(
      JSON.stringify({ 
        error: 'Formato file non supportato. Usa .jpg, .jpeg o .png' 
      }),
      { 
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  const GITHUB_PATH = `assets/images/posts/${filename}`;

  // Verifica se il file esiste già
  const checkUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
  const checkResponse = await fetch(checkUrl, {
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Cloudflare-Worker'
    }
  });

  if (checkResponse.ok) {
    return new Response(
      JSON.stringify({ 
        error: `Un file con il nome "${filename}" esiste già. Rinominalo e riprova.` 
      }),
      { 
        status: 409,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  // Carica il file su GitHub
  const uploadUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
  const uploadResponse = await fetch(uploadUrl, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'Cloudflare-Worker'
    },
    body: JSON.stringify({
      message: `Upload image: ${filename}`,
      content: fileContent,
      branch: 'main'
    })
  });

  if (!uploadResponse.ok) {
    const errorData = await uploadResponse.json();
    console.error('GitHub API Error:', errorData);
    return new Response(
      JSON.stringify({ 
        error: 'Errore durante il caricamento su GitHub',
        details: errorData.message 
      }),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  return new Response(
    JSON.stringify({ 
      success: true,
      message: `Immagine "${filename}" caricata con successo!`,
      webpName: filename.replace(/\.(jpg|jpeg|png)$/i, '.webp'),
      path: GITHUB_PATH
    }),
    { 
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    }
  );
}

// Funzione per gestire la creazione dei post
async function handlePostCreation(data, GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, corsHeaders) {
  const { filename, content } = data;

  // Verifica che il filename sia un .md file
  if (!filename.endsWith('.md')) {
    return new Response(
      JSON.stringify({ 
        error: 'Il file deve avere estensione .md' 
      }),
      { 
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  // Verifica e correggi il marcatore <!--more-->
  let processedContent = ensureMoreMarker(content);

  const GITHUB_PATH = `_posts/${filename}`;

  // Verifica se il post esiste già
  const checkUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
  const checkResponse = await fetch(checkUrl, {
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Cloudflare-Worker'
    }
  });

  if (checkResponse.ok) {
    return new Response(
      JSON.stringify({ 
        error: `Un post con il nome "${filename}" esiste già. Modifica il titolo o la data.` 
      }),
      { 
        status: 409,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  // Converti il contenuto in base64
  const contentBase64 = btoa(unescape(encodeURIComponent(processedContent)));

  // Carica il post su GitHub
  const uploadUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
  const uploadResponse = await fetch(uploadUrl, {
    method: 'PUT',
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
      'User-Agent': 'Cloudflare-Worker'
    },
    body: JSON.stringify({
      message: `Create post: ${filename}`,
      content: contentBase64,
      branch: 'main'
    })
  });

  if (!uploadResponse.ok) {
    const errorData = await uploadResponse.json();
    console.error('GitHub API Error:', errorData);
    return new Response(
      JSON.stringify({ 
        error: 'Errore durante la creazione del post su GitHub',
        details: errorData.message 
      }),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    );
  }

  return new Response(
    JSON.stringify({ 
      success: true,
      message: `Post "${filename}" creato con successo!`,
      filename: filename,
      path: GITHUB_PATH
    }),
    { 
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    }
  );
}

// Funzione per verificare e inserire il marcatore <!--more-->
function ensureMoreMarker(content) {
  // Separa front matter dal contenuto
  const frontMatterRegex = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;
  const match = content.match(frontMatterRegex);
  
  if (!match) {
    // Se non c'è front matter, restituisci il contenuto originale
    return content;
  }
  
  const frontMatter = match[1];
  let postContent = match[2];
  
  // Rimuovi spazi/newline iniziali
  postContent = postContent.trim();
  
  // Estrai il titolo dal front matter per controllarne la lunghezza
  const titleMatch = frontMatter.match(/title:\s*['"]?([^'"\n]+)['"]?/);
  const titleLength = titleMatch ? titleMatch[1].trim().length : 0;
  
  // Se il titolo è >= 50 caratteri, riduci il limite a 80, altrimenti usa 100
  const maxLength = titleLength >= 50 ? 80 : 100;
  const minLength = titleLength >= 50 ? 40 : 50;
  const searchStart = titleLength >= 50 ? 60 : 80;
  const searchRange = titleLength >= 50 ? 40 : 50;
  
  // Controlla se <!--more--> è già presente
  if (postContent.includes('<!--more-->')) {
    // Se è presente, verifica che sia nella posizione corretta
    const moreIndex = postContent.indexOf('<!--more-->');
    if (moreIndex > 0 && moreIndex < 400) {
      // Il marcatore è già presente e in una posizione ragionevole
      return content;
    }
    // Se è troppo lontano, rimuovilo e lo reinseriremo nella posizione corretta
    postContent = postContent.replace('<!--more-->', '').trim();
  }
  
  // Trova la posizione migliore: dopo il primo paragrafo o dopo maxLength caratteri
  let insertPosition = maxLength;
  
  // Cerca il primo doppio newline (fine paragrafo) entro i primi 100 caratteri
  const firstParagraphEnd = postContent.substring(0, 100).indexOf('\n\n');
  if (firstParagraphEnd > 50 && firstParagraphEnd < 100) {
    insertPosition = firstParagraphEnd;
  } else {
    // Altrimenti cerca la fine della prima frase dopo searchStart caratteri
    const actualSearchStart = Math.min(searchStart, postContent.length);
    const remainingText = postContent.substring(actualSearchStart, Math.min(actualSearchStart + searchRange, postContent.length));
    
    // Cerca il primo punto seguito da spazio o newline
    const sentenceEndMatch = remainingText.match(/[.!?][\s\n]/);
    if (sentenceEndMatch) {
      insertPosition = actualSearchStart + sentenceEndMatch.index + 1;
    } else {
      // Se non trova un punto, cerca almeno uno spazio dopo 100 caratteri
      const spaceIndex = remainingText.indexOf(' ');
      if (spaceIndex !== -1) {
        insertPosition = searchStart + spaceIndex;
      }
    }
  }
  
  // Assicurati di non troncare nel mezzo di una parola
  while (insertPosition < postContent.length && 
         postContent[insertPosition] !== ' ' && 
         postContent[insertPosition] !== '\n') {
    insertPosition++;
  }
  
  // Inserisci il marcatore
  const beforeMarker = postContent.substring(0, insertPosition).trimEnd();
  const afterMarker = postContent.substring(insertPosition).trimStart();
  
  postContent = `${beforeMarker}\n\n<!--more-->\n\n${afterMarker}`;
  
  // Ricostruisci il file completo
  return `---\n${frontMatter}\n---\n${postContent}`;
}