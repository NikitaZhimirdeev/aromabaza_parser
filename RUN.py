from datetime import datetime
import modules_parser
import config


def main():
    now = datetime.now()
    now_time = datetime.now().strftime("%d_%m_%Y__%H-%M")

    print("Ключ -   Категория\n\n"
          "1    -   Бренды\n"
          "2    -   Категории")

    key = input('\nВведите ключ того, что вас интересует (1, либо 2): ')
    # key = '2'

    if key == '1':
        modules_parser.save_head(now_time, 'BREND')

        # Собираем ссылки на все брэнды
        ALL_brends = modules_parser.find_all_hrefs_brend()
        # print(ALL_brends)
        print()

        # Создаем сообщение со всеми брендами
        print(modules_parser.create_mes_all_brebds(ALL_brends))

        kategorii = input('\nВведите ключ(и) тех брендов, которые необходимо собрать (Пример 2,3,10,13,19): ')
        kategorii = kategorii.replace(' ', '').strip(',').split(',')
        # kategorii = ['0']
        # print(kategorii)
        print()

        # Собираем все данные по выбранным категориям
        if '0' in kategorii:
            kategorii = []
            i = 0
            for brend in ALL_brends:
                i += 1
                # if i <= 25:
                #     continue
                kategorii.append(brend)

            modules_parser.find_all_info(kategorii, ALL_brends, now_time, 'BREND')

        else:
            modules_parser.find_all_info(kategorii, ALL_brends, now_time, 'BREND')

        print()
        print(f'Время работы = {datetime.now() - now}')

    elif key == '2':
        modules_parser.save_head(now_time, 'Categorii')

        # Создаем сообщение со всеми категориями
        print(modules_parser.create_mes_all_brebds(config.URLS_categorii))

        kategorii = input('\nВведите ключ(и) тех брендов, которые необходимо собрать (Пример 2,3,10,13,19): ')
        kategorii = kategorii.replace(' ', '').strip(',').split(',')
        # kategorii = ['9']
        print(kategorii)

        # Собираем все данные по выбранным категориям
        if '0' in kategorii:
            kategorii = []
            i = 0
            for brend in config.URLS_categorii:
                i += 1
                # if i <= 25:
                #     continue
                kategorii.append(brend)

            modules_parser.find_all_info(kategorii, config.URLS_categorii, now_time, 'Categorii')

        else:
            modules_parser.find_all_info(kategorii, config.URLS_categorii, now_time, 'Categorii')


        print(f'Время работы = {datetime.now() - now}')

    else:
        print('Ввели не правильный ключ')


if __name__ == '__main__':
    main()



