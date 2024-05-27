import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import re
import os

class AuthorFinder:
    def __init__(self, soup, deserialized_json):
        self.soup = soup
        self.deserialized_json = deserialized_json

    def find(self):
        all_link_tags = self.soup.find_all("link")
        for link_tag in all_link_tags:
            if link_tag.get("content"):
                return link_tag.get("content")

        if self.deserialized_json:
            try:
                author = self.deserialized_json["author"]["name"]
                author = author.split(" ")

                if len(author) == 3:
                    return f"{author[2]}, {author[1][0]}."
                if len(author) == 2:
                    return f"{author[1]}, {author[0][0]}."
            except Exception:
                try:
                    return self.deserialized_json["page"]["pageInfo"]["publisher"]
                except KeyError:
                    pass

        author_tag = self.soup.find(class_="blog-entry__date--full fine-print")
        if author_tag:
            author_text = author_tag.get_text()
            match = re.search(r"(?<=By ).*(?= published)", author_text)
            if match:
                author = match.group(0).split(" ")
                if len(author) == 2:
                    return f"{author[1]}, {author[0][0]}."
        
        return "No author available"

def get_meta_content(soup, meta_names):
    for meta_name in meta_names:
        meta_tag = soup.find('meta', attrs={'name': meta_name}) or soup.find('meta', attrs={'property': meta_name})
        if meta_tag and 'content' in meta_tag.attrs:
            return meta_tag['content']
    return ''

def get_publication_date(soup):
    date_names = ['article:published_time', 'og:updated_time', 'date', 'article:modified_time', 'lastmod']
    date = get_meta_content(soup, date_names)
    if date:
        try:
            date_obj = datetime.fromisoformat(date)
            return date_obj.strftime('%Y')
        except ValueError:
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
                return date_obj.strftime('%Y')
            except ValueError:
                pass
    return "No date available"

def generate_harvard_reference(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        json_ld = soup.find('script', type='application/ld+json')
        deserialized_json = json.loads(json_ld.string) if json_ld else None
        
        title_tag = soup.find('title')
        title = title_tag.text if title_tag else 'No title available'
        
        author_finder = AuthorFinder(soup, deserialized_json)
        author = author_finder.find()
        year = get_publication_date(soup)
        accessed_date = datetime.now().strftime('%d %B %Y')
        
        if author and year:
            reference = f'{author} ({year}) {title}. Available at: {url} (Accessed: {accessed_date}).'
        elif author:
            reference = f'{author} {title}. Available at: {url} (Accessed: {accessed_date}).'
        elif year:
            reference = f'({year}) {title}. Available at: {url} (Accessed: {accessed_date}).'
        else:
            reference = f'{title}. Available at: {url} (Accessed: {accessed_date}).'
        
        return reference
    except requests.RequestException as e:
        print(f'Error fetching {url}: {e}')
        return ''

def main():
    input_file = 'urls.txt'
    output_file = 'references.txt'
    
    if not os.path.isfile(input_file):
        print(f"Input file '{input_file}' not found.")
        return
    
    with open(input_file, 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]
    
    references = [generate_harvard_reference(url) for url in urls]
    
    with open(output_file, 'w') as file:
        for ref in references:
            if ref:
                file.write(ref + '\n\n')
    
    print(f'References have been written to {output_file}')

if __name__ == '__main__':
    main()
