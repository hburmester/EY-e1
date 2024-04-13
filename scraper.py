import requests
from bs4 import BeautifulSoup
import threading

class WebScraper:
    def __init__(self):
        self.max_length = 0
        self.semaphore = threading.Semaphore(20)

    def scrape_website(self, url, entity_to_match):
        with self.semaphore:
            def extract_text(tags, attr=None):
                return [tag.get_text() if not attr else tag[attr] for tag in tags]

            matching_entities = []
            matching_jurisdictions = []
            matching_linked_to = []

            for _ in range(5):
                response = requests.get(url)
                if response.status_code != 200:
                    print(f'Failed to fetch data from {url}. Status code:', response.status_code)
                    return

                soup = BeautifulSoup(response.text, 'html.parser')
                entities_tags = soup.find_all('a', class_='font-weight-bold text-dark')
                jurisdiction_tags = soup.find_all('td', class_='jurisdiction')
                linked_to_tags = soup.find_all('td', class_='country')

                entities_text = extract_text(entities_tags)
                jurisdiction_text = extract_text(jurisdiction_tags)
                linked_to_text = extract_text(linked_to_tags)

                matching_entities.extend([entity for entity in entities_text if str(entity_to_match).lower() in entity.lower()])
                matching_jurisdictions.extend([jurisdiction for jurisdiction in jurisdiction_text if str(entity_to_match).lower() in jurisdiction.lower()])
                matching_linked_to.extend([linked_to for linked_to in linked_to_text if str(entity_to_match).lower() in linked_to.lower()])

                more_results_button = soup.find('a', class_='btn btn-dark font-weight-bold')
                if more_results_button:
                    url = 'https://offshoreleaks.icij.org/' + more_results_button['href']
                else:
                    break

            data_from = soup.find('div', class_='source-header__container__label m-0 text-uppercase h4 font-weight-bold')

            self.max_length = max(len(matching_entities), len(matching_jurisdictions), len(matching_linked_to))

            print(str(matching_entities[0:10]).lower())

        return { 'Matching Entities: ': matching_entities, 
                'Matching Jurisdictions: ' : matching_jurisdictions,
                 'Matching Links: ' : matching_linked_to ,
                 'Data From: ' : data_from,
                 'Count: ' : int(len(matching_entities) + len(matching_jurisdictions) + len(matching_linked_to)) }
