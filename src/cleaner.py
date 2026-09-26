#=========================================================================#
#  FILE   : src/cleaner.py                                                 #
#  PURPOSE: Tidies up the data we collected before we use it.              #
#  OWNER  : 25ada073                                                       #
#                                                                          #
#  Data taken from a website is never ready to analyse straight away.      #
#  The problems we found in the CSE data were:                             #
#                                                                          #
#    1. Dates arrive as very large numbers, such as 1786440420412, which   #
#       is the number of milliseconds since 1970. Left alone, pandas       #
#       treats them as ordinary numbers.                                   #
#                                                                          #
#    2. Some numbers arrive as text. You cannot add up text, and sorting   #
#       it puts "9" after "100" because it sorts alphabetically.           #
#                                                                          #
#    3. Some columns are empty for every single company.                   #
#                                                                          #
#    4. Company names have extra spaces around them, so grouping by name   #
#       creates two groups that look identical.                            #
#=========================================================================#

import pandas as pd


#-------------------------------------------------------------------------#
#  DESCRIBING THE DATA                                                     #
#-------------------------------------------------------------------------#

def describe(df):
    """
    Count the problems in a DataFrame.

    We run this before and after cleaning so we can show what changed.
    """
    if df is None or df.empty:
        return {"Rows": 0, "Columns": 0, "Empty cells": 0,
                "Empty columns": 0, "Duplicate rows": 0,
                "Number columns": 0, "Date columns": 0}

    return {
        "Rows": len(df),
        "Columns": len(df.columns),
        "Empty cells": int(df.isna().sum().sum()),
        "Empty columns": int(df.isna().all().sum()),
        "Duplicate rows": int(df.duplicated().sum()),
        "Number columns": int(df.select_dtypes(include="number").shape[1]),
        "Date columns": int(df.select_dtypes(include="datetime").shape[1]),
    }


def compare(before, after):
    """Put the before and after counts side by side."""
    rows = []
    for item in before:
        rows.append({
            "Check": item,
            "Before": before[item],
            "After": after.get(item, 0),
        })
    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  CLEANING                                                                #
#-------------------------------------------------------------------------#

def clean(df):
    """
    Clean a DataFrame and list what was changed.
    Returns (the cleaned DataFrame, a list of what we did).

    We copy the DataFrame first, so the original stays untouched in case
    we need to check something against it later.
    """
    if df is None or df.empty:
        return df, ["There was no data to clean."]

    tidy = df.copy()
    changes = []

    #--- 1. Turn the big numbers back into dates ------------------------#
    date_columns = []
    for column in tidy.columns:
        # Only look at columns whose name suggests a date, so we never
        # accidentally convert a price or a quantity.
        if not any(word in column.lower()
                   for word in ("date", "time", "created")):
            continue
        if not pd.api.types.is_numeric_dtype(tidy[column]):
            continue

        values = tidy[column].dropna()
        # Milliseconds since 1970 is a huge number for any recent date.
        # This check stops us changing a column that only happens to have
        # the word date in its name.
        if not values.empty and values.median() > 1_000_000_000_000:
            # The milliseconds are counted in UTC, the world's standard
            # time. Sri Lanka is 5 hours 30 minutes ahead of UTC, so we
            # convert to Colombo time - otherwise every trade looks as if
            # it happened before the market opened at 9.30 in the morning.
            # tz_localize(None) then drops the time zone label, because
            # Excel cannot save a date that has one.
            tidy[column] = (pd.to_datetime(tidy[column], unit="ms",
                                           utc=True, errors="coerce")
                            .dt.tz_convert("Asia/Colombo")
                            .dt.tz_localize(None))
            date_columns.append(column)

    if date_columns:
        changes.append(f"Turned {len(date_columns)} column(s) of large "
                       f"numbers back into dates: {', '.join(date_columns)}")

    #--- 2. Turn text that is really numbers into numbers ---------------#
    number_columns = []
    # Text columns. Newer pandas keeps text in its own "str" type, while
    # older pandas used "object", so we ask for both.
    for column in tidy.select_dtypes(include=["object", "str"]).columns:
        sample = tidy[column].dropna().astype(str).head(50)
        if sample.empty:
            continue

        # If almost everything in the column converts to a number, then
        # it was a number column stored as text.
        converted = pd.to_numeric(sample.str.replace(",", "", regex=False),
                                  errors="coerce")
        if converted.notna().mean() > 0.9:
            tidy[column] = pd.to_numeric(
                tidy[column].astype(str).str.replace(",", "", regex=False),
                errors="coerce")
            number_columns.append(column)

    if number_columns:
        changes.append(f"Changed {len(number_columns)} text column(s) into "
                       f"numbers so they can be sorted and totalled")

    #--- 3. Remove extra spaces from text -------------------------------#
    # Only trim values that really are text. A missing value must stay
    # missing - turning it into the text "nan" would hide a gap in the
    # data and make the table look more complete than it is.
    for column in tidy.select_dtypes(include=["object", "str"]).columns:
        tidy[column] = tidy[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value)
    changes.append("Removed extra spaces from the text columns")

    #--- 4. Drop columns that are empty for every row -------------------#
    empty = [c for c in tidy.columns if tidy[c].isna().all()]
    if empty:
        tidy = tidy.drop(columns=empty)
        changes.append(f"Removed {len(empty)} column(s) that were empty "
                       f"for every company")

    #--- 5. Remove repeated rows ----------------------------------------#
    before_rows = len(tidy)
    tidy = tidy.drop_duplicates().reset_index(drop=True)
    if before_rows != len(tidy):
        changes.append(f"Removed {before_rows - len(tidy)} repeated row(s)")

    #--- 6. Put the useful columns first --------------------------------#
    useful = ["symbol", "name", "price", "change", "percentageChange",
              "quantity", "turnover"]
    front = [c for c in useful if c in tidy.columns]
    if front:
        tidy = tidy[front + [c for c in tidy.columns if c not in front]]
        changes.append("Moved the most useful columns to the front")

    return tidy, changes


#-------------------------------------------------------------------------#
#  CHECKING THE VALUES MAKE SENSE                                          #
#                                                                          #
#  Cleaning fixes the shape of the data. These checks ask whether the      #
#  values are believable - a share price of -5 rupees would be perfectly   #
#  tidy and still completely wrong.                                        #
#-------------------------------------------------------------------------#

def check(df):
    """Run some simple checks and return the results as a table."""
    results = []

    if df is None or df.empty:
        return pd.DataFrame([{"Check": "Is there any data?",
                              "Result": "No", "Detail": "The table is empty"}])

    def add(name, passed, detail):
        results.append({"Check": name,
                        "Result": "OK" if passed else "Check this",
                        "Detail": detail})

    add("Rows collected", len(df) > 0, f"{len(df)} rows")

    if "price" in df.columns:
        negative = int((df["price"] < 0).sum())
        add("No negative prices", negative == 0,
            "All prices are zero or above" if negative == 0
            else f"{negative} negative price(s)")

    if "percentageChange" in df.columns:
        extreme = int((df["percentageChange"].abs() > 100).sum())
        add("Price changes look sensible", extreme == 0,
            "Nothing moved more than 100%" if extreme == 0
            else f"{extreme} company(s) moved more than 100%")

    if "symbol" in df.columns:
        missing = int(df["symbol"].isna().sum())
        add("Every row has a symbol", missing == 0,
            "All rows have one" if missing == 0
            else f"{missing} row(s) missing a symbol")

        repeated = int(df["symbol"].duplicated().sum())
        add("No company appears twice", repeated == 0,
            "Each company appears once" if repeated == 0
            else f"{repeated} repeated symbol(s)")

    total_cells = df.shape[0] * df.shape[1]
    if total_cells:
        filled = (1 - df.isna().sum().sum() / total_cells) * 100
        add("How complete is the data", filled > 70,
            f"{filled:.1f}% of cells have a value")

    return pd.DataFrame(results)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.cleaner                        #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    from src.api_client import CSEApi

    api = CSEApi()
    raw = api.trade_summary()

    if raw.empty:
        print("No data - check your internet connection.")
    else:
        before = describe(raw)
        tidy, changes = clean(raw)
        after = describe(tidy)

        print("What we changed")
        print("-" * 55)
        for change in changes:
            print("  -", change)

        print()
        print("Before and after")
        print("-" * 55)
        print(compare(before, after).to_string(index=False))

        print()
        print("Checks")
        print("-" * 55)
        print(check(tidy).to_string(index=False))
