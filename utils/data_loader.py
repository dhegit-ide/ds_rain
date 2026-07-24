import pandas as pd
import numpy as np

def validate_csv(df):
    if df is None or df.empty:
        return False, ":material/error: File kosong! Tidak ada data yang bisa diproses."
    if 'ds' not in df.columns:
        return False, ":material/error: Dataset tidak memiliki kolom 'ds' (tanggal)."
    if 'unique_id' not in df.columns:
        return False, ":material/error: Dataset tidak memiliki kolom 'unique_id' (nama wilayah)."        

    try: 
        df['ds'] = pd.to_datetime(df['ds'])
    except: 
        return False, ":material/error: Kolom 'ds' harus berformat tanggal (YYYY-MM-DD)."
    return True, ":material/check: File valid! Dataset siap diproses."


def validate_cv_df(df):
    if df is None or df.empty:
        return False, ":material/error: File kosong! Tidak ada data yang bisa diproses."
    required_cols = ["unique_id", "ds", "cutoff", "y"]
    for col in required_cols:
        if col not in df.columns:
            return False, f":material/error: Dataset tidak memiliki kolom wajib '{col}'."

    # cek minimal ada 1 kolom tambahan (hasil prediksi)
    pred_cols = [c for c in df.columns if c not in required_cols]
    if len(pred_cols) < 1:
        return False, ":material/error: Dataset harus punya minimal 1 kolom hasil prediksi model."

    try:
        df["ds"] = pd.to_datetime(df["ds"], errors="coerce")
        df["cutoff"] = pd.to_datetime(df["cutoff"], errors="coerce")
    except:
        return False, ":material/error: Kolom 'ds' dan 'cutoff' harus berformat tanggal (YYYY-MM-DD)."

    return True, ":material/check: File cv_df valid! Dataset siap diproses."


def get_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    exclude_cols = ['unique_id', 'ds']
    numeric_cols = [col for col in numeric_cols if col not in exclude_cols]
    return numeric_cols

def r2(
    df: pd.DataFrame,
    models: list,
    id_col: str = "unique_id",
    target_col: str = "y",
) -> pd.DataFrame:
    """Compute R² = 1 − SS_res/SS_tot per unique_id and model."""
    rows = []
    for uid, grp in df.groupby(id_col, observed=True, sort=False):
        row = {id_col: uid}
        y_true = grp[target_col].to_numpy(float)
        for model in models:
            y_pred = grp[model].to_numpy(float)
            valid  = np.isfinite(y_true) & np.isfinite(y_pred)
            yt, yp = y_true[valid], y_pred[valid]
            if len(yt) < 2:
                row[model] = np.nan
                continue
            ss_tot = np.sum((yt - yt.mean()) ** 2)
            ss_res = np.sum((yt - yp) ** 2)
            row[model] = np.nan if ss_tot == 0 else 1.0 - ss_res / ss_tot
        rows.append(row)
    return pd.DataFrame(rows)