
import pandas as pd
from scrapy.selector import Selector


def get_bet_odds(url_or_source, title):
    tables = pd.read_html(url_or_source)
    bet_table = tables[0]
    bet_table.columns = ['winner', 'bet365', 'skybet',
                         'ladbrokes', 'William Hill', 'Marathon Bet',
                         'Betfair Sportsbook', 'SunBets',
                         'Paddy Power', 'Unibet', 'Coral',
                         'Betfred', 'Boylesports', 'Black Type',
                         'Betstars', 'Betway', 'BetBright',
                         '10Bet', 'Sportingbet', '188Bet',
                         '888sport', 'Bet Victor', 'Sportpesa',
                         'Spreadex', 'IGNORE_REDUNDANT_COLUMN', 'Betfair', 'Betdaq',
                         'Matchbook', 'Smarkets',
                         ]
    result = {title: {}}

    top_dealers = bet_table.dropna(axis=1)

    for i, w in enumerate(top_dealers['winner']):
        result[title][w] = []
        for dealer in top_dealers.columns[1:].values.tolist():
            result[title][w].append({dealer: top_dealers[dealer][i]})

    return result


def get_bet_ratio(source):
    ratios = {}

    for i in [1, 2, 3]:
        try:
            extracted_text = Selector(text=source) \
                                .xpath('//*[@id="highcharts-0"]/svg/g[2]/g/g/g[{}]/text/tspan/text()'.format(str(i))) \
                                .extract()[0]
            team_name, ratio = extracted_text.split()[:-1][0], extracted_text.split()[-1].strip('(|)')
            ratios[team_name] = ratio
        except:
            continue

    return ratios


def get_google_winner(source, title):
    winning_percents = {}
    team_names = title.split('-v-')
    team1 = ' '.join(team_names[0].split('-'))
    team2 = ' '.join(team_names[1].split('-'))

    try:
        team1_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/text()') \
            .extract()[0]
    except:
        team1_percent = 'ERROR'

    try:
        draw_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[2]/text()') \
            .extract()[0]
    except:
        draw_percent = 'ERROR'

    try:
        team2_percent = Selector(text=source) \
            .xpath('//*[@id="match-stats"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[3]/text()') \
            .extract()[0]
    except:
        team2_percent = 'ERROR'

    winning_percents[team1] = team1_percent
    winning_percents['draw'] = draw_percent
    winning_percents[team2] = team2_percent

    print(winning_percents)

    return winning_percents


