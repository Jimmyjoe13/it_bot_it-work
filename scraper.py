import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional
import time
from urllib.parse import urljoin, urlparse

class ITWorkScraper:
    def __init__(self):
        self.setup_logging()
        self.base_urls = [
            'https://it-work.fr/',
            'https://blog.it-work.fr/'
        ]
        self.visited_urls = set()
        self.data_dir = 'scraped_data'
        os.makedirs(self.data_dir, exist_ok=True)

    def setup_logging(self):
        self.logger = logging.getLogger('ITWorkScraper')
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
            # Ajout du logging fichier
            filename = f'scraper_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de {url}: {str(e)}")
            return None

    def extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        contact_info = {
            'phone': [],
            'email': [],
            'address': [],
            'social_media': []
        }
        
        # Extraction des numéros de téléphone
        phone_elements = soup.find_all(string=lambda text: text and any(x in text for x in ['0', '+33']))
        for element in phone_elements:
            if any(char.isdigit() for char in element):
                contact_info['phone'].append(element.strip())

        # Extraction des emails
        email_elements = soup.find_all('a', href=lambda href: href and 'mailto:' in href)
        for element in email_elements:
            email = element['href'].replace('mailto:', '').strip()
            contact_info['email'].append(email)

        # Extraction des adresses
        address_elements = soup.find_all(['address', 'div'], class_=lambda x: x and 'address' in x.lower())
        for element in address_elements:
            contact_info['address'].append(element.get_text().strip())

        # Extraction des liens sociaux
        social_patterns = ['facebook', 'twitter', 'linkedin', 'instagram']
        social_links = soup.find_all('a', href=lambda href: href and any(pattern in href.lower() for pattern in social_patterns))
        for link in social_links:
            contact_info['social_media'].append({
                'platform': next(p for p in social_patterns if p in link['href'].lower()),
                'url': link['href']
            })

        return contact_info

    def extract_page_content(self, url: str, soup: BeautifulSoup) -> Dict:
        content = {
            'url': url,
            'title': '',
            'main_content': '',
            'meta_description': '',
            'contact_info': {},
            'links': [],
            'timestamp': datetime.now().isoformat()
        }

        # Extraction du titre
        title_tag = soup.find('title')
        if title_tag:
            content['title'] = title_tag.get_text().strip()

        # Extraction de la meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            content['meta_description'] = meta_desc.get('content', '').strip()

        # Extraction du contenu principal
        main_content = []
        
        # Articles de blog
        articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(c in str(x) for c in ['post', 'article', 'content']))
        for article in articles:
            # Extraction du texte et conservation de la structure
            for element in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol']):
                text = element.get_text().strip()
                if text:
                    main_content.append({
                        'type': element.name,
                        'content': text
                    })

        # Pages de service
        services = soup.find_all('div', class_=lambda x: x and 'service' in str(x))
        for service in services:
            service_content = service.get_text().strip()
            if service_content:
                main_content.append({
                    'type': 'service',
                    'content': service_content
                })

        content['main_content'] = main_content

        # Extraction des informations de contact
        content['contact_info'] = self.extract_contact_info(soup)

        # Extraction des liens internes
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/') or any(base_url in href for base_url in self.base_urls):
                full_url = urljoin(url, href)
                content['links'].append({
                    'url': full_url,
                    'text': link.get_text().strip() or link.get('title', '')
                })

        return content

    def save_content(self, content: Dict):
        try:
            # Création d'un nom de fichier basé sur l'URL
            parsed_url = urlparse(content['url'])
            filename = parsed_url.path.strip('/').replace('/', '_') or 'index'
            filepath = os.path.join(self.data_dir, f"{filename}.json")

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Contenu sauvegardé dans {filepath}")
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde du contenu: {str(e)}")

    def should_scrape_url(self, url: str) -> bool:
        # Vérifie si l'URL doit être scrapée
        return (
            url not in self.visited_urls and
            any(base_url in url for base_url in self.base_urls) and
            not any(ext in url for ext in ['.pdf', '.jpg', '.png', '.gif'])
        )

    def scrape_url(self, url: str, depth: int = 0, max_depth: int = 3):
        if not self.should_scrape_url(url) or depth > max_depth:
            return

        self.logger.info(f"Scraping de {url}")
        self.visited_urls.add(url)

        soup = self.get_page_content(url)
        if not soup:
            return

        # Extraction et sauvegarde du contenu
        content = self.extract_page_content(url, soup)
        self.save_content(content)

        # Pause pour éviter de surcharger le serveur
        time.sleep(2)

        # Scraping récursif des liens
        for link_info in content['links']:
            next_url = link_info['url']
            if self.should_scrape_url(next_url):
                self.scrape_url(next_url, depth + 1, max_depth)

    def run(self):
        self.logger.info("Démarrage du scraping")
        for base_url in self.base_urls:
            self.scrape_url(base_url)
        self.logger.info("Scraping terminé")

if __name__ == "__main__":
    scraper = ITWorkScraper()
    scraper.run()
