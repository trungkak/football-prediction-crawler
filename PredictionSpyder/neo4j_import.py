
import json
from neo4jrestclient.client import GraphDatabase
import argparse
import sys
import os


class PredictionDataImport(object):

    def __init__(self, uri, username, password):
        self.gdb = GraphDatabase(uri, username=username, password=password)

    def convert_to_dict(self, arr):
        D = {}
        for d in arr:
            key, val = list(d.items())[0]
            D[key] = val
        return D

    def import_bet_odds(self, bet_odds_data):
        for row in bet_odds_data:

            key, val = list(row.items())[0]

            team1, team2 = [' '.join(team.split("-")).title() for team in key.split("/")[-2].split("-v-")]
            team1_odds = self.convert_to_dict(val[team1])
            team2_odds = self.convert_to_dict(val[team2])
            draw_odds  = self.convert_to_dict(val['Draw'])

            all_sources = [elem[0] for elem in team1_odds.items()]
            for source in all_sources:
                odds_object = {
                    'team1': team1,
                    'team2': team2,
                    'team1_odds': team1_odds[source],
                    'team2_odds': team2_odds[source],
                    'draw_odds': draw_odds[source],
                    'source': source
                }

                print(odds_object)

                odds_prediction_script = """CREATE (odds:BET_ODDS_PREDICTION
                                                {source: "%s", team1: "%s", team2: "%s", team1_odds: "%s", team2_odds: "%s", draw_odds: "%s"})
                                        """ % (odds_object['source'], odds_object['team1'].title(), odds_object['team2'].title(),
                                               odds_object['team1_odds'], odds_object['team2_odds'], odds_object['draw_odds'])

                odds_results = self.gdb.query(odds_prediction_script, data_contents=True)
                print(odds_results)

        merge_script = """
                        MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT),
                                (odds_prediction:BET_ODDS_PREDICTION)
                            WHERE   match.team1 = odds_prediction.team1
                                AND match.team2 = odds_prediction.team2
                                AND tournament.name =~ ".*2018.*"
                            CREATE (odds_prediction)-[:PREDICT]->(match)
                            RETURN odds_prediction, match
                    """
        merge_results = self.gdb.query(merge_script, data_contents=True)
        print(merge_results)

    def import_winner(self, winner_data, method):
        for row in winner_data:
            team1 = row['first_team']
            team2 = row['second_team']
            team1_chance = int(row[team1].strip("%"))
            team2_chance = int(row[team2].strip("%"))
            draw_chance = int(row['draw'].strip("%"))

            if method == 'create':
                create_script = """CREATE (winner_prediction:WINNER_PREDICTION 
                        {source: "%s", team1: "%s", team2: "%s", team1_chance: %i, team2_chance: %i, draw_chance: %i})
                """ % ("google", team1.title(), team2.title(), team1_chance, team2_chance, draw_chance)

                create_result = self.gdb.query(create_script, data_contents=True)
                print(create_result)
                print('SUCCESSFULLY CREATE ON MATCH (%s - %s)' % (team1, team2))

            if method == 'update':
                update_script = """
                        MATCH (winner_prediction:WINNER_PREDICTION) 
                            WHERE   winner_prediction.team1 = '%s' 
                                AND winner_prediction.team2 = '%s' 
                            SET 
                                winner_prediction.team1_chance = %s,
                                winner_prediction.team2_chance = %s,
                                winner_prediction.draw_chance = %s
                    """ % (team1.title(),
                           team2.title(),
                           team1_chance,
                           team2_chance,
                           draw_chance)
                update_result = self.gdb.query(update_script, data_contents=True)
                print(update_result)
                print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))

        if method == 'create':
            merge_script = """
                    MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT), 
                            (winner_prediction:WINNER_PREDICTION) 
                        WHERE   match.team1 = winner_prediction.team1 
                            AND match.team2 = winner_prediction.team2 
                            AND tournament.name =~ ".*2018.*" 
                        CREATE (winner_prediction)-[:PREDICT]->(match) 
                        RETURN winner_prediction,match
                """
            merge_results = self.gdb.query(merge_script, data_contents=True)
            print(merge_results)

    def import_keonhacai(self, data, method):
        match_data = data

        for row in match_data:

            team1 = row['MATCHNAME']['team1'][0].strip().title()
            team2 = row['MATCHNAME']['team2'][0].strip().title()

            create_script = """CREATE (bet_odds_prediction:BET_ODDS_PREDICTION 
                            {
                                team1: '%s', 
                                team2: '%s', 
                                matchtime: '%s',
                                chance: '%s', 
                                dice: '%s', 
                                onextwo: '%s',
                                firsthalf_chance: '%s',
                                firsthalf_dice: '%s',
                                firsthalf_onextwo: '%s'
                            })
                    """ % (team1.title(),
                           team2.title(),
                           row['DATETIME'],
                           json.dumps(row['CATRAN-TYLE']),
                           json.dumps(row['CATRAN-TAIXIU']),
                           json.dumps(row['CATRAN-1X2']),
                           json.dumps(row['HIEP1-TYLE']),
                           json.dumps(row['HIEP1-TAIXIU']),
                           json.dumps(row['HIEP1-1X2']),
                           )

            update_script = """MATCH (bet_odds_prediction:BET_ODDS_PREDICTION)
                            WHERE bet_odds_prediction.team1 = '%s' AND bet_odds_prediction.team2 = '%s' 
                            SET
                                bet_odds_prediction.chance = '%s',
                                bet_odds_prediction.chance = '%s',
                                bet_odds_prediction.dice = '%s',
                                bet_odds_prediction.onextwo = '%s',
                                bet_odds_prediction.firsthalf_chance = '%s',
                                bet_odds_prediction.firsthalf_dice = '%s',
                                bet_odds_prediction.firsthalf_onextwo = '%s'
                    """ % (team1.title(),
                           team2.title(),
                           row['DATETIME'],
                           json.dumps(row['CATRAN-TYLE']),
                           json.dumps(row['CATRAN-TAIXIU']),
                           json.dumps(row['CATRAN-1X2']),
                           json.dumps(row['HIEP1-TYLE']),
                           json.dumps(row['HIEP1-TAIXIU']),
                           json.dumps(row['HIEP1-1X2']),
                           )

            try:
                if method == 'create':
                    create_result = self.gdb.query(create_script, data_contents=True)
                    print(create_result)
                    print('SUCCESSFULLY CREATE ON MATCH (%s - %s)' % (team1, team2))

                    merge_script = """
                                            MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT), 
                                                    (bet_odds_prediction:BET_ODDS_PREDICTION) 
                                                WHERE   match.team1 = bet_odds_prediction.team1 
                                                    AND match.team2 = bet_odds_prediction.team2 
                                                    AND tournament.name =~ ".*2018.*" 
                                                CREATE (bet_odds_prediction)-[:PREDICT]->(match) 
                                                RETURN bet_odds_prediction, match
                                        """
                    merge_results = self.gdb.query(merge_script, data_contents=True)
                    print(merge_results)
                    print("SUCCESSFULLY MERGE KEONHACAI_PREDICTION TO MATCH")

                if method == 'update':
                    update_result = self.gdb.query(update_script, data_contents=True)
                    print(update_result)
                    print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))
            except Exception as e:
                print(e)

    def import_188(self, data, method):

        for row in data:

            team1 = row['MATCHNAME']['team1']
            team2 = row['MATCHNAME']['team2']

            create_script = """CREATE (bet_odds_prediction:BET_ODDS_PREDICTION 
                            {
                                team1: '%s', 
                                team2: '%s', 
                                matchtime: '%s',
                                chance: '%s', 
                                dice: '%s', 
                                onextwo: '%s',
                                firsthalf_chance: '%s',
                                firsthalf_dice: '%s',
                                firsthalf_onextwo: '%s'
                            })
                    """ % (team1.title(),
                           team2.title(),
                           row['DATETIME'],
                           json.dumps(row['CATRAN-handicap']),
                           json.dumps(row['CATRAN-underover']),
                           json.dumps(row['CATRAN-onextwo']),
                           json.dumps(row['HIEP1-handicap']),
                           json.dumps(row['HIEP1-underover']),
                           json.dumps(row['HIEP1-onextwo']),
                           )

            update_script = """MATCH (bet_odds_prediction:BET_ODDS_PREDICTION)
                                        WHERE bet_odds_prediction.team1 = '%s' AND bet_odds_prediction.team2 = '%s' 
                                        SET
                                            bet_odds_prediction.chance = '%s',
                                            bet_odds_prediction.chance = '%s',
                                            bet_odds_prediction.dice = '%s',
                                            bet_odds_prediction.onextwo = '%s',
                                            bet_odds_prediction.firsthalf_chance = '%s',
                                            bet_odds_prediction.firsthalf_dice = '%s',
                                            bet_odds_prediction.firsthalf_onextwo = '%s'
                                """ % (team1.title(),
                                       team2.title(),
                                       row['DATETIME'],
                                       json.dumps(row['CATRAN-handicap']),
                                       json.dumps(row['CATRAN-underover']),
                                       json.dumps(row['CATRAN-onextwo']),
                                       json.dumps(row['HIEP1-handicap']),
                                       json.dumps(row['HIEP1-underover']),
                                       json.dumps(row['HIEP1-onextwo']),
                                       )

            try:
                if method == 'create':
                    create_result = self.gdb.query(create_script, data_contents=True)
                    print(create_result)
                    print('SUCCESSFULLY CREATE ON MATCH (%s - %s)' % (team1, team2))

                    merge_script = """
                                            MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT), 
                                                    (bet_odds_prediction:BET_ODDS_PREDICTION) 
                                                WHERE   match.team1 = bet_odds_prediction.team1 
                                                    AND match.team2 = bet_odds_prediction.team2 
                                                    AND tournament.name =~ ".*2018.*" 
                                                CREATE (bet_odds_prediction)-[:PREDICT]->(match) 
                                                RETURN bet_odds_prediction, match
                                        """
                    merge_results = self.gdb.query(merge_script, data_contents=True)
                    print(merge_results)
                    print("SUCCESSFULLY MERGE BET_ODDS_PREDICTION TO MATCH")

                if method == 'update':
                    update_result = self.gdb.query(update_script, data_contents=True)
                    print(update_result)
                    print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))
            except Exception as e:
                print(e)

    def import_matchscore(self, data, method):
        match_data = data

        for row in match_data:

            team1 = row['MATCHNAME']['team1'][0].strip().title()
            team2 = row['MATCHNAME']['team2'][0].strip().title()

            create_script = """CREATE (bet_odds_prediction:BET_ODDS_PREDICTION 
                            {
                                team1: '%s', 
                                team2: '%s', 
                                matchtime: '%s',
                                chance: '%s', 
                                dice: '%s', 
                                onextwo: '%s',
                                firsthalf_chance: '%s',
                                firsthalf_dice: '%s',
                                firsthalf_onextwo: '%s'
                            })
                    """ % (team1.title(),
                           team2.title(),
                           row['DATETIME'],
                           json.dumps(row['CATRAN-TYLE']),
                           json.dumps(row['CATRAN-TAIXIU']),
                           json.dumps(row['CATRAN-1X2']),
                           json.dumps(row['HIEP1-TYLE']),
                           json.dumps(row['HIEP1-TAIXIU']),
                           json.dumps(row['HIEP1-1X2']),
                           )
            result_fulltime = ''
            minute = 0
            try:
                matchtime = row['DATETIME']
                minute = matchtime.split(' ')[-1].strip("'")
                score = ' '.join(matchtime.split(' ')[:-1])
                score1, score2 = score.split("-")[0], score.split("-")[1]

                result_fulltime = {}
                result_fulltime['team1'] = team1.title()
                result_fulltime['team2'] = team2.title()
                result_fulltime['score1'] = int(score1)
                result_fulltime['score2'] = int(score2)
            except:
                print('TRAN DAU CHUA BAT DAU')
                continue

            update_script = """MATCH (match:MATCH)
                            WHERE match.team1 = '%s' AND match.team2 = '%s' 
                            SET
                                match.result_fulltime = '%s',
                                match.time = '%s' 
                    """ % (team1.title(),
                           team2.title(),
                           json.dumps(result_fulltime),
                           minute
                           )

            try:
                if method == 'create':
                    print('THIS METHOD DOES NOT ALLOW CREATING')
                    return None

                if method == 'update':
                    print(update_script)
                    update_result = self.gdb.query(update_script, data_contents=True)
                    print(update_result)
                    print('SUCCESSFULLY UPDATE ON MATCH (%s - %s)' % (team1, team2))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    pi = PredictionDataImport("http://10.199.220.179:7474/", "neo4j", "123456")

    parser = argparse.ArgumentParser(description='Index data to neo4j')
    parser.add_argument('-s', '--source', dest='source', default='188bet')

    parser.add_argument('-m', '--method', dest='method', default='update')

    args = parser.parse_args()

    if args.method not in ['update', 'create']:
        print('Only allow method from [update, create]')
        sys.exit(1)
    else:
        method = args.method

    if args.source == 'google':
        with open(os.path.abspath('winner.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_winner(data, method)

    elif args.source == 'keonhacai':
        with open(os.path.abspath('keonhacai.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_keonhacai(data, method)

    elif args.source == '188bet':
        with open(os.path.abspath('188.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_188(data, method)

    elif args.source == 'matchscore':
        with open(os.path.abspath('keonhacai.json'), 'r') as f:
            data = json.loads(f.read())
            pi.import_matchscore(data, method)

    else:
        print('Only allow source from [google, keonhacai, 188bet]')
        sys.exit(1)
