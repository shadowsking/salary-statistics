import time

import requests

from salary_helpers import predict_salary


def fetch_areas_ids(location: str = None) -> list:
    if not location:
        return []

    response = requests.get(
        "https://api.hh.ru/suggests/areas", params={"text": location}
    )
    response.raise_for_status()

    areas_ids = []
    for area in response.json().get("items"):
        areas_ids.append(area.get("id"))

    return areas_ids


def fetch_vacancies(text: str, area: list, page: int = None) -> dict:
    payload = {
        "professional_role": 96,
        "text": text,
        "area": area,
        "page": page,
        "per_page": 100,
        "only_with_salary": True,
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


def get_vacancies_from_hh(text: str, location: str = None) -> dict:
    area_ids = fetch_areas_ids(location)
    page = 0
    vacancies = {}
    while True:
        response_object = fetch_vacancies(text, area_ids, page)
        vacancies.setdefault("found", response_object["found"])
        items = vacancies.setdefault("items", [])
        items.extend(response_object.get("items"))
        page += 1
        if page >= response_object.get("pages"):
            break

    return vacancies


def predict_rub_salary_hh(vacancy: dict) -> int | None:
    salary = vacancy.get("salary")
    if not salary or salary.get("currency") != "RUR":
        return

    return predict_salary(salary.get("from"), salary.get("to"))
