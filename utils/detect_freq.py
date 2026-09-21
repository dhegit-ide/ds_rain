import pandas as pd

def detect_and_summary(df, date_col='ds', group_col='unique_id'):
    dates = pd.to_datetime(df[date_col].unique())
    dates = pd.Series(sorted(dates))
        
    start = dates.min()
    end = dates.max()
        
    diffs = dates.diff().dropna()
    median_diff = diffs.median()
    days = median_diff.days
        
    if days == 1:
        freq = "Harian"
        total = (end - start).days + 1
        unit = "hari"
    elif 28 <= days <= 31:
        freq = "Bulanan"
        total = (end.year - start.year) * 12 + (end.month - start.month) + 1
        unit = "bulan"
    elif 365 <= days <= 366:
        freq = "Tahunan"
        total = end.year - start.year + 1
        unit = "tahun"
    else:
        freq = "tidak jelas"
        total = len(df)
        unit = "baris"
        
    return freq, start.date(), end.date(), total, unit