# Names of columns to be visualized
variables = [
    "indexed_vulnerability",
    "pct_poc",
    "pct_underserved_poc",
    "median_hh_inc",
    "pct_with_disability",
    "pct_food_stamps",
    "pct_rent_over35",
    "pct_wo_broadband",
    "pct_less_vehicles",
    "pct_over_70",
]

# Labels for dropdown options
variable_labels = {
    "indexed_vulnerability": "Vulnerability index",
    "pct_poc": "People of Color",
    "pct_underserved_poc": "Black, indigenous, latinx people",
    "median_hh_inc": "Median household income",
    "pct_with_disability": "Persons with disabilities",
    "pct_food_stamps": "Food stamp recipients",
    "pct_rent_over35": "Cost-burdened renters (35%+)",
    "pct_wo_broadband": "No broadband access",
    "pct_less_vehicles": "Households without a vehicle",
    "pct_over_70": "People over age 70",
}

dimension_labels = {"absolute": "Absolute", "relative": "Difference since 2019"}

# Ordering for bar plot
order = [
    "Least Vulnerable",
    "Medium-Low Vulnerable",
    "Medium Vulnerable",
    "Medium-High Vulnerable",
    "Most Vulnerable",
]
