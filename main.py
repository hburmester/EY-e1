from scraper import WebScraper

def main():
    uris = 'https://offshoreleaks.icij.org/investigations/pandora-papers'
    scraper = WebScraper(uris)
    scraper.scrape_website()
    print("Maximum length of obtained data:", scraper.max_length)
    matches = scraper.find_matches('Panama')
    print(matches)

if __name__ == "__main__":
    main()