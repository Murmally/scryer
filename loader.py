import os
import sc2reader



def get_filename_from_path(path):
	tmp = path.split('\\')
	return tmp[len(tmp) - 1]

def format_teams(replay):
    teams = list()
    for team in replay.teams:
        players = list()
        for player in team:
            players.append("({0}) {1}".format(player.pick_race[0], player.name))
        formattedPlayers = '\n         '.join(players)
        teams.append("Team {0}:  {1}".format(team.number, formattedPlayers))
    return '\n'.join(teams)
    
def format_replay_header(replay):
	ret_val = """
{file}
----------------------------------
{category} Game, {start_time}
{type} on {map_name}
Length: {game_length}s
Teams:
{formatted_teams}
""".format(file=get_filename_from_path(replay.filename) , formatted_teams=format_teams(replay), **replay.__dict__)
	return ret_val


# Based on user's input this function loads appropriate replays.
def get_files_to_parse():
	replay = sc2reader.load_replays(os.getcwd())
	return replay
