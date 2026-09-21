import streamlit as st

def parse_window_size(val_str: str, total: int):
    """
    Mengubah input teks (misal: '120' atau '20%') menjadi nilai integer 
    dengan proteksi rentang minimal 1 hingga maksimal `total`.
    """
    val_str = str(val_str).strip()
    if not val_str:
        return None
    
    parsed_val = None
    if val_str.endswith("%"):
        try:
            pct = float(val_str.replace("%", "").strip())
            parsed_val = int(round((pct / 100.0) * total))
        except ValueError:
            return None
    else:
        try:
            parsed_val = int(float(val_str))
        except ValueError:
            return None

    if parsed_val is not None:
        return max(1, min(parsed_val, total))
    return None


# def init_sliding_window_state(unique_dates_str):
#     """Inisialisasi Session State awal dengan memastikan batas aman."""
#     total_dates = len(unique_dates_str)
#     if "window_size_input" not in st.session_state:
#         st.session_state.window_size_input = "100%"
#     if "window_size" not in st.session_state:
#         st.session_state.window_size = parse_window_size("100%", total_dates) or total_dates
#     if "min_idx" not in st.session_state:
#         st.session_state.min_idx = 0
#     if "max_idx" not in st.session_state:
#         st.session_state.max_idx = min(total_dates, st.session_state.window_size)

def init_sliding_window_state(unique_dates_str):
    """Inisialisasi & sinkronisasi Session State awal dengan batas aman."""
    total_dates = len(unique_dates_str)
    if "window_size_input" not in st.session_state:
        st.session_state.window_size_input = "100%"
        
    # Hitung ulang window size sesuai input teks dan total_dates dataset aktif
    parsed_size = parse_window_size(st.session_state.window_size_input, total_dates)
    st.session_state.window_size = parsed_size if parsed_size is not None else total_dates

    # Pastikan index tidak melebihi total_dates dari dataset yang baru diupload
    if "min_idx" not in st.session_state or st.session_state.min_idx >= total_dates:
        st.session_state.min_idx = 0

    # Jika window_size_input adalah 100% atau dataset baru dimuat, set max_idx ke total_dates
    if st.session_state.window_size_input == "100%":
        st.session_state.max_idx = total_dates
    else:
        st.session_state.max_idx = min(total_dates, st.session_state.min_idx + st.session_state.window_size)


def sync_date_widgets(unique_dates_str):
    """Update widget key `selected_start_date` & `selected_end_date` agar UI otomatis berubah."""
    total_dates = len(unique_dates_str)
    safe_min = max(0, min(st.session_state.min_idx, total_dates - 1))
    safe_max = max(0, min(st.session_state.max_idx - 1, total_dates - 1))
    
    st.session_state.selected_start_date = str(unique_dates_str[safe_min])
    st.session_state.selected_end_date = str(unique_dates_str[safe_max])


def on_window_change(unique_dates_str):
    """Callback ketika input Panjang Window diubah."""
    total_dates = len(unique_dates_str)
    size = parse_window_size(st.session_state.window_size_input, total_dates)
    if size is not None:
        st.session_state.window_size = size
        if st.session_state.min_idx + size <= total_dates:
            st.session_state.max_idx = st.session_state.min_idx + size
        else:
            st.session_state.max_idx = total_dates
            st.session_state.min_idx = max(0, total_dates - size)
        sync_date_widgets(unique_dates_str)


def on_start_date_change(unique_dates_str):
    """Callback saat Tanggal Mulai diubah oleh user."""
    total_dates = len(unique_dates_str)
    selected_date = str(st.session_state.selected_start_date)
    
    if selected_date in unique_dates_str:
        new_min = unique_dates_str.index(selected_date)
        w_size = st.session_state.window_size
        
        new_max = new_min + w_size
        if new_max <= total_dates:
            st.session_state.min_idx = new_min
            st.session_state.max_idx = new_max
        else:
            st.session_state.max_idx = total_dates
            st.session_state.min_idx = max(0, total_dates - w_size)
            
        sync_date_widgets(unique_dates_str)


def on_end_date_change(unique_dates_str):
    """Callback saat Tanggal Akhir diubah oleh user."""
    total_dates = len(unique_dates_str)
    selected_date = str(st.session_state.selected_end_date)
    
    if selected_date in unique_dates_str:
        new_max = unique_dates_str.index(selected_date) + 1 
        w_size = st.session_state.window_size
        
        new_min = new_max - w_size
        if new_min >= 0:
            st.session_state.min_idx = new_min
            st.session_state.max_idx = new_max
        else:
            st.session_state.min_idx = 0
            st.session_state.max_idx = min(total_dates, w_size)
            
        sync_date_widgets(unique_dates_str)