import pandas as pd

def read_excel_files(file_paths):
    df_list = []

    for idx, file_path in enumerate(file_paths, start=1):
        try:
            df = pd.read_excel(file_path)
            
            df.columns = df.columns.str.lower()
            df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
            df = df[df['state'].notna() & (df['state'] != '')]
            
            # Convert latitude and longitude to numeric values, errors='coerce' converts invalid values to NaN
            df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
            df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
            
            # Remove rows with NaN values in latitude or longitude columns
            df = df.dropna(subset=['latitude', 'longitude'])
            
            # print(f"[OK] File {idx} read: {file_path}")
            df_list.append(df)
        except Exception as e:
            print(f"[ERROR] Could not read File {idx} ({file_path}): {e}")
    
    return df_list