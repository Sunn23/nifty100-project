def remove_duplicates(df, subset):

    rows_before = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates(subset=subset)

    rows_after = len(df)

    removed = rows_before - rows_after

    return df, rows_before, rows_after, removed