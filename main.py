
import schedule
import time
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
from betfair import BetfairSpider
from dafabet import DafabetSpider

# Set up the MongoDB client
client = MongoClient('mongodb://mongodb:27017/')
db = client['betting_data']

# Set up the scheduler
def run_scraper():
    # Create a new CrawlerProcess with custom settings
    process = CrawlerProcess(get_project_settings())

    # Add your scraper spiders to the process
    process.crawl(BetfairSpider)
    process.crawl(DafabetSpider)

    # Start the scraping process
    process.start()

    # Load data from JSON files
    with open('betfair.json') as file:
        betfair_data = json.load(file)
    # with open('dafabet.json') as file:
        # dafabet_data = json.load(file)

    # Store data in MongoDB
    db['betfair_data'].insert_many(betfair_data)
    # db['dafabet_data'].insert_many(dafabet_data)

# Schedule the script to run daily at a specific time
# schedule.every().day.at("14:01").do(run_scraper)
schedule.every(2).minutes.do(run_scraper)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)
