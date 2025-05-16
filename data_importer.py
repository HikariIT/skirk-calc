import pandas as pd

chars = ['Furina', 'Escoffier', 'Citlali', 'Skirk']
param_dict = {}

for i in range(1, 5):
    df = pd.read_excel(r"C:\Users\xdart\Desktop\Skirk Rotation Assembler.xlsx", sheet_name=f"Character{i}", usecols="T:Z", skiprows=14, nrows=30)
    df = df.dropna(how='all')
    df['Element'] = df['Element'].fillna("None")
    df['ICD'] = df['ICD'].fillna("None")
    df['DMG Talent Type'] = df['DMG Talent Type'].fillna("N/A")
    final_dict = {}

    for j in range(len(df)):
        final_dict[df.iloc[j, 0]] = (df.iloc[j, 1], df.iloc[j, 2])

    param_dict[chars[i - 1]] = final_dict

print(param_dict)

