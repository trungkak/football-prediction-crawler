
import json
from neo4jrestclient.client import GraphDatabase


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

    def import_winner(self, winner_data):
        for row in winner_data:
            team1 = row['first_team']
            team2 = row['second_team']
            team1_chance = int(row[team1].strip("%"))
            team2_chance = int(row[team2].strip("%"))
            draw_chance = int(row['draw'].strip("%"))

            winner_prediction_script = """CREATE (winner_prediction:WINNER_PREDICTION 
                    {source: "%s", team1: "%s", team2: "%s", team1_chance: %i, team2_chance: %i, draw_chance: %i})
            """ % ("google", team1.title(), team2.title(), team1_chance, team2_chance, draw_chance)

            create_result = self.gdb.query(winner_prediction_script, data_contents=True)
            print(create_result)

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

    def import_keonhacai(self, keonhacai_data):
        match_data = keonhacai_data[0]['data']

        worldcup_real_matches = [('Russia', 'Saudi Arabia'), ('egypt', 'uruguay'), ('morocco', 'iran'), ('portugal', 'spain')]

        for i, team in enumerate(worldcup_real_matches):

            row = match_data[i]
            #team1 = row['MATCHNAME'][0][0]
            #team2 = row['MATCHNAME'][1][0]
            team1 = team[0]
            team2 = team[1]

            keonhacai_script = """CREATE (bet_odds_prediction:BET_ODDS_PREDICTION 
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

            try:
                create_result = self.gdb.query(keonhacai_script, data_contents=True)
                print(create_result)
                print("SUCCESSFULLY CREATE KEONHACAI_PREDICTION")
            except Exception as e:
                print(e)

        merge_script = """
                        MATCH (match:MATCH)-[:BELONG_TO]->(tournament:TOURNAMENT), 
                                (bet_odds_prediction:BET_ODDS_PREDICTION) 
                            WHERE   match.team1 = bet_odds_prediction.team1 
                                AND match.team2 = bet_odds_prediction.team2 
                                AND tournament.name =~ ".*2018.*" 
                            CREATE (bet_odds_prediction)-[:PREDICT]->(match) 
                            RETURN bet_odds_prediction, match
                    """
        try:
            merge_results = self.gdb.query(merge_script, data_contents=True)
            print(merge_results)
            print("SUCCESSFULLY MERGE KEONHACAI_PREDICTION TO MATCH")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pi = PredictionDataImport("http://10.199.220.179:7474/", "neo4j", "123456")
    # pi = PredictionDataImport("http://localhost:7474/", "neo4j", "123456")

    # with open('../winner.json', 'r') as f:
    #     data = json.loads(f.read())
    #     pi.import_winner(data)

    with open('../keonhacai.json', 'r') as f:
        data = json.loads(f.read())
        pi.import_keonhacai(data)
