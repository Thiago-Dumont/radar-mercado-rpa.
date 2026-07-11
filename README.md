# radar-mercado-rpa.
# 📊 Radar de Mercado Automático: Pipeline ETL com LLM

Este projeto é um pipeline de Automação Robótica de Processos (RPA) focado em extração de dados da web (Web Scraping) e orquestração de Inteligência Artificial. Ele atua como um observatório automatizado, monitorando fontes de notícias, analisando o sentimento do mercado e entregando relatórios estruturados.

Desenvolvido como uma solução da **Ápice Data** para transformar dados textuais brutos e desorganizados em inteligência de negócios acionável, em tempo real e sem intervenção humana.

## ⚙️ Arquitetura e Fluxo de Dados

O pipeline opera em três camadas principais (Extração, Transformação e Carga/Notificação):

1. **Extração (Web Scraping Segura):** Utiliza Python para consumir feeds públicos (RSS/XML). O script aplica técnicas de engenharia de dados para contornar proteções básicas de scraping (uso de User-Agent) e realiza a higienização prévia dos dados, removendo entradas vazias.
2. **Transformação (LLM Parsing Estruturado):** Os dados textuais brutos são processados pelo modelo **Llama 3.1 (via Groq API)**. O modelo é configurado via engenharia de prompt para atuar como um parser, extraindo o sentimento (Positivo, Negativo ou Neutro) e sendo forçado a devolver a resposta estritamente em um objeto JSON válido (`json_object`), garantindo a estabilidade da automação.
3. **Notificação (Integração de API):** O JSON estruturado é lido pelo Python, convertido em um relatório visualmente amigável com indicadores em emojis, e preparado para disparo via APIs de mensageria (como WhatsApp via CallMeBot ou Telegram).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Coleta de Dados:** `requests`, `BeautifulSoup` (bs4)
* **Inteligência Artificial:** Groq API (Modelo open-weights Llama 3.1)
* **Estruturação:** Manipulação nativa de JSON e URL Encoding (`urllib.parse`)

## 🚀 Potencial de Escala e Aplicações

A estrutura deste código atua como o "cérebro" de um motor de automação que pode ser adaptado para diversas rotinas corporativas:
* Monitoramento diário de Editais de Licitação e Diários Oficiais.
* Leitura estruturada de PDFs (notas fiscais e recibos bagunçados) para pipelines de ETL financeiros.
* Triagem automatizada de tickets de atendimento ao cliente via análise de sentimento.
