import pandas as pd
import numpy as np

##############################################################################

"""Start: Lift related clean up"""
def replace_lift_null_data(df):
    """Gives zero for null value for each lift, irrespective of event, removes null values"""
    lifts = ["Squat", "Bench", "Deadlift"]
    lift_number = [1, 2, 3, 4]
    for lift in lifts:
        for attempt in lift_number:
            column_name = f"{lift}{attempt}Kg"
            df[column_name] = df[column_name].fillna(0)
    pass

def checks_best_lift(df):
    """For respective lift, returns max value out of attempts one, two and three. If failing each of the three (negative values for each), gives zero for total of the lift"""
    for lift in ["Squat", "Bench", "Deadlift"]:
        column_name = f"Best3{lift}Kg"
        df[column_name] = df[[f"{lift}1Kg", f"{lift}2Kg", f"{lift}3Kg"]].max(axis = 1)
        df.loc[df[column_name] <= 0, column_name] = 0
    pass

def calculate_total(df):
    """Calculates total of all three lifts, irrespective of event, even if all lifts fail"""
    df["TotalKg"] = df[["Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]].sum(axis = 1)
    pass

def validate_comp(df):
    """Checks place of lifter and returns True if valid record, returns False if disqualified, didn't show up, got zero on all lifts etc."""
    """Dropped one row where place is 195th when goes up to 120th"""
    df = df[~(df["Place"] == "195")]
    df["ValidComp"] = df.apply(lambda row: True if (str.isdigit(row["Place"]) and row["TotalKg"] != 0) else False, axis=1)
    #Old rule, not bad, may also use
    #df["Qualified"] = df.apply(lambda row: str.isdigit(row["Place"]), axis = 1)
    return df
"""End: Lift related clean up"""

##############################################################################

def rearrange_column(df, column_before):
    columns = list(df.columns)
    index_to_place = df.columns.get_loc(column_before)
    columns = columns[:index_to_place+1] + [columns[-1]] + columns[index_to_place+1:len(columns)-1]
    return df[columns]

# Future implementation, too difficult to compute right now, NOT FINISHED
def check_event_with_lifts(df):
    """Want to check whether data for lifts correlates with the correct event i.e. do non-bench events have a bench press lift?"""
    """Go throw every row, access the Event value, check corresponding columns to see if zero"""
    event_list = list(df["Event"].unique())
    event_list.remove("SBD")
    events_to_check = {}
    for events in event_list:
        events_to_check[events] = []
        if 'B' not in events:
            events_to_check[events].append("Best3BenchKg")
        if 'S' not in events:
            events_to_check[events].append("Best3SquatKg")
        if 'D' not in events:
            events_to_check[events].append("Best3DeadliftKg")

##############################################################################

"""Start: Weight related data clean up"""
def drop_null_weights(df):
    """Drop rows where no weight class nor bodyweight exists"""
    # Not sure how to deduce information, perhaps from Division, Sex?
    return df[~((df["BodyweightKg"].isna()) & ((df["WeightClassKg"].isna()) | (df["WeightClassKg"] == "+")))]

def fix_plus_weightclass(df):
    """For weight classes that just have a '+' sign or null value, replace it with the entry for the weight class and the plus sign, sorted next function"""
    df["WeightClassKg"] = df["WeightClassKg"].fillna(df["BodyweightKg"].astype("string"))
    df["WeightClassKg"] = df.apply(lambda row: str(row["BodyweightKg"]) if (row["WeightClassKg"] == "+") else str(row["WeightClassKg"]), axis=1)
    pass

def redefine_weight_classes(df):
    """Create new weight class under IPF rules based off of existing weight class"""
    M_bins = [0, 53, 59, 66, 74, 83, 93, 105, 120, 999]
    F_bins = [0, 43, 47, 52, 57, 63, 69, 76, 84, 999]

    M_labels = ["-53", "53-59", "59-66", "66-74", "74-83", "83-93", "93-105", "105-120", "120+"]
    F_labels = ["-43", "43-47", "47-52", "52-57", "57-63", "63-69", "69-76", "76-84", "84+"]

    """Remove + from weight classes and convert to numeric datatype"""
    df["IPFWeightClassKg"] = df["WeightClassKg"].apply(lambda row: row.replace("+", ""))
    df["IPFWeightClassKg"] = pd.to_numeric(df["IPFWeightClassKg"])

    """Check each value of the row and put in the correct bin"""
    df_female = df.loc[df["Sex"] == "F"]
    df_male = df.loc[(df["Sex"] == "M") | (df["Sex"] == "Mx")]
    df_female["IPFWeightClassKg"] = pd.cut(df_female["IPFWeightClassKg"], bins = F_bins, labels = F_labels)
    df_male['IPFWeightClassKg'] = pd.cut(df_male['IPFWeightClassKg'], bins = M_bins, labels = M_labels)

    return pd.concat([df_female, df_male])
"""End: Weight related data clean up"""

##############################################################################

"""Start: Federation and Metric cleaning"""
def assume_untested(df):
    """Null values take value False and if already Yes returns True"""
    df["Tested"] = df["Tested"].apply(lambda row: True if row == "Yes" else False)
    pass

def fill_unknown_values(df):
    """Fills columns with 'N/A'"""
    # Future implementation, use NLP, fuzzywuzzy to read meet town and match with state
    unknown_dict = {
        "MeetTown": "N/A",
        "MeetState": "N/A",
        "Country": "N/A",
        "State": "N/A",
        "Division": "Open",
    }
    df.fillna(value=unknown_dict, inplace=True)
    pass

def assume_federation(df):
    """Takes lifters with no parent federation and assumes their federation is the parent federation"""
    df["ParentFederation"] = np.where(df["ParentFederation"].isna(), df["Federation"], df["ParentFederation"])
    pass

def fill_lift_scores(df):
    """Takes all metrics and all ones that are null are given zero"""
    # Future implementation: create own calculators of each from research and apply them, based on event, gender, bodyweight, total
    criteria = ["Dots", "Wilks", "Glossbrenner", "Goodlift"]
    df[criteria] = df[criteria].fillna(value = 0)
    pass
"""End: Federation and Metric cleaning"""

##############################################################################

"""Start: Age related data clean up"""
def rename_entries(df):
    df["AgeClass"] = df["AgeClass"].apply(lambda row: "80+" if row == "80-999" else row)
    df["BirthYearClass"] = df["BirthYearClass"].apply(lambda row: "70+" if row == "70-999" else row)
    return df

def discard_empty_ages(df):
    df = df.loc[~((df["Age"].isna()) & (df["AgeClass"].isna()) & (df["BirthYearClass"].isna()))]
    df = df[~((df["Age"].notna()) & (df["AgeClass"].isna()))]
    return df

def lazy_drop(df):
    return df.dropna()

def redefine_age_classes(df):
    class_conversion = {
        "5-12": "-18", "13-15": "-18", "16-17": "-18",
        "18-19": "19-23", "20-23": "19-23",
        "24-34": "24-39", "35-39": "24-39",
        "40-44": "40-49", "45-49": "40-49",
        "50-54": "50-59", "55-59": "50-59",
        "60-64": "60-69", "65-69": "60-69",
        "70-74": "70+", "75-79": "70+", "80+": "70+"
    }
    df["IPFAgeClass"] = df["AgeClass"].apply(lambda row: class_conversion[row] if type(row) == str else "Unavailable")
    pass
