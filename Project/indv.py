#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError


def get_student():
    """
    Запросить данные о студенте.
    """
    surname = input("Введите фамилию и инициалы: ")
    group_num = input("Введите номер группы: ")
    print('Введите оценки: ')
    grades = [int(n) for n in input().split()]

    student = {
        'name': surname,
        'group_number': group_num,
        'grades': grades
    }

    return student


def display_students(staff):
    """
    Отобразить список студентов.
    """
    # Проверить, что список студентов не пуст.
    if staff:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 14
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^14} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Оценки"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(staff, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>14} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group_number', ''),
                    ', '.join(str(el) for el in student.get('grades'))
                )
            )
        print(line)

    else:
        print("Список студентов пуст.")


def select_students(staff):
    # Сформировать список студентов, имеющих оценки 4 и 5.
    result = []
    for student in staff:
        if all(grade >= 4 for grade in student['grades']):
            result.append(student)

    # Возвратить список выбранных студентов.
    return result


def save_students(file_name, staff):
    """
    Сохранить всех учеников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    """
    Загрузить всех учеников из файла JSON.
    """
    # Загрузка схемы.
    with open("student-schema.json", "r") as schem:
        schema = json.load(schem)

    try:
        validate(instance=file_name, schema=schema)
        print("Validation succeeded!")
        with open(file_name, "r", encoding="utf-8") as fin:
            return json.load(fin)
    except ValidationError as e:
        print("Validation failed!")
        print(f"Error massage: {e.message}")


def main():
    """
    Главная функция программы.
    """
    # Список студентов.
    students = []

    # бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о работнике.
            student = get_student()

            # Добавить словарь в список.
            students.append(student)
            # Сортировка по возрастанию среднего балла
            students.sort(key=lambda x: sum(x['grades']) / 5)

        elif command == 'list':
            # Отобразить всех студентов.
            display_students(students)

        elif command == 'select':
            selected = select_students(students)
            # Отобразить выбранных студентов.
            display_students(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_students(file_name, students)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            students = load_students(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить студента;")
            print("list - вывести список студентов;")
            print("select - запросить студентов, имеющих оценки 4, 5;")
            print("help - отобразить справку;")
            print("load - загрузить данные из файла;")
            print("save - сохранить данные в файл;")
            print("exit - завершить работу с программой.")

        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
