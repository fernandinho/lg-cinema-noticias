
import json
import re
import html
import urllib.request
import xml.etree.ElementTree as ET

FEEDS = [
    ("CANALTECH", "https://canaltech.com.br/rss/"),
    ("TECHTUDO", "https://www.techtudo.com.br/rss/techtudo"),
]

def limpar(texto):
    texto = re.sub(r"<[^>]+>", " ", texto or "")
    texto = html.unescape(texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()

def buscar(nome, url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as resposta:
        xml = resposta.read()

    raiz = ET.fromstring(xml)
    noticias = []

    for item in raiz.findall("./channel/item")[:10]:
        titulo = item.findtext("title", "")
        link = item.findtext("link", "")
        descricao = item.findtext("description", "")

       if titulo and link:
    noticias.append({
        "source": nome,
        "title": limpar(titulo),
        "link": link.strip(),
        "description": limpar(descricao),
        "description_html": descricao
    })

    return noticias

def main():
    listas = []

    for nome, url in FEEDS:
        try:
            noticias = buscar(nome, url)
            print(nome, len(noticias), "noticias")
            listas.append(noticias)
        except Exception as erro:
            print("Erro em", nome, erro)
            listas.append([])

    resultado = []

    for i in range(10):
        for noticias in listas:
            if i < len(noticias):
                resultado.append(noticias[i])

    if not resultado:
        raise RuntimeError("Nenhuma noticia obtida; arquivo anterior preservado.")

    with open("tech-news-data.json", "w", encoding="utf-8") as arquivo:
        json.dump(resultado, arquivo, ensure_ascii=False, indent=2)

    print("Arquivo atualizado:", len(resultado), "noticias")

if __name__ == "__main__":
    main()
