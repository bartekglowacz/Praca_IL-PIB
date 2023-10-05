import pandas as pd

plik_ZNB_csv = "tmp/IZ702_SN23050_VHBA596_1_H_ATT_ON.csv"
wysokosci_csv = "tmp/h.txt"

# Wczytanie pliku CSV
df = pd.read_csv(plik_ZNB_csv, skiprows=2, sep=";")
wybrane_kolumny = df.loc[:, df.columns.str.contains("db:Mem|freq")]

# Wczytanie wysokości
plik_h = open(wysokosci_csv, "r")
df_wysokosci = [float(str(x.replace(",", "."))) for x in plik_h]
df_wysokosci = pd.DataFrame(df_wysokosci)
df_wysokosci = df_wysokosci.T

# Dodanie wysokości do DataFrame
wybrane_kolumny.loc[len(wybrane_kolumny), :] = [str(float(df_wysokosci[x])).replace(".", ",") for x in df_wysokosci]
plik_edited = pd.DataFrame(wybrane_kolumny)

plik_edited_kropki = plik_edited.replace(",", ".", regex=True).astype(float)
max_level = plik_edited_kropki.iloc[:, 1:].max(axis=1)
plik_edited_kropki['max [dB]'] = max_level
plik_edited_kropki['h [m]'] = plik_edited_kropki.iloc[len(plik_edited_kropki)-1, 1:].where(max_level)

print(plik_edited_kropki)
plik_edited_kropki.to_csv("tmp/wynik.csv", index=False, sep=";", decimal=",")
