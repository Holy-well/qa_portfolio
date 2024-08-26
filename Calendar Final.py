#!/usr/bin/env python
# coding: utf-8

# In[2]:


import datetime
from itertools import combinations

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

def round_robin(teams):
    if len(teams) % 2 != 0:
        teams.append(None)  # Добавляем виртуальную команду для нечетного числа команд

    n = len(teams)
    schedule = []

    for i in range(n - 1):
        round_matches = []
        for j in range(n // 2):
            team1 = teams[j]
            team2 = teams[n - 1 - j]
            if team1 is not None and team2 is not None:
                round_matches.append((team1, team2))
            elif team1 is not None or team2 is not None:
                round_matches.append((team1 if team1 is not None else team2, "BYE"))
        schedule.append(round_matches)
        # Rotate teams, except the first one
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    return schedule

def generate_schedule(teams, num_games, start_date, duration_weeks):
    # Генерация расписания по круговой системе
    base_schedule = round_robin(teams)
    full_schedule = base_schedule * num_games  # Повторяем расписание для каждой игры

    schedule = []
    current_date = start_date
    optimal_interval = datetime.timedelta(weeks=1)
    min_interval = datetime.timedelta(days=3)

    for i, round_matches in enumerate(full_schedule):
        if i > 0:
            current_date += optimal_interval
            if current_date > start_date + datetime.timedelta(weeks=duration_weeks):
                current_date -= optimal_interval - min_interval

        if current_date > start_date + datetime.timedelta(weeks=duration_weeks):
            print("Предупреждение: невозможно уложить все матчи в установленную длительность соревнования.")
            needed_weeks = (i + 1) * optimal_interval.days // 7
            print(f"Минимальная необходимая длительность соревнования: {needed_weeks} недель.")
            return schedule

        schedule.append((current_date, round_matches))

    total_rounds = len(full_schedule)
    estimated_weeks_needed = total_rounds

    if estimated_weeks_needed < duration_weeks:
        print("Предупреждение: Длительность соревнования значительно превышает необходимую для проведения всех туров.")
        print(f"Вы задали {duration_weeks} недель, но требуется только {estimated_weeks_needed} недель.")

    return schedule

def print_schedule(schedule):
    for i, (date, matches) in enumerate(schedule):
        print(f"Tour {i + 1} - {date.strftime('%d/%m/%Y')}")
        for match in matches:
            if match[1] == "BYE":
                print(f"{match[0]} пропускает тур.")
            else:
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




