import requests
from bs4 import BeautifulSoup
import time

class WebScraper:
    max_calls_per_minute = 20

    def __init__(self):
        self.max_length = 0

    def scrape_website(self, urls):
        def extract_text(tags, attr=None):
            return [tag.get_text() if not attr else tag[attr] for tag in tags]

        self.entities_text = []
        self.jurisdiction_text = []
        self.linked_to_text = []

        for url in urls:
            limit = 0
            calls = 0
            start_time = time.time()

            while True:
                response = requests.get(url)
                calls += 1
                if calls > self.max_calls_per_minute:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 60:
                        time.sleep(60 - elapsed_time)
                        calls = 0
                        start_time = time.time()

                if response.status_code != 200:
                    print(f'Failed to fetch data from {url}. Status code:', response.status_code)
                    break

                soup = BeautifulSoup(response.text, 'html.parser')
                entities_values = soup.find_all('a', class_='font-weight-bold text-dark')
                jurisdiction_values = soup.find_all('td', class_='jurisdiction')
                linked_to_values = soup.find_all('td', class_='country')

                self.entities_text.extend(extract_text(entities_values))
                self.jurisdiction_text.extend(extract_text(jurisdiction_values))
                self.linked_to_text.extend(extract_text(linked_to_values))

                more_results_button = soup.find('a', class_='btn btn-dark font-weight-bold')
                if not more_results_button or limit > 5:
                    break

                limit += 1
                url = 'https://offshoreleaks.icij.org/' + more_results_button['href']

            data_from = soup.find('div', class_='source-header__container__label m-0 text-uppercase h4 font-weight-bold')

        self.max_length = max(len(self.entities_text), len(self.jurisdiction_text), len(self.linked_to_text))

    def find_matches(self, entity_to_match):
        matching_entities = [entity for entity in self.entities_text if entity_to_match.lower() in entity.lower()]
        matching_jurisdictions = [jurisdiction for jurisdiction in self.jurisdiction_text if entity_to_match.lower() in jurisdiction.lower()]
        matching_linked_to = [linked_to for linked_to in self.linked_to_text if entity_to_match.lower() in linked_to.lower()]

        return { 'Matching Entities: ': matching_entities, 
                'Matching Jurisdictions: ' : matching_jurisdictions,
                 'Matching Links: ' : matching_linked_to ,
                 'Count: ' : int(len(matching_entities) + len(matching_jurisdictions) + len(matching_linked_to)) }
