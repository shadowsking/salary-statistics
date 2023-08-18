import statistics

from terminaltables import AsciiTable


def predict_salary(salary_from: int = None, salary_to: int = None) -> int | None:
    if not salary_from and not salary_to:
        return

    average_salary = None
    if salary_from and salary_to:
        average_salary = statistics.mean([salary_from, salary_to])
    elif salary_from and not salary_to:
        average_salary = salary_from * 1.2
    elif salary_to and not salary_from:
        average_salary = salary_to * 0.8

    average_salary = round(average_salary, 0)
    return int(average_salary)


def create_table(salaries: dict, title: str):
    table_statistics = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language, salary_statistics in salaries.items():
        if not salary_statistics:
            continue

        ordered_columns = ["vacancies_found", "vacancies_processed", "average_salary"]
        row = [language, *map(salary_statistics.get, ordered_columns)]
        table_statistics.append(row)

    table_instance = AsciiTable(table_statistics, title)
    return table_instance.table
