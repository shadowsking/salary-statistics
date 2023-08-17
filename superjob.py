import requests
from salary_helpers import predict_salary


def fetch_town_ids(api_key: str, location: str = None):
    payload = {"keyword": location}
    response = requests.get(
        "https://api.superjob.ru/2.0/towns/",
        params=payload,
        headers={"X-Api-App-Id": api_key},
    )
    response.raise_for_status()

    town_ids = []
    for area in response.json().get("objects"):
        town_ids.append(area.get("id"))

    return town_ids


def fetch_vacancies(
    api_key: str, text: str, towns: list = None, page: int = None
) -> dict:
    payload = {
        "keyword": text,
        "t": towns,
        "page": page,
    }
    response = requests.get(
        "https://api.superjob.ru/2.0/vacancies/",
        params=payload,
        headers={"X-Api-App-Id": api_key},
    )
    response.raise_for_status()
    return response.json()


def get_vacancies_from_sj(api_key: str, text: str, location: str = None):
    towns = fetch_town_ids(api_key, location)
    page = 0
    vacancies = {}
    while True:
        response_object = fetch_vacancies(api_key, text, towns, page)

        vacancies["found"] = response_object.get("total")

        items = vacancies.setdefault("items", [])
        items.extend(response_object.get("objects"))

        page += 1

        if not response_object.get("more"):
            break

    return vacancies


def predict_rub_salary_sj(vacancy: dict) -> int | None:
    if vacancy.get("currency") != "rub":
        return

    return predict_salary(vacancy.get("payment_from"), vacancy.get("payment_to"))
