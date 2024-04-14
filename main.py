from scraper import WebScraper

def main():
    urls = ['https://offshoreleaks.icij.org/investigations/pandora-papers', 'https://offshoreleaks.icij.org/investigations/paradise-papers']
    entities = ['Bancard']
    scraper = WebScraper()

    for url in urls:
        for entity in entities:
            print(scraper.scrape_website(url, entity))
            
if __name__ == "__main__":
    main()