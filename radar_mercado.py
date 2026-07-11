import requests
from bs4 import BeautifulSoup
import json
import urllib.parse

# 1. Configurações da IA (Groq/Llama)
api_key_groq = "SUA_CHAVE_GROQ_AQUI"
url_groq = "https://api.groq.com/openai/v1/chat/completions"

headers_groq = {
    "Authorization": f"Bearer {api_key_groq}",
    "Content-Type": "application/json"
}

# 2. Configurações do WhatsApp (CallMeBot)
seu_numero_whatsapp = "+55SEUDDDENUMERO" 
api_key_whatsapp = "SUA_CHAVE_CALLMEBOT_AQUI"

def enviar_mensagem_whatsapp(mensagem_texto):
    texto_codificado = urllib.parse.quote(mensagem_texto)
    url_zap = f"https://api.callmebot.com/whatsapp.php?phone={seu_numero_whatsapp}&text={texto_codificado}&apikey={api_key_whatsapp}"
    
    resposta = requests.get(url_zap)
    if resposta.status_code == 200:
        print("✅ O servidor do CallMeBot aceitou a mensagem! Verifique seu celular.")
    else:
        print(f"❌ Erro do CallMeBot: {resposta.text}")

print("1. Acessando o portal de notícias (G1 Economia)...\n")
url_alvo = "https://g1.globo.com/rss/g1/economia/"
headers_site = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    resposta_site = requests.get(url_alvo, headers_site)
    soup = BeautifulSoup(resposta_site.content, 'xml')
    
    noticias = []
    # Limpeza de dados
    for item in soup.find_all('item')[:10]:
        titulo = item.title.text if item.title else ""
        titulo_limpo = titulo.strip()
        if titulo_limpo: 
            noticias.append(titulo_limpo)
            if len(noticias) == 5:
                break
        
    texto_bruto_site = "\n".join(noticias)

except Exception as e:
    print(f"Erro ao acessar o site: {e}")
    texto_bruto_site = ""

if texto_bruto_site:
    print("2. Analisando as notícias com a IA (Llama 3.1)...\n")
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system", 
                "content": "Você é um analista de mercado. Você DEVE responder obrigatoriamente em formato JSON."
            },
            {
                "role": "user", 
                "content": f"Classifique o sentimento (Positivo, Negativo ou Neutro) das seguintes manchetes. Devolva um objeto JSON com uma chave 'noticias' contendo uma lista com 'manchete' e 'sentimento'.\n\nManchetes:\n{texto_bruto_site}"
            }
        ],
        "response_format": {"type": "json_object"} 
    }

    resposta_ia = requests.post(url_groq, headers=headers_groq, json=payload)

    if resposta_ia.status_code == 200:
        resultado = resposta_ia.json()['choices'][0]['message']['content']
        dados_json = json.loads(resultado)
        
        mensagem_final = "📊 *RESUMO DO MERCADO*\n\n"
        
        for item in dados_json.get("noticias", []):
            sentimento = item.get('sentimento', 'NEUTRO').upper()
            manchete = item.get('manchete', '')
            
            if "POSITIVO" in sentimento:
                emoji = "🟢"
            elif "NEGATIVO" in sentimento:
                emoji = "🔴"
            else:
                emoji = "⚪"
                
            mensagem_final += f"{emoji} *{sentimento}*\n{manchete}\n\n"
        
        print("3. Preparando para enviar via WhatsApp...\n")
        enviar_mensagem_whatsapp(mensagem_final)
            
    else:
        print(f"Erro na IA: Status {resposta_ia.status_code}\nDetalhes: {resposta_ia.text}")
else:
    print("O processo parou porque nenhuma notícia foi extraída.")
