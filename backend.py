from bs4 import BeautifulSoup
from other_funcs import get_request


def get_nickname(id):
    url = f'https://gomafia.pro/stats/{id}'
    response = get_request(url)
    soup = BeautifulSoup(response, 'lxml')
    nick = soup.find('div', class_='ProfileUserInfo_profile-user__name__iJAAE').text
    return nick


def get_tour_links(id):
    tour_hrefs = []
    pages = get_pages(id)
    for page in range(1, pages + 1):
        url = f'https://gomafia.pro/stats/{id}?tab=history&page={page}'
        response = get_request(url)
        soup = BeautifulSoup(response, 'lxml')
        tournaments = soup.find_all('a', class_='Links_links__c3oXE Links_links_primary__fsjS6')

        for tour in tournaments:
            link = tour.get('href')
            tour_hrefs.append('https://gomafia.pro/' + link)

    return tour_hrefs


def get_pages(id):
    url = f'https://gomafia.pro/stats/{id}?tab=history&page=1'
    response = get_request(url)
    soup = BeautifulSoup(response, 'lxml')
    pages_count_obj = soup.find_all('div', class_='Pagination_pagination__page___s0V8')
    try:
        count_pages = int(pages_count_obj[-1].text)
    except IndexError:
        count_pages = 1
    return count_pages


def dict_handler(result_dict):
    total_dict = {}



    for key, value in result_dict.items():
        monochrome_game_count_red = 0
        monochrome_game_count_red_win = 0
        monochrome_game_count_black = 0
        monochrome_game_count_black_win = 0
        colorful_game_count = 0
        colorful_game_count_win = 0

        total_dict[key] = [f'Совместных игр всего: {len(value)}']
        for element in value:
            not_main_role, main_role, win_main = element[0], element[1], element[3]
            if main_role == 'Мир' or main_role == 'Шер':
                if not_main_role == 'Мир' or not_main_role == 'Шер':
                    monochrome_game_count_red += 1
                    if win_main == 'win':
                        monochrome_game_count_red_win += 1
                elif not_main_role == 'Дон' or not_main_role == 'Маф':
                    colorful_game_count += 1
                    if win_main == 'win':
                        colorful_game_count_win += 1
            elif main_role == 'Маф' or main_role == 'Дон':
                if not_main_role == 'Маф' or not_main_role == 'Дон':
                    monochrome_game_count_black += 1
                    if win_main == 'win':
                        monochrome_game_count_black_win += 1
                elif not_main_role == 'Мир' or not_main_role == 'Шер':
                    colorful_game_count += 1
                    if win_main == 'win':
                        colorful_game_count_win += 1

        total_dict[key].append(f'Игр в одноцвете: {monochrome_game_count_red + monochrome_game_count_black}')
        total_dict[key].append(f'Побед в одноцвете: {monochrome_game_count_black_win + monochrome_game_count_red_win}')
        total_dict[key].append(f'Поражений в одноцвете: {(monochrome_game_count_red + monochrome_game_count_black) - (monochrome_game_count_red_win + monochrome_game_count_black_win)}')
        total_dict[key].append(f'Игр в красном одноцвете: {monochrome_game_count_red}')
        total_dict[key].append(f'Побед в красном одноцвете: {monochrome_game_count_red_win}')
        total_dict[key].append(f'Поражений в красном одноцвете: {monochrome_game_count_red - monochrome_game_count_red_win}')
        total_dict[key].append(f'Игр в черном одноцвете: {monochrome_game_count_black}')
        total_dict[key].append(f'Побед в черном одноцвете: {monochrome_game_count_black_win}')
        total_dict[key].append(f'Поражений в черном одноцвете: {monochrome_game_count_black - monochrome_game_count_black_win}')
        total_dict[key].append(f'Игр в разноцвете: {colorful_game_count}')
        total_dict[key].append(f'Побед в разноцвете: {colorful_game_count_win}')
        total_dict[key].append(f'Поражений в разноцвете: {colorful_game_count - colorful_game_count_win}')

    return total_dict