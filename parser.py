import pprint

from backend import get_nickname, get_tour_links, dict_handler
from other_funcs import tour_handler
from result_dict_operations import all_stat


def gomafia_matchs_parse(id):

    players_plays = {}

    nick = get_nickname(id)
    tour_links = get_tour_links(id)
    res = tour_handler(tour_links, nick, players_plays)
    total_dict = dict_handler(res)
    result_list = all_stat(total_dict, nick)
    return result_list, nick

