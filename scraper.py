import time
import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self):
        self.last_request_time = time.time()
        self.request_interval = 60 / 20  # 20 requests per minute

    def throttle_requests(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_request_time
        if elapsed_time < self.request_interval:
            time.sleep(self.request_interval - elapsed_time)
        self.last_request_time = time.time()

    def scrape_website(self, url, entity_to_match):
        self.throttle_requests()

        def extract_and_filter_text(tags, entity_to_match):
            def extract_text(tags, attr=None):
                return [tag.get_text() if not attr else tag[attr] for tag in tags]

            text_list = extract_text(tags)
            filtered_text = [text for text in text_list if str(entity_to_match).lower() in text.lower()]
            return filtered_text

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

            matching_entities.extend(extract_and_filter_text(entities_tags, entity_to_match))
            matching_jurisdictions.extend(extract_and_filter_text(jurisdiction_tags, entity_to_match))
            matching_linked_to.extend(extract_and_filter_text(linked_to_tags, entity_to_match))

            more_results_button = soup.find('a', class_='btn btn-dark font-weight-bold')
            if more_results_button:
                url = 'https://offshoreleaks.icij.org/' + more_results_button['href']
            else:
                break

        data_from = soup.find('div', class_='source-header__container__label m-0 text-uppercase h4 font-weight-bold').get_text()

        return { 'Matching Entities: ': matching_entities, 
                'Matching Jurisdictions: ' : matching_jurisdictions,
                'Matching Links: ' : matching_linked_to ,
                'Data From: ' : data_from,
                'Count: ' : int(len(matching_entities) + len(matching_jurisdictions) + len(matching_linked_to)) }
