import argparse
import os
import statistics
from typing import Callable

import dotenv
from tqdm import tqdm

from headhunter import get_vacancies_from_hh, predict_rub_salary_hh
from salary_helpers import create_table
from superjob import get_vacancies_from_sj, predict_rub_salary_sj

PROGRAMMING_LANGUAGE = [
    "TypeScript",
    "Swift",
    "Scala",
    "Objective-C",
    "Shell",
    "Go",
    "C",
    "C#",
    "C++",
    "PHP",
    "Ruby",
    "Python",
    "Java",
    "JavaScript",
]


def get_vacancies_statistics(
    vacancies: dict, predict_rub_salary_method: Callable
) -> dict | None:
    salaries = []
    for vacancy in vacancies.get("items"):
        salary = predict_rub_salary_method(vacancy)
        if not salary:
            continue

        salaries.append(salary)

    if not salaries:
        return

    average_salary = round(statistics.mean(salaries), 0)
    return {
        "vacancies_found": vacancies.get("found"),
        "vacancies_processed": len(salaries),
        "average_salary": int(average_salary),
    }


def main(location=None):
    dotenv.load_dotenv()
    salary_statistics = {}
    for language in tqdm(PROGRAMMING_LANGUAGE):
        vacancies = get_vacancies_from_hh(
            text=language,
            location=location,
        )
        head_hunter = salary_statistics.setdefault("Head Hunter", {})
        head_hunter[language] = (
            get_vacancies_statistics(vacancies, predict_rub_salary_hh) or {}
        )

        vacancies = get_vacancies_from_sj(
            os.getenv("SJ_API_KEY"), text=language, location=location
        )
        super_job = salary_statistics.setdefault("Super Job", {})
        super_job[language] = (
            get_vacancies_statistics(vacancies, predict_rub_salary_sj) or {}
        )

    for platform_title, stat in salary_statistics.items():
        print(create_table(stat, f"{platform_title} {location}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Collects statistics on salaries of programming languages."
    )
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        help="Search area. (default: Moscow)",
        default="Moscow",
    )
    args = parser.parse_args()
    main(args.location)
