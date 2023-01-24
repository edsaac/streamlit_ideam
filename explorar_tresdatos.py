import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scipy.stats import linregress

datos = pd.read_csv("datos_ideam/tresestaciones.csv")
st.write(datos.info())

opciones = datos["NombreEstacion"].unique()
estacion_x = st.selectbox("Seleccione una estación", opciones)
estacion_y = st.selectbox("Seleccione la otra estación", opciones)

df_x = datos[datos["NombreEstacion"] == estacion_x]
df_x = df_x[["Fecha", "Valor"]]
df_x["Fecha"] = pd.to_datetime(df_x["Fecha"], format=r"%Y-%m-%d %H:%M")

df_y = datos[datos["NombreEstacion"] == estacion_y]
df_y = df_y[["Fecha", "Valor"]]
df_y["Fecha"] = pd.to_datetime(df_y["Fecha"], format=r"%Y-%m-%d %H:%M")

fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df_x["Fecha"], df_x["Valor"], label=estacion_x, lw=1)
ax.plot(df_y["Fecha"], df_y["Valor"], label=estacion_y, lw=1)
ax.set_xlabel("Fecha", fontsize=14)
ax.set_ylabel("Caudal medio diario [m³/d]", fontsize=14)
ax.legend()
st.pyplot(fig)

combinado = df_x.merge(df_y, on="Fecha", suffixes=[f"_{estacion_x}", f"_{estacion_y}"])

regresión = linregress(combinado[f"Valor_{estacion_x}"], combinado[f"Valor_{estacion_y}"])
label_regresión = f"""Regresión Lineal: 
$y = {regresión.slope:.3f} * x + {regresión.intercept:.1f}$
R² = {regresión.rvalue**2:.3f}"""

fig, ax = plt.subplots(figsize=(7,7))
ax.set_aspect("equal")
ax.scatter(combinado[f"Valor_{estacion_x}"], combinado[f"Valor_{estacion_y}"], marker=".", s=10)
ax.axline((0,regresión.intercept), slope=regresión.slope, label=label_regresión, ls="dashed", c="k")
ax.set_xlabel(f"CMD {estacion_x} [m³/s]", fontsize=14)
ax.set_ylabel(f"CMD {estacion_y} [m³/s]", fontsize=14)
ax.set_ylim(0, 7000)
ax.set_xlim(0, 7000)
ax.spines.top.set_visible(False)
ax.spines.right.set_visible(False)
ax.legend(fontsize=12)
st.pyplot(fig)