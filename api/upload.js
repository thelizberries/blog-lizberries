// Vercel Serverless Function per caricare immagini su GitHub
// Gestisce autenticazione con password e upload sicuro

export default async function handler(req, res) {
  // Abilita CORS per permettere richieste dal blog
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Gestisci preflight request
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Accetta solo POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { password, filename, fileContent } = req.body;

    // Verifica password (da configurare nelle variabili d'ambiente di Vercel)
    const UPLOAD_PASSWORD = process.env.UPLOAD_PASSWORD;
    if (password !== UPLOAD_PASSWORD) {
      return res.status(401).json({ error: 'Password non corretta' });
    }

    // Verifica che il file sia un'immagine
    const allowedExtensions = ['.jpg', '.jpeg', '.png'];
    const fileExt = filename.toLowerCase().substring(filename.lastIndexOf('.'));
    if (!allowedExtensions.includes(fileExt)) {
      return res.status(400).json({ 
        error: 'Formato file non supportato. Usa .jpg, .jpeg o .png' 
      });
    }

    // GitHub API setup
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const GITHUB_OWNER = 'thelizberries';
    const GITHUB_REPO = 'blog';
    const GITHUB_PATH = `assets/images/posts/${filename}`;

    // Verifica se il file esiste già
    const checkUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
    const checkResponse = await fetch(checkUrl, {
      headers: {
        'Authorization': `token ${GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });

    if (checkResponse.ok) {
      return res.status(409).json({ 
        error: `Un file con il nome "${filename}" esiste già. Rinominalo e riprova.` 
      });
    }

    // Carica il file su GitHub
    const uploadUrl = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${GITHUB_PATH}`;
    const uploadResponse = await fetch(uploadUrl, {
      method: 'PUT',
      headers: {
        'Authorization': `token ${GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: `Upload image: ${filename}`,
        content: fileContent, // fileContent deve essere già in base64
        branch: 'main'
      })
    });

    if (!uploadResponse.ok) {
      const errorData = await uploadResponse.json();
      console.error('GitHub API Error:', errorData);
      return res.status(500).json({ 
        error: 'Errore durante il caricamento su GitHub',
        details: errorData.message 
      });
    }

    const result = await uploadResponse.json();
    
    return res.status(200).json({ 
      success: true,
      message: `Immagine "${filename}" caricata con successo!`,
      webpName: filename.replace(/\.(jpg|jpeg|png)$/i, '.webp'),
      path: GITHUB_PATH
    });

  } catch (error) {
    console.error('Upload error:', error);
    return res.status(500).json({ 
      error: 'Errore del server',
      details: error.message 
    });
  }
}
