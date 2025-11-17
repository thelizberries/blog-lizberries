// Netlify Function per caricare immagini su GitHub
// Gestisce autenticazione con password e upload sicuro

exports.handler = async (event, context) => {
  // Abilita CORS per permettere richieste dal blog
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  // Gestisci preflight request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Accetta solo POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { password, filename, fileContent } = JSON.parse(event.body);

    // Verifica password (da configurare nelle variabili d'ambiente di Netlify)
    const UPLOAD_PASSWORD = process.env.UPLOAD_PASSWORD;
    if (password !== UPLOAD_PASSWORD) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({ error: 'Password non corretta' })
      };
    }

    // Verifica che il file sia un'immagine
    const allowedExtensions = ['.jpg', '.jpeg', '.png'];
    const fileExt = filename.toLowerCase().substring(filename.lastIndexOf('.'));
    if (!allowedExtensions.includes(fileExt)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          error: 'Formato file non supportato. Usa .jpg, .jpeg o .png' 
        })
      };
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
      return {
        statusCode: 409,
        headers,
        body: JSON.stringify({ 
          error: `Un file con il nome "${filename}" esiste già. Rinominalo e riprova.` 
        })
      };
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
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ 
          error: 'Errore durante il caricamento su GitHub',
          details: errorData.message 
        })
      };
    }

    const result = await uploadResponse.json();
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ 
        success: true,
        message: `Immagine "${filename}" caricata con successo!`,
        webpName: filename.replace(/\.(jpg|jpeg|png)$/i, '.webp'),
        path: GITHUB_PATH
      })
    };

  } catch (error) {
    console.error('Upload error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Errore del server',
        details: error.message 
      })
    };
  }
};
