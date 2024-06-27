import argparse
import os

import pandas as pd
import math
import numpy as np
from census import Census
from us import states
from pygris import tracts
import matplotlib.pyplot as plt

from config import FIELDS, REGION, WEIGHTS
from utils import logging

# Get an API key here: https://api.census.gov/data/key_signup.html
CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")
c = Census(CENSUS_API_KEY)


def load(year):
    # we have to match the sorting of the original work
    # so this query we will merge to preserve the sorting we need
    sort_query = c.acs5.state_county_tract(
        fields=["NAME", "B01001_001E"],
        state_fips=states.TX.fips,
        county_fips="*",
        tract="*",
        year=year,
    )
    tx_census = c.acs5.state_county_tract(
        fields=FIELDS,
        state_fips=states.TX.fips,
        county_fips="*",
        tract="*",
        year=year,
    )
    df = pd.DataFrame(tx_census)
    sort_query = pd.DataFrame(sort_query)
    sort_query = sort_query[sort_query["county"].isin(REGION)]
    sort_query = sort_query[["NAME"]]
    df = df[df["county"].isin(REGION)]
    df = sort_query.merge(df, on="NAME", how="left")
    return df


def transform(census_data):
    # Renaming columns
    census_data.rename(
        columns={
            "B19013_001E": "median_hh_inc",
            "B25003_001E": "tot_hh",
            "B25003_003E": "tot_renters",
            "B03002_001E": "tot_pop",
            "B03002_003E": "tot_whitenh",
            "B03002_004E": "tot_black",
            "B03002_005E": "tot_aian",
            "B03002_006E": "tot_asian",
            "B03002_007E": "tot_nhpi",
            "B03002_008E": "tot_other",
            "B03002_009E": "tot_multi",
            "B03002_012E": "tot_hisp",
            "B19058_001E": "univ_food_stamps",
            "B19058_002E": "tot_food_stamps",
            "B28001_001E": "univ_devices",
            "B28001_011E": "tot_no_device",
            "B09001_001E": "tot_age_under_18",
            "B15002_001E": "tot_adults",
            "B23025_005E": "tot_unemployed",
            "B18101_001E": "tot_with_disability",
        },
        inplace=True,
    )

    # Replacing missing values in median income with the average for the region
    avg_inc = census_data[census_data["median_hh_inc"] != -666666666]["median_hh_inc"].mean()
    census_data["median_hh_inc"] = census_data["median_hh_inc"].replace(-666666666, avg_inc)

    # Census calculations
    census_data["tot_age_70_to_79"] = (
            census_data["B01001_022E"]
            + census_data["B01001_023E"]
            + census_data["B01001_046E"]
            + census_data["B01001_047E"]
    )
    census_data["tot_age_over_80"] = (
            census_data["B01001_024E"]
            + census_data["B01001_025E"]
            + census_data["B01001_048E"]
            + census_data["B01001_049E"]
    )
    census_data["tot_age_over_70"] = (
            census_data["tot_age_70_to_79"] + census_data["tot_age_over_80"]
    )
    census_data["tot_ba"] = (
            census_data["B15002_015E"]
            + census_data["B15002_016E"]
            + census_data["B15002_017E"]
            + census_data["B15002_018E"]
            + census_data["B15002_032E"]
            + census_data["B15002_033E"]
            + census_data["B15002_034E"]
            + census_data["B15002_035E"]
    )
    census_data["tot_noba"] = census_data["tot_adults"] - census_data["tot_ba"]
    census_data["tot_poc"] = census_data["tot_pop"] - census_data["tot_whitenh"]
    census_data["total_overcrowded_households"] = (
            census_data["B25014_005E"]
            + census_data["B25014_006E"]
            + census_data["B25014_007E"]
            + census_data["B25014_011E"]
            + census_data["B25014_012E"]
            + census_data["B25014_013E"]
    )
    census_data["tot_home_lang"] = (
            census_data["C16002_001E"] - census_data["C16002_002E"]
    )
    census_data["tot_wfh"] = census_data["B08101_001E"] - census_data["B08101_049E"]
    census_data["tot_unenrolled_school"] = (
            census_data["B14001_003E"]
            + census_data["B14001_004E"]
            + census_data["B14001_005E"]
            + census_data["B14001_006E"]
            + census_data["B14001_007E"]
    )
    census_data["tot_wo_broadband"] = (
            census_data["B28002_003E"] + census_data["B28002_013E"]
    )
    census_data["tot_less_vehicle"] = (
            census_data["B08203_014E"]
            + census_data["B08203_020E"]
            + census_data["B08203_021E"]
            + census_data["B08203_026E"]
            + census_data["B08203_027E"]
            + census_data["B08203_028E"]
    )
    census_data["tot_mortgage_over35"] = (
            census_data["B25091_009E"]
            + census_data["B25091_010E"]
            + census_data["B25091_011E"]
    )
    census_data["tot_rent_over35"] = (
            census_data["B25070_008E"]
            + census_data["B25070_009E"]
            + census_data["B25070_010E"]
    )
    census_data["tot_eng_prof"] = (
            census_data["C16002_004E"]
            + census_data["C16002_007E"]
            + census_data["C16002_010E"]
            + census_data["C16002_013E"]
    )

    census_data["pct_over_70"] = census_data["tot_age_over_70"] / census_data["tot_pop"]
    census_data["pct_rent"] = census_data["tot_renters"] / census_data["tot_hh"]
    census_data["pct_ba"] = census_data["tot_ba"] / census_data["tot_adults"]
    census_data["pct_noba"] = census_data["tot_noba"] / census_data["tot_adults"]
    census_data["pct_poc"] = census_data["tot_poc"] / census_data["tot_pop"]
    census_data["pct_underserved_poc"] = (
                                                 census_data["tot_black"]
                                                 + census_data["tot_hisp"]
                                                 + census_data["tot_aian"]
                                                 + census_data["tot_nhpi"]
                                         ) / census_data["tot_pop"]
    census_data["pct_food_stamps"] = (
            census_data["tot_food_stamps"].divide(census_data["univ_food_stamps"])
    ).fillna(0)
    census_data["pct_no_device"] = (
            census_data["tot_no_device"].divide(census_data["univ_devices"])
    ).fillna(0)
    census_data["pctovercrowd"] = (
            census_data["total_overcrowded_households"].divide(census_data["B25014_001E"])
    ).fillna(0)
    census_data["pct_unemployed"] = (
            census_data["tot_unemployed"].divide(census_data["B23025_001E"])
    ).fillna(0)
    census_data["pct_wfh"] = (census_data["tot_wfh"].divide(census_data["B08101_001E"])).fillna(0)
    census_data["pct_unenrolled"] = (
            census_data["tot_unenrolled_school"].divide(census_data["tot_age_under_18"])
    ).fillna(0)
    census_data["pct_wo_broadband"] = (
            census_data["tot_wo_broadband"].divide(census_data["B28002_001E"])
    ).fillna(0)
    census_data["pct_less_vehicles"] = census_data["tot_less_vehicle"].divide((
            census_data["B08203_001E"] - census_data["B08203_007E"])
    ).fillna(0)
    census_data["pct_lang_home"] = (
            census_data["tot_home_lang"].divide(census_data["C16002_001E"])
    ).fillna(0)
    census_data["pct_mortgage_over35"] = (
            census_data["tot_mortgage_over35"].divide(census_data["B25091_001E"])
    ).fillna(0)
    census_data["pct_rent_over35"] = (
            census_data["tot_rent_over35"].divide(census_data["B25070_001E"])
    ).fillna(0)
    census_data["pct_with_disability"] = (
            census_data["tot_with_disability"].divide(census_data["tot_pop"])
    )
    census_data["pct_eng_prof"] = (
            census_data["tot_eng_prof"].divide(census_data["C16002_001E"])
    ).fillna(0)

    return census_data


def create_categories(row):
    if row["indexed_vulnerability"] > 80:
        return "Most Vulnerable"
    if row["indexed_vulnerability"] > 60:
        return "Medium-High Vulnerable"
    if row["indexed_vulnerability"] > 40:
        return "Medium Vulnerable"
    if row["indexed_vulnerability"] > 20:
        return "Medium-Low Vulnerable"
    return "Least Vulnerable"


def apply_weights(census_data):
    # Applying the weights as defined in config.py

    census_data["composite_vulnerability"] = 0
    for item in WEIGHTS:
        if "negative weight" in item:
            census_data[item["column"]] = census_data[item["column"]] * -1
        census_data[item["name"]] = (
                ntile(census_data, item["column"], n=100) * item["weight"]
        )
        census_data["composite_vulnerability"] = (
                census_data["composite_vulnerability"] + census_data[item["name"]]
        )

    # min-max normalization
    census_data["indexed_vulnerability"] = (
                                                   census_data["composite_vulnerability"]
                                                   - census_data["composite_vulnerability"].min()
                                           ) / (
                                                   census_data["composite_vulnerability"].max()
                                                   - census_data["composite_vulnerability"].min()
                                           )
    census_data["indexed_vulnerability"] = census_data["indexed_vulnerability"] * 100
    census_data["eaz_type"] = census_data.apply(create_categories, axis=1)
    return census_data


def ntile(df, column, n):
    """
    Implementing R's version of ntile in pandas
    src: https://github.com/tidyverse/dplyr/blob/HEAD/R/rank.R

    :param df: dataframe to apply ntile to
    :param column: name of the column to ntile
    :param n: number of bins
    :return:
    """
    x = df[column].rank(method="first")
    length = len(df[column]) - sum(df[column].isna())
    n_larger = int(length % n)
    size = length / n
    larger_size = int(math.ceil(size))
    smaller_size = int(math.floor(size))
    larger_threshold = larger_size * n_larger
    output = np.where(
        x <= larger_threshold,
        (x + (larger_size - 1)) / larger_size,
        (x + (-larger_threshold + smaller_size - 1)) / smaller_size + n_larger,
    )
    return np.floor(output)


def get_geometry(df, year):
    # Gets the TIGER geometry for the census tracts
    geom = tracts(state="TX", year=year, cache=True)
    geom = geom[["GEOID", "geometry"]]
    df = df[["GEO_ID", "NAME", "indexed_vulnerability", "eaz_type"]]
    df["GEOID"] = df["GEO_ID"].str[9:20]
    gdf = geom.merge(df, on="GEOID", how="right")
    gdf.drop(columns=["GEO_ID"], inplace=True)

    return gdf


def plot_image(gdf, year):
    # Plots an image of the geometry
    ax = gdf.plot(column="indexed_vulnerability", cmap="viridis", legend=True)
    ax.set_axis_off()
    ax.set_title(f"Austin Vulnerability Score,{year} ACS")
    plt.savefig(f"images/{year}.png", dpi=300)


def main(args):
    year = args.year

    logger.info(f"Year selected: {year}")
    logger.info("Downloading Census data")
    df = load(year)

    logger.info("Transforming Census data")
    df = transform(df)
    df = apply_weights(df)

    logger.info("Downloading Census tract geometry")
    gdf = get_geometry(df, year)

    logger.info("Exporting data and graphics")
    plot_image(gdf, year)
    gdf.to_file(f"gis/equity_analysis_zones_{year}.geojson")
    logger.info("Processed completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        default=2019,
        help="int: Year of the ACS to use for the analysis.",
    )

    args = parser.parse_args()
    logger = logging.getLogger(__file__)

    main(args)
