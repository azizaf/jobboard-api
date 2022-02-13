from pymongo import MongoClient
from titanscraper import TitanScraper
SOURCES_FILE = "sources.txt"


mongo_client = MongoClient()
db = mongo_client.jobboard
jobs_collection = db.jobs_collection

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
    logger = scraper.logger
    sources = load_sources()

    for source in sources:
        _, resource = scraper.load_resource(source)
        data = scraper.xml_to_dict(resource)

        items = get_items_from_data(data)
        for item in items:
            logger.info(f"Adding {item['link']} {[item['title']]} to collection")
            # check if the item is already in the collection
            if jobs_collection.find_one({'link' : item['link']}):
                logger.info("Item already in collection")
            else:
                try:
                    _id = jobs_collection.insert_one(item).inserted_id
                    logger.info(f"Item added with id {_id}")
                except Exception as e:
                    logger.error(e)


if __name__ == "__main__":
    main()