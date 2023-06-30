import schedule
import time
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from betfair import BetfairSpider
from scores import ScoresSpider
import mysql.connector

# Set up the MySQL connection
# cnx = mysql.connector.connect(
#     host="mysql",
#     user="root",
#     port=3306,
#     password="password",
#     database="gaming_data"
# )

cnx = mysql.connector.connect(
    host="containers-us-west-44.railway.app",
    user="root",
    port=7858,
    password="0mDweMZ7ocWgn97fS55A",
    database="railway"
)


def store_games_in_mysql(table_name, data):
    cursor = cnx.cursor()
    # Prepare the SQL statement
    sql = f"INSERT INTO {table_name} (teamA, teamB, startDateTime, endDateTime," \
          " oddsA, oddsDraw, oddsB) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    try:
        # Execute the SQL statement for each data entry
        for entry in data:
            values = (
                entry['teamA'],
                entry['teamB'],
                entry['startDateTime'],
                entry['endDateTime'],
                entry['oddsA'],
                entry['oddsDraw'],
                entry['oddsB']
            )
            cursor.execute(sql, values)

        # Commit the changes to the database
        cnx.commit()
    except mysql.connector.Error as error:
        # Handle the error
        print("Error storing data in MySQL:", error)
    finally:
        # Close the cursor
        cursor.close()

def update_games_in_mysql(table_name, data):
    cursor = cnx.cursor()
    # Prepare the SQL statement
    sql = f"UPDATE {table_name} SET teamA = %s, teamB = %s, startDateTime = %s, endDateTime = %s, " \
          "oddsA = %s, oddsDraw = %s, oddsB = %s, scoreA = %s, scoreB = %s, gameStatus = %s WHERE gameId = %s"

    try:
        # Execute the SQL statement for each data entry
        for entry in data:
            values = (
                entry['teamA'],
                entry['teamB'],
                entry['startDateTime'],
                entry['endDateTime'],
                entry['oddsA'],
                entry['oddsDraw'],
                entry['oddsB'],
                entry['scoreA'],
                entry['scoreB'],
                entry['gameStatus'],
                entry['gameId']  # Assuming you have a unique gameId for each game in the database
            )
            cursor.execute(sql, values)

        # Commit the changes to the database
        cnx.commit()
    except mysql.connector.Error as error:
        # Handle the error
        print("Error updating data in MySQL:", error)
    # finally:
        # Close the cursor
        # cursor.close()
        # cnx.close()

def update_games_scores(scores_data):
    cursor = cnx.cursor(dictionary=True)
    sql = f"SELECT * FROM games WHERE gamestatus = 1"
    cursor.execute(sql)
    games_data = cursor.fetchall()
    print('GAME-DATA', games_data)
    

    for game_db in games_data:
        for game in scores_data:
            if game_db['teamA'] == game['teamA'] and game_db['teamB'] == game['teamB']:
                game_db['scoreA'] = game['scoreA']
                game_db['scoreB'] = game['scoreB']
                if game_db['scoreA'] is not None and game_db['scoreB'] is not None:
                    game_db['gameStatus'] = 0
                    update_games_in_mysql('games', [game_db])
                    break

    # cursor.close()

    # print('GAMES', games_data)
   

    # return bet_data




def run_scraper():
    # Create a new CrawlerProcess with custom settings
    process = CrawlerProcess(get_project_settings())

    # Scraper spiders to the process
    process.crawl(BetfairSpider)
    process.crawl(ScoresSpider)

    # Start the scraping process
    process.start()

    # Load data from JSON files
    with open('betfair.json') as file:
        betfair_data = json.load(file)

    # Store games data in MySQL
    store_games_in_mysql('games', betfair_data)

    with open('scores.json') as file:
        scores_data = json.load(file)

    # Store scores data in MySQL
    update_games_scores(scores_data)

schedule.every().day.at("4:01").do(run_scraper)
# schedule.every(10).seconds.do(run_scraper)

# Run the scheduler indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)