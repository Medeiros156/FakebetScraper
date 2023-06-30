import scrapy
import json
from unidecode import unidecode

class DafabetSpider(scrapy.Spider):
    name = 'dafabet'
    start_urls = ['https://www.dafabet.com/pt/dfgoal/sports/240-football/22977-brazil/22980-brasileiro-serie-a']

    def parse(self, response):
        # Extract the XHR URL from the response or any other way
        xhr_url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=22980&sortByEventpath=true&sortByEventpathIds=211990%2C18008522%2C18008523%2C18130920%2C25675278%2C25675280%2C42868%2C23234%2C22934%2C22977%2C23332%2C22896%2C22915%2C27073%2C22925%2C23025%2C23404%2C23375%2C23168%2C27057%2C23462%2C70445%2C240%2C227%2C239%2C249%2C250%2C226%2C1%2C3700%2C5000%2C1700%2C1250%2C238%2C1750%2C25645812%2C23237%2C218448%2C126769%2C89420%2C3502154%2C215%2C99917500%2C2700%2C22886%2C22889%2C3500%2C1300%2C1600%2C237%2C1100%2C2100%2C10199131%2C22881%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C1800%2C10999130%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=pt'

        yield scrapy.Request(xhr_url, callback=self.parse_xhr_response)

    def parse_xhr_response(self, response):
        # Process the XHR response here
        # Extract the data you need from the response
        # Example: extracting JSON data
        data = response.json()
        print('dat', data[0]['id'])
        format_data = []
        for item in data:
            team = [unidecode(t) for t in item['description'].split(' vs ')]
            p1 = item['markets'][0]['outcomes'][0]['consolidatedPrice']['currentPrice']['decimal']
            p2 = item['markets'][0]['outcomes'][1]['consolidatedPrice']['currentPrice']['decimal']
            p3 = item['markets'][0]['outcomes'][2]['consolidatedPrice']['currentPrice']['decimal']
            item = {
                'team': team,
                'p1': p1,
                'p2': p2,
                'p3': p3,
            }
            format_data.append(item)

        with open('dafabet.json', 'w') as file:
            json.dump(format_data, file)
        self.log('JSON file created.')
