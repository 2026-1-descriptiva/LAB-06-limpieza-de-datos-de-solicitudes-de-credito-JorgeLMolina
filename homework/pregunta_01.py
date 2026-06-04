"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import pandas as pd
import os
import numpy as np


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    if not os.path.exists("files/output"):
        os.makedirs("files/output")


    sol_credito = pd.read_csv("files/input/solicitudes_de_credito.csv",sep=";",encoding="utf-8")
    sol_credito.set_index(sol_credito.columns[0], inplace=True)

    sol_credito =sol_credito.dropna()

    columnas_texto = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "línea_credito"]

    sol_credito[columnas_texto] = sol_credito[columnas_texto].apply(
        lambda col: col
        .str.lower()                           
        .str.replace('á','a').str.replace('é','e').str.replace('í','i').str.replace('ó','o').str.replace('ú','u').str.replace('ñ','n')                           
        .str.replace(r'[^a-z0-9\s]', ' ', regex=True)
        .str.strip()                   
    )

    sol_credito["barrio"] = (
        sol_credito["barrio"]
        .str.lower()
        .str.replace(r"[-_]", " ", regex=True)
        )

    year_temporal= sol_credito["fecha_de_beneficio"].str.match(r"^\d{4}/")
    parsed = pd.Series(index=sol_credito.index, dtype="datetime64[ns]")
    parsed[~year_temporal] = pd.to_datetime(
        sol_credito.loc[~year_temporal, "fecha_de_beneficio"], dayfirst=True
    )
    parsed[year_temporal] = pd.to_datetime(
        sol_credito.loc[year_temporal, "fecha_de_beneficio"], format="%Y/%m/%d"
    )
    sol_credito["fecha_de_beneficio"] = parsed.dt.strftime("%Y/%m/%d")

    sol_credito['estrato'] = sol_credito['estrato'].astype(int)
    sol_credito['comuna_ciudadano'] = sol_credito['comuna_ciudadano'].astype(int)

    sol_credito['monto_del_credito'] = (
        sol_credito['monto_del_credito']
        .str.replace(r"[\$ ,]", "", regex=True) 
        .str.replace(r"\.0+$", "", regex=True)  
        .astype(int)
    )



    sol_credito = sol_credito.drop_duplicates()

    print(sol_credito.sexo.value_counts().to_list())
    sol_credito.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)


    return

pregunta_01()