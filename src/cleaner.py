import pandas as pd

def clean_data(file):
    try:
        df = pd.read_csv(file)
        # التنظيف: إزالة الصفوف التي تحتوي على قيم فارغة
        cleaned_df = df.dropna(how='any')
        return cleaned_df
    except Exception as e:
        return None