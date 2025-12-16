import requests
from bs4 import BeautifulSoup

url = "https://ranobes.net/ranking/all_time/"
headers = {'User-Agent': 'Mozilla/5.0'}

respuesta = requests.get(url, headers=headers)

if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    novels_list = []
    

    contenido = soup.find_all('div', class_='rank-story-tools')
    
    for container in contenido:
        novela_container = container.find_parent('article') or container.find_parent('div', class_=lambda x: x and 'story' in x)
        
        if not novela_container:
            novela_container = container
        
        # TÍTULO
        title = "Sin título"
        # Buscar título en diferentes lugares
        for selector in ['h2', 'h3', 'h4', 'a.title', 'span.title']:
            title_tag = novela_container.select_one(selector)
            if title_tag:
                title = title_tag.get_text(strip=True)
                break
        
        # ENLACE
        novel_url = "#"
        link_tag = novela_container.find('a', href=True)
        if link_tag:
            novel_url = link_tag['href']
            if novel_url.startswith('/'):
                novel_url = f"https://ranobes.net{novel_url}"
            elif not novel_url.startswith('http'):
                novel_url = f"https://ranobes.net/{novel_url}"
        
        # VISTAS 
        views_span = container.find('span', class_='rank-story-data-val')
        if views_span:
            views_number = views_span.get_text(strip=True)
            views_text = f"{views_number}"
        else:
            views_text = "N/A"
        
        # DESCRIPCIÓN BREVE
        description = "Sin descripción"
        # Buscar descripción en diferentes lugares
        for selector in ['p', 'div.desc', 'div.description', 'div.excerpt', 'span.desc']:
            desc_tag = novela_container.select_one(selector)
            if desc_tag:
                desc_text = desc_tag.get_text(strip=True)
                if len(desc_text) > 20:  # Asegurar que sea una descripción real
                    description = desc_text[:150] + "..." if len(desc_text) > 150 else desc_text
                    break
        
        # Si no encontró descripción, usar parte del texto general
        if description == "Sin descripción":
            all_text = novela_container.get_text(strip=True)

            clean_text = all_text.replace(title, '').replace(views_text, '')
            if len(clean_text) > 30:
                description = clean_text[:170] + "...>>view more" if len(clean_text) > 170 else clean_text
        
        # Guardar en la lista
        novels_list.append({
            'title': title,
            'url': novel_url,
            'views': views_text,
            'description': description
        })
    
    # Mostrar resultados
    if novels_list:
        print(f"Encontradas {len(novels_list)} novelas:\n")
        for i, novel in enumerate(novels_list, 1):
            print(f"{i}. {novel['title']}\n")
            print(f"Enlace: {novel['url']}\n")
            print(f"Vistas: {novel['views']}\n")
            print(f"Descripción: {novel['description']}\n")