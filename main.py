from assets.extract import extract_dataset
import pandas as pd
from assets.clean import *

ADDRESS = "https://openpowerlifting.gitlab.io/opl-csv/files/openpowerlifting-latest.zip"

def clean_lift_data(df):
    """Fill in null data for non-completed lifts for all attempts of all lifts"""
    replace_lift_null_data(df)
    """Properly returns best lift for each respective lift"""
    checks_best_lift(df)
    """Calculates total for all three lifts"""
    calculate_total(df)
    """Returns boolean for new column: 'ValidComp' if non-zero total and qualified i.e. no disqualifications, not showing up, failing all lifts, etc."""
    df = validate_comp(df)
    pass

def clean_weight_data(df):
    """Removes rows where no WeightClass nor Bodyweight are available"""
    df = drop_null_weights(df)
    """Fixes all entries where WeightClass was simply a '+', takes bodyweight and uses that as the weight class"""
    fix_plus_weightclass(df)
    """Created IPF Weight Class, takes WeightClass entry and removes any plus signs, assigns them into bins according to IPF weight classes"""
    df = redefine_weight_classes(df)
    pass

def clean_metric_federation_data(df):
    """If null values False, if Yes gives True"""
    assume_untested(df)

    """Fill columns with no entry with placeholder"""
    fill_unknown_values(df)

    """For lifters with no parent federation, assume federation they belong to is the parent federation"""
    assume_federation(df)

    """All metrics with null values, taken to be zero"""
    fill_lift_scores(df)
    pass

def main():
    """Load into dataframe from extracted csv dataset"""
    df = pd.read_csv(extract_dataset(ADDRESS))

    """Cleaning lift related data"""
    clean_lift_data(df)

    """Cleaning weight related data"""
    clean_weight_data(df)

    """Cleaning metric and federation data"""
    clean_metric_federation_data(df)
    df.to_csv("./data.csv", index = False)
    """Cleaning age data"""

if __name__ == "__main__":
    main()