from scraper import WebScraper

def main():
    url = 'https://offshoreleaks.icij.org'
    sub_url = ['/investigations/pandora-papers', '/investigations/paradise-papers', '/investigations/panama-papers', '/investigations/bahamas-leaks', '/investigations/offshore-leaks']
    urls = [url + str(sub_url[i]) for i in range(len(sub_url))]
    entities = ['bancard', 'cabo verde']
    scraper = WebScraper()

    for url in urls:
        for entity in entities:
            print(scraper.scrape_website(url, entity))
            
if __name__ == "__main__":
    main()