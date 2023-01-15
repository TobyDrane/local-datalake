import requests

import pandas
from pandas import DataFrame

URL = "https://randomuser.me/api/"


def extract_user_df(amount: int) -> DataFrame:
    try:
        response = requests.get(url=f"{URL}?results={amount}")
        data = response.json()
        df = pandas.DataFrame.from_dict(data["results"])
        return df
    except Exception as e:
        print(e)


def extract_user(amount: int) -> None:
    df = extract_user_df(amount)
    print(df.info())
