import unicodedata

import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def get_headers():
    headers = Headers(browser='firefox', os='win')
    return headers.generate()

def get_request(url):
    response = requests.get(url, headers=get_headers())
    return response.text


def game_handler(games_list, nickname, players_plays_dict):
    for game in games_list:
        player_stat = []
        win_team = win_or_lose_check(game)
        rows = game.find_all('tr', class_='TableTournamentResultGame_table-tournament-result-game__item__SbL_M')

        clean_row = unicodedata.normalize("NFKD", str(rows)).strip().lower()
        clean_nick = unicodedata.normalize("NFKD", nickname).strip().lower()

        if clean_nick not in clean_row:
            continue

        for row in rows:
            columns = row.find_all('td')
            table_nick = columns[1].text.strip()
            clean_table_nick = unicodedata.normalize("NFKD", table_nick).strip().lower()
            role = columns[2].text
            win_lose = game_win_result(role, win_team)
            if clean_table_nick == clean_nick:
                result = [table_nick, '', role, '', win_lose]
            else:
                result = [table_nick, role, '', win_lose, '']
            player_stat.append(result)

        game_result = game_list_format(player_stat, nickname)
        players_plays_dict = game_list_result_handler(game_result, players_plays_dict)
    return players_plays_dict



def game_list_format(game_list, nickname):
    exceptional_result = [result for result in game_list if result[2] and result[4]]

    if exceptional_result:
        exceptional_result = exceptional_result[0]
    else:
        exceptional_result = [None, None, '', None, '']

    processed_results = []

    for result in game_list:
        if nickname in result:
            continue
        if not result[2]:
            result[2] = exceptional_result[2]
        if not result[4]:
            result[4] = exceptional_result[4]
        processed_results.append(result)
    return processed_results



def tour_handler(tours, nickname, players_plays_dict):
    if len(tours) == 0:
        return
    for tour in tours:
        tour += '?tab=games'
        response = get_request(tour)
        soup = BeautifulSoup(response, 'lxml')
        games_list = soup.find_all('table', class_='TableTournamentResultGame_table-tournament-result-game__WkjoT')
        total_stat = game_handler(games_list, nickname, players_plays_dict)
    return total_stat



def win_or_lose_check(game):
    black_win = game.find('th',
                        class_='undefined TableTournamentResultGame_table-tournament-result-game__th_mafia__2o2TU')
    red_win = game.find('th',
                          class_='undefined TableTournamentResultGame_table-tournament-result-game__th_city__hmlwA')



    if red_win is not None:
        total_win = 'Победа красных'
    elif black_win is not None:
        total_win = 'Победа мафии'
    else:
        total_win = 'Не определено'

    return total_win


def game_win_result(role, win_team):
    if ((role == "Мир" or role == "Шер") and win_team == 'Победа красных') or ((role == "Маф" or role == "Дон") and win_team == 'Победа мафии'):
        game_result = 'win'
    else:
        game_result = 'lose'

    return game_result


def game_list_result_handler(result_list, players_plays_dict):
    for lst in result_list:
        key = lst[0]
        values = lst[1:5]
        if key in players_plays_dict:
            players_plays_dict[key].append(values)
        else:
            players_plays_dict[key] = [values]

    return players_plays_dict