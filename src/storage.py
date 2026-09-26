#=========================================================================#
#  FILE   : src/storage.py                                                 #
#  PURPOSE: Saves the data we collected as CSV, Excel and JSON files.      #
#  OWNER  : 25ada141                                                       #
#                                                                          #
#  Every file we save credits the Colombo Stock Exchange as the source     #
#  and records when the data was collected. A spreadsheet passed on to     #
#  somebody else with no source attached is how data gets misused, so the  #
#  credit travels inside the file itself.                                  #
#                                                                          #
#  Each file type needs a different way of carrying that credit:           #
#     CSV    a few comment lines at the top, starting with #               #
#     Excel  a second sheet named Source                                   #
#     JSON   a details section above the records                           #
#=========================================================================#

import json
from datetime import datetime

import pandas as pd

import config


#-------------------------------------------------------------------------#
#  SAVING A DATAFRAME                                                      #
#-------------------------------------------------------------------------#

def export(df, name, formats=("csv", "excel", "json")):
    """
    Save one DataFrame in the formats asked for.
    Returns the list of files created.
    """
    if df is None or df.empty:
        return []

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    collected = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    created = []

    #--- CSV ------------------------------------------------------------#
    if "csv" in formats:
        path = config.EXPORT_DIR / f"{name}_{stamp}.csv"

        # The lines beginning with # are comments. Excel shows them, and
        # pandas can skip them when reading the file back:
        #     pd.read_csv(path, comment="#")
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            f.write(f"# {config.ATTRIBUTION}\n")
            f.write(f"# Collected on: {collected}\n")
            f.write(f"# Rows: {len(df)}   Columns: {len(df.columns)}\n")
            df.to_csv(f, index=False)

        created.append(path)

    #--- Excel ----------------------------------------------------------#
    if "excel" in formats:
        path = config.EXPORT_DIR / f"{name}_{stamp}.xlsx"
        try:
            source = pd.DataFrame({
                "Item": ["Source", "Website", "Collected on", "Rows",
                         "Collected by", "Course"],
                "Value": ["Colombo Stock Exchange", config.BASE_URL,
                          collected, len(df), " / ".join(config.member_label(m) for m in config.TEAM),
                          config.COURSE],
            })

            with pd.ExcelWriter(path, engine="openpyxl") as writer:
                df.to_excel(writer, sheet_name="Data", index=False)
                source.to_excel(writer, sheet_name="Source", index=False)

            created.append(path)
        except Exception:
            pass

    #--- JSON -----------------------------------------------------------#
    if "json" in formats:
        path = config.EXPORT_DIR / f"{name}_{stamp}.json"

        contents = {
            "details": {
                "source": config.ATTRIBUTION,
                "collected_on": collected,
                "rows": len(df),
                "collected_by": [config.member_label(m) for m in config.TEAM],
            },
            "records": json.loads(df.to_json(orient="records",
                                             date_format="iso")),
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(contents, f, indent=2)

        created.append(path)

    return created


#-------------------------------------------------------------------------#
#  SAVING A PDF                                                            #
#-------------------------------------------------------------------------#

def save_pdf(content, filename):
    """Write a downloaded PDF into data/pdfs/."""
    # Remove any characters Windows will not accept in a filename.
    safe = "".join(c for c in filename if c.isalnum() or c in " ._-").strip()
    safe = safe[:110] or "document"
    if not safe.lower().endswith(".pdf"):
        safe += ".pdf"

    path = config.PDF_DIR / safe
    with open(path, "wb") as f:
        f.write(content)
    return path


#-------------------------------------------------------------------------#
#  LISTING WHAT WE HAVE SAVED                                              #
#-------------------------------------------------------------------------#

def list_exports():
    """All the files we have exported, newest first."""
    rows = []
    files = sorted(config.EXPORT_DIR.glob("*"),
                   key=lambda p: p.stat().st_mtime, reverse=True)

    for path in files:
        if path.is_file():
            rows.append({
                "File": path.name,
                "Type": path.suffix.upper().lstrip("."),
                "Size (KB)": round(path.stat().st_size / 1024, 1),
                "Saved": datetime.fromtimestamp(
                    path.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            })

    return pd.DataFrame(rows)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.storage                        #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    sample = pd.DataFrame({
        "symbol": ["SAMP.N0000", "AEL.N0000", "ABAN.N0000"],
        "price": [136.75, 24.50, 1094.25],
        "change": [-0.25, 0.30, 0.00],
    })

    print("Saving a small example in all three formats")
    print("-" * 55)
    for path in export(sample, "example"):
        print("  saved:", path.name)

    print()
    print("Reading the CSV back, skipping the comment lines:")
    csv_file = sorted(config.EXPORT_DIR.glob("example_*.csv"))[-1]
    print(pd.read_csv(csv_file, comment="#").to_string(index=False))
