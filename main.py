from scraper import WebScraper
import threading

def main():
    urls = ['https://offshoreleaks.icij.org/investigations/pandora-papers', 'https://offshoreleaks.icij.org/investigations/paradise-papers']
    entities = ['Bancard']
    scraper = WebScraper()

    threads = []
    for url in urls:
        for entity in entities:
            thread = threading.Thread(target=scraper.scrape_website, args=(url,entity))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()
        result = scraper.max_length
        print(f'Maximum length: {result}')

if __name__ == "__main__":
    main()