import pprint
import unicodedata
from collections import OrderedDict

def all_stat(total_dict, nickname):
    biggest_plays = most_play(total_dict, nickname)
    biggest_total_wr, worst_total_wr = best_mono(total_dict)
    biggest_red_wr = best_mono_red(total_dict)
    biggest_black_wr = best_mono_black(total_dict)
    best_against_wr, worst_against_wr = best_against(total_dict)
    result_list = ([biggest_plays, biggest_total_wr, biggest_red_wr, biggest_black_wr, worst_total_wr, best_against_wr, worst_against_wr])
    return result_list


def most_play(total_dict, nickname):
    result = []
    sorted_list = OrderedDict(sorted(total_dict.items(), key=lambda x: int(x[1][0].split(': ')[1]), reverse=True))
    counter = 0
    clean_nickname = unicodedata.normalize("NFKD", nickname).strip().lower()
    for key, value in sorted_list.items():
        clean_key = unicodedata.normalize("NFKD", nickname).strip().lower()
        if counter == 3:
            break
        # if clean_key == clean_nickname:
        #     continue
        result.append(f'{key}: {value[0]}')
        counter += 1

    return result


def best_mono(total_dict):
    result_dict = {}
    result_list_good = []
    result_list_bad = []
    range_count = 0
    sort_dict = OrderedDict(sorted(total_dict.items(), key=lambda x: int(x[1][1].split(': ')[1]), reverse=True))
    for key, value in sort_dict.items():
        if range_count == 50:
            break
        all_games = None
        wins = None
        for item in value:
            if 'Игр в одноцвете' in item:
                all_games = int(item.split(': ')[1])
            if 'Побед в одноцвете' in item:
                wins = int(item.split(': ')[1])
        if all_games is not None and wins is not None:
            result_dict[key] = [calculate_winrate(wins, all_games - wins), all_games]
        range_count += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list_good.append(f'{key}: винрейт: {value[0]}%, игр: {value[1]}')
        counter += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1]))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list_bad.append(f'{key}: винрейт: {value[0]}%, игр: {value[1]}')
        counter += 1
    return result_list_good, result_list_bad


def best_mono_red(total_dict):
    result_dict = {}
    result_list = []
    range_counter = 0
    sort_dict = OrderedDict(sorted(total_dict.items(), key=lambda x: int(x[1][4].split(': ')[1]), reverse=True))
    for key, value in sort_dict.items():
        if range_counter == 35:
            break
        all_games = None
        wins = None
        for item in value:
            if 'Игр в красном одноцвете' in item:
                all_games = int(item.split(': ')[1])
            if 'Побед в красном одноцвете' in item:
                wins = int(item.split(': ')[1])
        if all_games is not None and wins is not None:
            result_dict[key] = [calculate_winrate(wins, all_games - wins), all_games]
        range_counter += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list.append(f'{key}: винрейт: {value[0]}%, игр: {value[1]}')
        counter += 1
    return result_list


def best_mono_black(total_dict):
    result_dict = {}
    result_list = []
    range_counter = 0
    sort_dict = OrderedDict(sorted(total_dict.items(), key=lambda x: int(x[1][7].split(': ')[1]), reverse=True))
    for key, value in sort_dict.items():
        if range_counter == 10:
            break
        all_games = None
        wins = None
        for item in value:
            if 'Игр в черном одноцвете' in item:
                all_games = int(item.split(': ')[1])
            if 'Побед в черном одноцвете' in item:
                wins = int(item.split(': ')[1])
        if all_games is not None and wins is not None:
            result_dict[key] = [calculate_winrate(wins, all_games - wins), all_games]
        range_counter += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list.append(f'{key}: винрейт: {value[0]}% игр: {value[1]}')
        counter += 1
    return result_list


def best_against(total_dict):
    result_dict = {}
    result_list_good = []
    result_list_bad = []
    range_counter = 0
    sort_dict = OrderedDict(sorted(total_dict.items(), key=lambda x: int(x[1][10].split(': ')[1]), reverse=True))
    for key, value in sort_dict.items():
        if range_counter == 40:
            break
        all_games = None
        wins = None
        for item in value:
            if 'Игр в разноцвете' in item:
                all_games = int(item.split(': ')[1])
            if 'Побед в разноцвете' in item:
                wins = int(item.split(': ')[1])
        if all_games is not None and wins is not None:
            result_dict[key] = [calculate_winrate(wins, all_games - wins), all_games]
        range_counter += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list_good.append(f'{key}: винрейт: {value[0]}% игр: {value[1]}')
        counter += 1

    sorted_dict = OrderedDict(sorted(result_dict.items(), key=lambda item: item[1]))
    counter = 0
    for key, value in sorted_dict.items():
        if counter == 3:
            break
        result_list_bad.append(f'{key}: винрейт: {value[0]}% игр: {value[1]}')
        counter += 1
    return result_list_good, result_list_bad


def calculate_winrate(wins, loses):
    if wins + loses == 0:
        return 0
    return round((wins / (wins + loses)) * 100)