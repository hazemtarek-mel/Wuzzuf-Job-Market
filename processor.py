import pandas as pd
import os

RAW_DATA_PATH = "data/wuzzuf_jobs_raw.csv"
CLEAN_DATA_PATH = "data/wuzzuf_jobs_clean.csv"

def process_data():
    """
    Reads raw data, cleans it, filters for Egypt only, and saves to clean CSV.
    Returns the cleaned DataFrame.
    """
    if not os.path.exists(RAW_DATA_PATH):
        print(f"Error: {RAW_DATA_PATH} not found.")
        return pd.DataFrame()

    try:
        # 1. Load Raw Data
        df = pd.read_csv(RAW_DATA_PATH)
        
        # 2. Basic Cleaning (Missing Values)
        df['Job Title'] = df['Job Title'].fillna("Unknown")
        df['Company Name'] = df['Company Name'].fillna("Unknown")
        df['Location'] = df['Location'].fillna("Unknown")
        df['Skills'] = df['Skills'].fillna("")
        df['Job Type'] = df['Job Type'].fillna("Unknown")
        df['Level'] = df['Level'].fillna("Unknown")

        # 3. Extract City (First part of location)
        # e.g. "Maadi, Cairo, Egypt" -> "Maadi"
        df['City'] = df['Location'].apply(lambda x: x.split(',')[0].strip() if isinstance(x, str) else x)

        # 4. FILTER: Egypt Only
        # We explicitly remove jobs that don't satisfy the Egypt location requirement
        df = df[df['Location'].str.contains("Egypt", case=False, na=False)]

        # 5. Save to Clean CSV
        df.to_csv(CLEAN_DATA_PATH, index=False)
        print(f"Data processed successfully. Saved {len(df)} rows to {CLEAN_DATA_PATH}")
        
        return df
        
    except Exception as e:
        print(f"Error during data processing: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    process_data()
