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


def get_vacancies_from_sj(api_key: str, text: str, town_ids: list) -> dict:
    page = 0
    vacancies = {}
    while True:
        response_vacancies = fetch_vacancies(api_key, text, town_ids, page)
        vacancies["found"] = response_vacancies.get("total")
        vacancies.setdefault("items", []).extend(response_vacancies.get("objects"))
        page += 1

        if not response_vacancies.get("more"):
            break

    return vacancies


def predict_rub_salary_sj(vacancy: dict) -> int | None:
    if vacancy.get("currency") != "rub":
        return

    return predict_salary(vacancy.get("payment_from"), vacancy.get("payment_to"))
