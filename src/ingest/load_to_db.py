from sqlalchemy import create_engine
from pathlib import Path

ENGINE = create_engine("sqlite:///./grants.db", future=True)

def write_df(df):
    with ENGINE.begin() as conn:
        df.to_sql("grants", conn, if_exists="append", index=False)
