
import pandas as pd
from scrapy.selector import Selector
from datetime import datetime
from bs4 import BeautifulSoup, Comment


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
    winning_percents['first_team'] = team1
    winning_percents['second_team'] = team2

    return winning_percents


# Keo nha cai data

def concat_row_data(sub_table):
    result = {}
    names = ['team1', 'team2', 'draw']
    for i, tr in enumerate(sub_table.find('tbody').find_all('tr', recursive=False)):
        tds = tr.find_all('td')
        content = [td.text for td in tds if td.text.strip() != '']
        if len(content) != 0:
            result[names[i]] = content
    return result

    # result = []
    #
    # for tr in sub_table.find('tbody').find_all('tr', recursive=False):
    #     tds = tr.find_all('td')
    #     result.append([td.text for td in tds])
    # return result


def parse_row(elem):
    COLUMN_NAMES = ['DATETIME',
                    'MATCHNAME',
                    'CATRAN-TYLE',
                    'CATRAN-TAIXIU',
                    'CATRAN-1X2',
                    'HIEP1-TYLE',
                    'HIEP1-TAIXIU',
                    'HIEP1-1X2']

    match_obj = {}
    tds = elem.find_all('td', recursive=False)

    for index, name in enumerate(COLUMN_NAMES):
        td = tds[index]
        if len(td.find_all('table')) == 0:
            match_obj[name] = ' '.join(td.find_all(text=True))
        else:
            match_obj[name] = concat_row_data(td.find_all('table')[0])

    return match_obj


def get_keonhacai(source, key_term):
    current_time = datetime.utcnow()
    current_timestamp = datetime.fromtimestamp(float(current_time.timestamp())).strftime('%Y-%m-%d %H:%M:%S')

    # get the main table
    soup = BeautifulSoup(source, "lxml")
    table = soup.find("table", id="dm3")

    # get all table rows at first level
    table_rows = table.find('tbody').find_all('tr', recursive=False)

    # find the row contains key term and its index
    key_term_row = list(filter(lambda elem: len(elem.find_all('td')) == 1 and elem.text.strip() == key_term, table_rows))[0]
    key_term_row_index = table_rows.index(key_term_row)

    # find the next row the contains a term
    next_term_row = list(filter(lambda elem: len(elem.find_all('td')) == 1, table_rows[key_term_row_index + 1:]))[0]
    next_term_row_index = table_rows.index(next_term_row)

    match_data = {'timestamp': current_timestamp, 'data': []}

    for match_row in table_rows[key_term_row_index + 1: next_term_row_index]:
        match_data['data'].append(parse_row(match_row))

    return match_data


def get_oneeighteight(source, match_name):
    soup = BeautifulSoup(source, "lxml")
    bet_tables = soup.find_all("table", class_="bet-types-table")

    matches = []

    names = []

    for bet_table in bet_tables:
        table_rows = bet_table.find('tbody').find_all('tr', recursive=False)[2:] # Cause 2 first tr is metadata
        for table_row in table_rows:
            tds = table_row.find_all('td', recursive=False)
            # row_data = [td.text for td in tds if td.text.strip() != '']
            row_data = [' '.join(td.find_all(text=lambda text: not isinstance(text, Comment))) for td in tds if td.text.strip() != '']
            matches.append(row_data)
    print('*** ' + match_name + ' ***')
    return matches
