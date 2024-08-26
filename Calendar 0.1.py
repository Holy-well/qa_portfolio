#!/usr/bin/env python
# coding: utf-8

# In[7]:


import datetime
from itertools import combinations, cycle

def input_number(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Введите число в диапазоне от {min_value} до {max_value}.")
        except ValueError:
            print("Введите корректное число.")

def input_teams(num_teams):
    teams = []
    for i in range(1, num_teams + 1):
        name = input(f"Введите имя команды {i} (или нажмите Enter для Club {i}): ")
        if not name:
            name = f"Club {i}"
        teams.append(name)
    return teams

def input_date(prompt):
    while True:
        try:
            date = input(prompt)
            return datetime.datetime.strptime(date, "%m/%Y")
        except ValueError:
            print("Введите дату в формате MM/YYYY.")

def generate_schedule(teams, num_games, start_date, duration_weeks):
    num_teams = len(teams)
    if num_teams % 2 != 0:
        teams.append(None)  # Добавляем виртуальную команду для нечетного числа команд

    # Генерация всех матчей
    matches = list(combinations(teams, 2))
    matches = matches * num_games  # Умножаем матчи на количество игр

    # Разделение матчей на туры
    rounds = []
    for i in range(0, len(matches), num_teams // 2):
        rounds.append(matches[i:i + num_teams // 2])

    # Планирование дат туров
    schedule = []
    current_date = start_date
    optimal_interval = datetime.timedelta(weeks=1)
    min_interval = datetime.timedelta(days=3)

    for i, round_matches in enumerate(rounds):
        if i > 0:
            if current_date + min_interval > start_date + datetime.timedelta(weeks=duration_weeks):
                print("Ошибка: соревнование выходит за рамки указанной длительности.")
                return

            current_date += optimal_interval
            if current_date > start_date + datetime.timedelta(weeks=duration_weeks):
                current_date -= optimal_interval - min_interval

        schedule.append((current_date, round_matches))

    return schedule

def print_schedule(schedule):
    for i, (date, matches) in enumerate(schedule):
        print(f"Tour {i + 1} - {date.strftime('%d/%m/%Y')}")
        for match in matches:
            if match[0] is None or match[1] is None:
                continue
            print(f"{match[0]} vs {match[1]}")
        print()

def main():
    # Ввод данных
    num_teams = input_number("Введите количество команд (от 2 до 24): ", 2, 24)
    teams = input_teams(num_teams)
    num_games = input_number("Введите количество игр между командами (от 1 до 4): ", 1, 4)
    start_date = input_date("Введите дату начала соревнования (MM/YYYY): ")
    duration_weeks = input_number("Введите длительность соревнования в неделях (от 1 до 520): ", 1, 520)

    # Генерация расписания
    schedule = generate_schedule(teams, num_games, start_date, duration_weeks)

    if schedule:
        # Вывод расписания
        print_schedule(schedule)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




