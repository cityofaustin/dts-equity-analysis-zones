# Austin Equity Analysis Zones

This repository stores the script meant to maintain the Austin Equity Analysis Zones (EAZs). The EAZs were originally created by work led by the City of Austin's Transportation Department [Systems Development Division](https://www.austintexas.gov/department/transportation-systems-development) and [Open Austin](https://www.open-austin.org/). 

The original work was completed using the 2019 [American Community Survey](https://www.census.gov/programs-surveys/acs) (ACS), a yearly product from the US Census Bureau.
The purpose of this repo is to allow the EAZs to be refreshed on a yearly basis with the most recent ACS.

## Background 

Within the Austin Strategic Mobility Plan (ASMP), adopted by City Council in 2019, Action Item 200 - Equity Analysis Zones calls for staff to:

> Identify a framework to designate geographic zones that will be used in analyzing the equity of programming, project implementation, and engagement efforts related to transportation. The criteria should consider race, income, car-ownership, educational attainment, housing tenure, transit availability, language spoken at home, age, disability status, and other factors to help focus efforts on historically underrepresented and underserved communities.

A community advisory team was formed during 2020 to determine how to best weigh data from the ACS.
These weights were used to calculate a socioeconomic vulnerability index for each census tract in the region. 

The weights determined by the advisory team were as follows:
- Percent People of color - 5
- Percent people who identify as Black, Indigenous, Latinx - 5
- Median Household Income - 4
- Percent of people on Food Stamps/SNAP - 2
- Percent of people whose rent is above 35% of monthly income - 2
- Percent of people without broadband internet - 2
- Percent of households with less than one vehicle per working occupant - 1
- Percent of people with a disability - 4
- Percent of people aged 65 and over - 1

## Vulnerability Weighting Map Tool

The advisory team used the [Vulnerability Weighting Map](https://github.com/cityofaustin/vulnerability_weighting_map) to visualize ACS data alongside different weights.

## Getting started

You'll need a python 3.9 environment, then clone this repo and install the dependencies:

`pip install --upgrade pip`

`pip install -r requirements.txt`

Get a census API key [here](https://api.census.gov/data/key_signup.html) and provide it as an environment variable `CENSUS_API_KEY`.

## Running

Running the main script without a `year` parameter will use a default year of 2019 for the analysis.

`python main.py` -> `Year selected: 2019`

`python main.py --year 2021` -> `Year selected: 2021`

## Outputs

In the `gis` directory, geojson files are created for the years ran with the following output columns
- `GEOID`: the unique TIGER line geometry ID for the census tract
- `NAME`: the name of the census tract
- `indexed_vulnerability`: the value of socioeconomic vulnerability index for the census tract
- `eaz_type`: the vulnerability category this tract falls into based on the index

A map is generated of the vulnerability index for the region in the `images` directory. 

## Equity Analysis Yearly Comparison Tool

The `/maps` directory of this repo stores the code used to develop (and deploy) the yearly comparison tool. This tool allows
comparisons of variables between different years of the ACS. It is hosted at [equitytool.austinmobility.io](https://equitytool.austinmobility.io/).

![eaz tool example image](docs/imgs/eaz_tool.png)

## Analysis

The `/analysis` directory stores some one-off jupyter notebooks used for analysis and data wrangling. 
