import time

import requests

from salary_helpers import predict_salary


def fetch_areas_ids(location: str) -> list:
    response = requests.get(
        "https://api.hh.ru/suggests/areas", params={"text": location}
    )
    response.raise_for_status()

    return [area.get("id") for area in response.json().get("items")]


def fetch_vacancies(text: str, area: list, page: int = None) -> dict:
    payload = {
        "text": text,
        "area": area,
        "page": page,
        "per_page": 100,
    }

    attempt = 0
    max_attempts = 5
    attempt_interval = 15
    while attempt < max_attempts:
        try:
            response = requests.get("https://api.hh.ru/vacancies", params=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as ex:
            if attempt == max_attempts:
                raise ex

            attempt += 1
            time.sleep(attempt_interval)


def get_vacancies_from_hh(text: str, area_ids: list) -> dict:
    page = 0
    vacancies = {}
    while True:
        response_vacancies = fetch_vacancies(text, area_ids, page)
        vacancies.setdefault("found", response_vacancies["found"])
        vacancies.setdefault("items", []).extend(response_vacancies.get("items"))
        page += 1
        if page >= response_vacancies.get("pages"):
            break

    return vacancies


def predict_rub_salary_hh(vacancy: dict) -> int | None:
    salary = vacancy.get("salary")
    if not salary or salary.get("currency") != "RUR":
        return

    return predict_salary(salary.get("from"), salary.get("to"))
