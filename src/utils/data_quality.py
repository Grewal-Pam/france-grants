def assert_no_nulls(df, cols):
    for col in cols:
        if df[col].isnull().any():
            raise ValueError(f"Null values found in {col}")


def assert_year_range(df, col="year", min_year=1950, max_year=2050):
    bad = df[(df[col] < min_year) | (df[col] > max_year)]
    if len(bad) > 0:
        raise ValueError(f"Invalid years detected in {col}")


def assert_positive(df, col="amount_usd"):
    negatives = df[df[col] < 0]
    if len(negatives) > 0:
        print(f"⚠️  Warning: {len(negatives)} negative grant entries, converting to 0")
    df[col] = df[col].clip(lower=0)

