import requests
import pandas
from io import BytesIO, StringIO
from prefect import flow, task
from prefect.filesystems import RemoteFileSystem
from prefect.tasks import task_input_hash

files_raw = RemoteFileSystem.load("raw-s3")
files_processed = RemoteFileSystem.load("processed-s3")


@task(cache_key_fn=task_input_hash)
def load_raw_excel(url, sheet_name):
    r = requests.get(url)
    open("temp.xls", "wb").write(r.content)
    df = pandas.read_excel("temp.xls", sheet_name=sheet_name)
    return df


@task(cache_key_fn=task_input_hash)
def load_raw_csv(url):
    r = requests.get(url).content
    df = pandas.read_csv(StringIO(r.decode("utf-8")))
    return df


@task
def transform_age_dataset(age_df):
    df = age_df[
        [
            "ONSConstID",
            "ConstituencyName",
            "RegionName",
            "ConstLevel",
            "Const%",
            "Date",
            "Age group",
        ]
    ].drop_duplicates()
    # Only select the most recent 2020 data
    df = df.loc[df["Date"] == 2020]

    # Now convert long form dataset to wide form breaking down age group percentages for every constituency
    df_pivot = pandas.pivot(
        df, index="ONSConstID", columns="Age group", values="Const%"
    )
    df_pivot.columns = [f"%{i}YO" for i in df_pivot.columns]

    # Combine wide for age breakdown with long form population stats
    df = df.groupby(["ONSConstID", "ConstituencyName", "RegionName"], as_index=False)[
        "ConstLevel"
    ].sum()
    df = df.set_index("ONSConstID")
    df = pandas.concat([df, df_pivot], axis=1)
    return df


@task
def transform_constituency_map_data():
    # Data comes from https://geoportal.statistics.gov.uk/datasets/ons::westminster-parliamentary-constituencies-december-2022-uk-bfc/explore
    df = pandas.read_csv(
        StringIO(
            files_raw.read_path(
                "/uk_demographics/Westminster_Parliamentary_Constituencies_(December_2022)_UK_BFC.csv"
            ).decode("utf-8")
        )
    )
    # Convert metres squared to kilometers squared
    df["SHAPE_Area"] = df["SHAPE_Area"] / 1000000
    return df


@flow(name="UK Demographics", log_prints=True)
def main():
    url = "https://data.parliament.uk/resources/constituencystatistics/PowerBIData/Demography/Population.xlsx"
    df = load_raw_excel(url=url, sheet_name="Age group data")
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer)
    files_raw.write_path("/uk_demographics/population_data.csv", csv_buffer.getvalue())

    csv_buffer = BytesIO()
    df = transform_age_dataset(df)
    df.to_csv(csv_buffer)
    files_processed.write_path(
        "/uk_demographics/constituency_population_stats.csv", csv_buffer.getvalue()
    )

    url = "https://opendata.arcgis.com/api/v3/datasets/d66d6ff58fcc4461970ae003a5cab096_0/download/data?format=csv&spatialRefId=27700&where=1%3D1"
    df = load_raw_csv(url)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer)
    files_raw.write_path(
        "/uk_demographics/constituency_map_data.csv", csv_buffer.getvalue()
    )

    df = transform_constituency_map_data()
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer)
    files_processed.write_path(
        "/uk_demographics/constituency_map.csv", csv_buffer.getvalue()
    )


if __name__ == "__main__":
    main()
