import telebot
from config import TOKEN
from parser import gomafia_matchs_parse

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '💬 Привет! Могу показать статистику твоих пересечений с игроками и вашей результативности за все турниры на gomafia, для этого введи айди своего ника (посмотреть можно, открыв ссылку профиля). 💬')
    bot.send_message(message.chat.id, 'Если интересен алгоритм подсчета винрейта, напишите команду /info')
    bot.send_message(message.chat.id, 'А также, если нашли ошибки в работе бота - пишите сюда @kingananaz (telegram)')

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id,
                     f'🤖Алгоритм такой:🤖\n'
                     f'Сначала идет сортировка по наибольшему кол-ву игр в соответствующем показателе\n'
                     f'В зачет по каждой категории идут разное кол-во мест в сортировке (зачем? я решил, что так репрезентативнее)\n'
                     f'Для общего винрейта в одноцветах (победы и поражения) - первые 50 строк\n'
                     f'Для винрейта в одноцвете на красной - первые 35 строк\n'
                     f'Для винрейта в одноцвете на черной - первые 10\n'
                     f'Для винрейта в разноцветах (победы и поражения) - первые 40'
                     )

@bot.message_handler()
def stat(message):
    id = message.text

    def get_stat():
        try:
            bot.send_message(message.chat.id, f'❗ Собираем информацию, потребуется какое-то время, зависит от нагрузки бота ❗ \n')
            result_list, nick = gomafia_matchs_parse(id)
        except (AttributeError, TypeError):
            bot.send_message(message.chat.id,
                             '❌ По вашему айди невозможно собрать статистику  ❌')
            return

        if result_list is None:
            bot.send_message(message.chat.id, 'Не найдено сыгранных турниров 😳')
            return

        biggest_plays = result_list[0]
        biggest_total_wr = result_list[1]
        biggest_red_wr = result_list[2]
        biggest_black_wr = result_list[3]
        worst_total_wr = result_list[4]
        best_against_wr = result_list[5]
        worst_against_wr = result_list[6]

        try:
            bot.send_message(message.chat.id,
                             f'📊 Статистика игрока {nick}\n'
                             f'😎 Больше всего сыграно игр с:\n'
                             f'1. {biggest_plays[0]}\n'
                             f'2. {biggest_plays[1]}\n'
                            f'3. {biggest_plays[2]}\n'
                            f'💯 Самый высокий винрейт на всех картах в одноцвете\n'
                            f'1. {biggest_total_wr[0]}\n'
                            f'2. {biggest_total_wr[1]}\n'
                            f'3. {biggest_total_wr[2]}\n'
                            f'💝 Самый высокий винрейт на красной в одноцвете\n'
                            f'1. {biggest_red_wr[0]}\n'
                            f'2. {biggest_red_wr[1]}\n'
                            f'3. {biggest_red_wr[2]}\n'
                            f'🖤 Самый высокий винрейт на черной в одноцвете\n'
                            f'1. {biggest_black_wr[0]}\n'
                            f'2. {biggest_black_wr[1]}\n'
                            f'3. {biggest_black_wr[2]}\n'
                            f'🤬 Самый низкий винрейт в одноцвете\n'
                            f'1. {worst_total_wr[0]}\n'
                            f'2. {worst_total_wr[1]}\n'
                            f'3. {worst_total_wr[2]}\n'
                            f'😈 Самый высокий винрейт против\n'
                            f'1. {worst_against_wr[0]}\n'
                            f'2. {worst_against_wr[1]}\n'
                            f'3. {worst_against_wr[2]}\n'
                            f'💀 Самый низкий винрейт против\n'
                            f'1. {best_against_wr[0]}\n'
                            f'2. {best_against_wr[1]}\n'
                            f'3. {best_against_wr[2]}\n'
                            )
            bot.send_message(message.chat.id,
                             f'FREE DONATION ♥ \n'
                             f'Если вы щедрый, приятный, хороший пользователь, можете поддержать разработчика любым донатом \n'
                             f'Телефон - 89513669262, Тинькофф \n'
                             f'Номер карты - 2200 7008 4224 6505 \n'
                             f'FREE DONATION ♥ \n'
                            )
        except(IndexError):
            bot.send_message(message.chat.id,
                             f'Неизвестная ошибка, напишите @kingananaz ваш ник и айди\n'
                             )
            return

    get_stat()


bot.polling(none_stop=True, timeout=100000)