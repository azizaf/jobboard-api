import pymongo
from titanscraper import TitanScraper
SOURCES_FILE = "sources.txt"


def load_sources():
    """Loads the file that contains all the source targets for the spider to scrap"""
    try:
        file = open(SOURCES_FILE, encoding="utf-8")
    except FileNotFoundError:
        raise
    else:
        sources = ( link.strip() for link in file.readlines() )
        file.close()
        return sources


def get_items_from_data(data):
    """Get the job items from the json data. Different sources has different access tress from the parsed data"""
    return data['rss']['channel']['item']


def main():
    """The main fuction, nothing to say about this"""
    scraper = TitanScraper()
    sources = load_sources()

    for source in sources:
        _, resource = scraper.load_resource(source)
        data = scraper.xml_to_dict(resource)

        items = get_items_from_data(data)
        for item in items:
            print(item['title'])


if __name__ == "__main__":
    main()