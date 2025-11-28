import os
import pandas as pd
from pathlib import Path
import numpy as np
import sqlite3

groups = {
    "RTX1": [4419, 4420, 4421, 4422, 4423, 4424],
    "RTX2": [4435, 4436, 4437, 4438, 4439, 4440],
    "RTX3": [4443, 4444, 4445, 4446, 4448],
    "RTX4": [4451, 4452, 4454, 4455, 4456],
    "RTX5": [4475, 4476, 4477, 4478, 4479, 4480],
    "RTX6": [4483, 4484, 4485, 4486, 4487, 4488],
    "RTX7": [4499, 4501, 4503, 4504],
    "RTX8": [4507, 4508, 4509, 4510, 4511, 4512],
    "RTX9": [4515, 4516, 4517, 4518, 4519, 4520]
}

root_path = Path(__file__).parent.parent / "data" / "csv"


def get_rtx_group(volume):
    for group, volumes in groups.items():
        if volume in volumes:
            return group
    return None


def train_or_valid(df_length, ratios=[0.8, 0.15, 0.05]):
    return np.random.choice(['train', 'valid', 'test'], size=df_length, p=ratios)


def to_sqlite(final_df, sqlite_path):

    # Nom de la table dans laquelle sauvegarder le DataFrame
    table_name = "dataset"

    # Créer une connexion à la base de données SQLite
    conn = sqlite3.connect(sqlite_path)

    # Sauvegarder le DataFrame dans la table
    final_df.to_sql(table_name, conn, if_exists="replace", index=False)

    # Fermer la connexion
    conn.close()

    print(
        f"Le DataFrame a été sauvegardé dans {sqlite_path}, table '{table_name}'.")


def create_dataframe():

    # Liste des volumes
    volumes = []
    for g, v in groups.items():
        volumes += v

    print(f"nombre de cubes : {len(volumes)}")

    # Liste pour stocker les DataFrames
    dfs = []

    # Parcourir chaque volume
    for volume in volumes:
        pattern = f"volume_{volume}_[100, 100, 100]_random.csv"
        for root, dirs, files in os.walk(root_path):
            for file in files:
                if file == pattern:
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    group = get_rtx_group(volume)
                    df['RTX'] = group

                    if group in ['RTX2', 'RTX4', 'RTX8']:
                        kind = "other"
                    else:
                        kind = train_or_valid(len(df))
                    df['kind'] = kind

                    dfs.append(df)

    # Concaténer tous les DataFrames
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        print("DataFrame final :")
        print(final_df[final_df['RTX'] == 'RTX8'].head())
    else:
        print("Aucun fichier trouvé.")

    return final_df


if __name__ == "__main__":
    final_df = create_dataframe()
    proportions = final_df['kind'].value_counts(normalize=True)

    # Afficher les proportions
    print("Proportions des étiquettes dans 'kind' :")
    print(proportions, proportions*len(final_df))

    to_sqlite(final_df, "dataset_random.db")
