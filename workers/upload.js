// Cloudflare Worker per caricare immagini su GitHub
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
      const { password, filename, fileContent } = await request.json();

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

      // GitHub API setup
      const GITHUB_TOKEN = env.GITHUB_TOKEN;
      const GITHUB_OWNER = 'thelizberries';
      const GITHUB_REPO = 'blog';
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
          content: fileContent, // fileContent deve essere già in base64
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

      const result = await uploadResponse.json();
      
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

    } catch (error) {
      console.error('Upload error:', error);
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
