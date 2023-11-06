# Counties selected in region
REGION = [
    "021",  # Bastrop
    "055",  # Caldwell
    "209",  # Hays
    "453",  # Travis
    "491",  # Williamson
]

# Fields pulled from Census, more info available at:
# https://api.census.gov/data/{year}/acs/acs5/groups/{table ID}.json
FIELDS = [
    "NAME",
    # Table B01001 SEX BY AGE
    "B01001_001E",  # Total survey count
    "B01001_022E",  # Male age 70-74
    "B01001_023E",  # Male age 75-79
    "B01001_046E",  # Female age 70-74
    "B01001_047E",  # Female age 75-79
    "B01001_024E",  # Male age 80-84
    "B01001_025E",  # Male age >85
    "B01001_048E",  # Female age 80-84
    "B01001_049E",  # Female age >85
    # Table B15002 SEX BY EDUCATIONAL ATTAINMENT FOR THE POPULATION 25 YEARS AND OVER
    "B15002_001E",  # Total survey count
    "B15002_015E",  # Male Bachelor's Degree
    "B15002_016E",  # Male Master's Degree
    "B15002_017E",  # Male Professional School Degree
    "B15002_018E",  # Male Doctorate Degree
    "B15002_032E",  # Female Bachelor's Degree
    "B15002_033E",  # Female Master's Degree
    "B15002_034E",  # Female Professional School Degree
    "B15002_035E",  # Female Doctorate Degree
    # Table B25014 TENURE BY OCCUPANTS PER ROOM
    "B25014_001E",  # Total survey count
    "B25014_005E",  # Owner occupied: 1.01 to 1.50 occupants per room
    "B25014_006E",  # Owner occupied: 1.51 to 2.00 occupants per room
    "B25014_007E",  # Owner occupied: 2.01 or more occupants per room
    "B25014_011E",  # Renter occupied: 1.01 to 1.50 occupants per room
    "B25014_012E",  # Renter occupied: 1.51 to 2.00 occupants per room
    "B25014_013E",  # Renter occupied: 2.01 or more occupants per room
    # Table C16002 HOUSEHOLD LANGUAGE BY HOUSEHOLD LIMITED ENGLISH SPEAKING STATUS
    "C16002_001E",  # Total survey count
    "C16002_002E",  # English Only
    "C16002_004E",  # Limited English-speaking household: Spanish
    "C16002_007E",  # Limited English-speaking household: Other Indo-European languages
    "C16002_010E",  # Limited English-speaking household: Asian and Pacific Island languages
    "C16002_013E",  # Limited English-speaking household: Other languages
    # Table B23025 EMPLOYMENT STATUS FOR THE POPULATION 16 YEARS AND OVER
    "B23025_001E",  # Total survey count
    "B23025_005E",  # Unemployed
    # Table B08101 MEANS OF TRANSPORTATION TO WORK BY AGE
    "B08101_001E",  # Total survey count
    "B08101_049E",  # Worked from home
    # Table B14001 SCHOOL ENROLLMENT BY LEVEL OF SCHOOL FOR THE POPULATION 3 YEARS AND OVER
    "B14001_001E",  # Total survey count
    "B14001_003E",  # Enrolled in nursery school, preschool
    "B14001_004E",  # Enrolled in kindergarten
    "B14001_005E",  # Enrolled in grade 1 to grade 4
    "B14001_006E",  # Enrolled in grade 5 to grade 8
    "B14001_007E",  # Enrolled in grade 9 to grade 12
    # Table B28002 PRESENCE AND TYPES OF INTERNET SUBSCRIPTIONS IN HOUSEHOLD
    "B28002_001E",  # Total survey count
    "B28002_003E",  # Dial-up with no other type of Internet subscription
    "B28002_013E",  # No Internet access
    # Table B08203 NUMBER OF WORKERS IN HOUSEHOLD BY VEHICLES AVAILABLE
    "B08203_001E",  # Total survey count
    "B08203_014E",  # 1 worker: No vehicle available
    "B08203_020E",  # 2 workers: No vehicle available
    "B08203_021E",  # 2 workers: 1 vehicle available
    "B08203_026E",  # 3 or more workers: No vehicle available
    "B08203_027E",  # 3 or more workers: 1 vehicle available
    "B08203_028E",  # 3 or more workers: 2 vehicles available
    "B08203_007E",  # No Workers
    # Table B25091 MORTGAGE STATUS BY SELECTED MONTHLY OWNER COSTS AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    "B25091_001E",  # Total survey count
    "B25091_009E",  # 35.0 to 39.9 percent
    "B25091_010E",  # 40.0 to 49.9 percent
    "B25091_011E",  # 50.0 percent or more
    # Table B25070 GROSS RENT AS A PERCENTAGE OF HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    "B25070_001E",  # Total survey count
    "B25070_008E",  # 35.0 to 39.9 percent
    "B25070_009E",  # 40.0 to 49.9 percent
    "B25070_010E",  # 50.0 percent or more
    # Table B18101 SEX BY AGE BY DISABILITY STATUS
    "B18101_001E",  # Total survey count
    # Table B03002 HISPANIC OR LATINO ORIGIN BY RACE
    "B03002_001E",  # Total Population
    "B03002_003E",  # Not Hispanic or Latino: White alone
    "B03002_004E",  # Not Hispanic or Latino: Black or African American alone
    "B03002_005E",  # Not Hispanic or Latino: American Indian and Alaska Native alone
    "B03002_006E",  # Not Hispanic or Latino: Asian alone
    "B03002_007E",  # Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander alone
    "B03002_008E",  # Not Hispanic or Latino: Some other race alone
    "B03002_009E",  # Not Hispanic or Latino: Two or more races
    "B03002_012E",  # Total Hispanic or Latino
    # Table B19058 PUBLIC ASSISTANCE INCOME OR FOOD STAMPS/SNAP IN THE PAST 12 MONTHS FOR HOUSEHOLDS
    "B19058_001E",  # Total survey count
    "B19058_002E",  # With cash public assistance or Food Stamps/SNAP
    # Table B28001 TYPES OF COMPUTERS IN HOUSEHOLD
    "B28001_001E",  # Total survey count
    "B28001_011E",  # No computer
    # Other tables
    "B19013_001E",  # Median household income in the past 12 months
    "B25003_001E",  # Total occupied housing units
    "B25003_003E",  # Renter occupied housing units
    "B09001_001E",  # Population under age 18
]

WEIGHTS = [
    {
        "name": "Percent People of color",
        "weight": 5,
        "column": "pct_poc",
    },
    {
        "name": "Percent people who identify as Black, Indigenous, Latinx",
        "weight": 5,
        "column": "pct_underserved_poc",
    },
    {
        "name": "Median Household Income",
        "weight": 4,
        "column": "median_hh_inc",
        "negative weight": True,  # We want to weight lower median incomes higher
    },
    {
        "name": "Percent of people on Food Stamps/SNAP",
        "weight": 2,
        "column": "pct_food_stamps",
    },
    {
        "name": "Percent of people whose rent is above 35% of monthly income",
        "weight": 2,
        "column": "pct_rent_over35",
    },
    {
        "name": "Percent of people without broadband internet",
        "weight": 2,
        "column": "pct_wo_broadband",
    },
    {
        "name": "Percent of households with less than one vehicle per working occupant",
        "weight": 1,
        "column": "pct_less_vehicles",
    },
    {
        "name": "Percent of people with a disability",
        "weight": 4,
        "column": "pct_with_disability",
    },
    {
        "name": "Percent of people aged 65 and over",
        "weight": 1,
        "column": "pct_over_70",
    },
]
