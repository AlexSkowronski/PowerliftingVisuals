import pandas as pd

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