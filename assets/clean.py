import pandas as pd
import numpy as np

# NOT IN USAGE
def drop_columns(df):
    drop_columns = ['State', 'Federation', 'ParentFederation', 'Date', 'MeetCountry', 'MeetState', 'MeetTown', 'MeetName']
    df = df.drop(drop_columns, axis = 1)
    pass

def replace_lift_null_data(df):
    """Gives zero for null value for each lift, irrespective of event"""
    lifts = ["Squat", "Bench", "Deadlift"]
    lift_number = [1, 2, 3, 4]
    for lift in lifts:
        for attempt in lift_number:
            column_name = f"{lift}{attempt}Kg"
            df[column_name] = df[column_name].fillna(0)
    pass

def checks_best_lift(df):
    """Calculates best lift out of the three attempts per lift, gives zero if failing all three lifts"""
    for lift in ["Squat", "Bench", "Deadlift"]:
        column_name = f"Best3{lift}Kg"
        df[column_name] = df[[f"{lift}1Kg", f"{lift}2Kg", f"{lift}3Kg"]].max(axis = 1)
        df.loc[df[column_name] <= 0, column_name] = 0
    pass

def calculate_total(df):
    df["TotalKg"] = df[["Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg"]].sum(axis = 1)
    pass

def check_qualification(df):
    df["Qualified"] = df.apply(lambda row: str.isdigit(row["Place"]), axis = 1)
    pass

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

def drop_null_weights(df):
    """Drop rows where no weight class nor bodyweight exists"""
    return df.loc[(df["BodyweightKg"].notnull()) & (df["WeightClassKg"].notnull())]

# Not working, just going to drop it for now
def empty_weight_classes(df):
    df.loc[df["WeightClassKg"] == "+"]["WeightClassKg"] = df.loc[df["WeightClassKg"] == "+"]["BodyweightKg"]
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

def assume_untested(df):
    df.loc[df["Tested"].isna(), "Tested"] = False
    pass

def fill_unknown_values(df, column_name:str, value_to_fill):
    df[column_name].fillna(value_to_fill, inplace = True)
    pass

def assume_federation(df):
    df["ParentFederation"] = np.where(df["ParentFederation"].isna(), df["Federation"], df["ParentFederation"])
    pass

def fill_lift_scores(df):
    criteria = ["Dots", "Wilks", "Glossbrenner", "Goodlift"]
    df[criteria] = df[criteria].fillna(value = 0)
    pass