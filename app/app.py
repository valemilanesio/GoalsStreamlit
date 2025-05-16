import streamlit as st
import pandas as pd
import plotly.express as px
import os

def cargar_datos(jugador):
    return pd.read_csv(f"datasets/{jugador}.csv")

def set_background(jugador):
    jpg_path = f"images/{jugador}.jpg"
    webp_path = f"images/{jugador}.webp"
    imagen_path = jpg_path if os.path.exists(jpg_path) else webp_path if os.path.exists(webp_path) else None
    
    if imagen_path:
        desplazamientos = {"messi": "top 50px", "ronaldo": "top -40px", "lewandowski": "top 60px", "neymar": "top -80px"}
        desplazamiento = desplazamientos.get(jugador, "center")
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.3)), 
                            url("data:image/jpg;base64,{get_base64(imagen_path)}") no-repeat center {desplazamiento} fixed;
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

def get_base64(image_path):
    import base64
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    st.set_page_config(page_title="Goles de Messi, Lewandowski, Ronaldo y Neymar", layout="wide")

    st.markdown(
        """
        <h1 style="color: white; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9), -2px -2px 5px rgba(0, 0, 0, 0.9);">
        📊 Análisis de los goles de Messi, Lewandowski, Ronaldo y Neymar
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    jugadores = ["messi", "lewandowski", "ronaldo", "neymar"]
    datos = {jugador: cargar_datos(jugador) for jugador in jugadores}
    
    st.sidebar.header("Filtros")
    jugador_seleccionado = st.sidebar.selectbox("Selecciona un jugador", jugadores, format_func=lambda x: x.capitalize())
    club_seleccionado = st.sidebar.selectbox("Selecciona un club", ["Todos"] + list(datos[jugador_seleccionado]["Club"].unique()))
    rival_seleccionado = st.sidebar.selectbox("Selecciona un rival", ["Todos"] + list(datos[jugador_seleccionado]["Opponent"].unique()))
    
    # Mostrar los 10 rivales a los que el jugador ha hecho más goles
    st.sidebar.subheader("Rivales que más lo sufrieron")
    rivales_mas_sufridos = datos[jugador_seleccionado]["Opponent"].value_counts().head(20).reset_index()
    rivales_mas_sufridos.columns = ["Rival", "Goles"]
    st.sidebar.dataframe(rivales_mas_sufridos)
    
    set_background(jugador_seleccionado)
    
    df = datos[jugador_seleccionado]
    if club_seleccionado != "Todos":
        df = df[df["Club"] == club_seleccionado]
    if rival_seleccionado != "Todos":
        df = df[df["Opponent"] == rival_seleccionado]
    
    st.markdown(
        f"""
        <h3 style="color: white; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9), -2px -2px 5px rgba(0, 0, 0, 0.9);">
        Goles de {jugador_seleccionado.capitalize()}
        </h3>
        """,
        unsafe_allow_html=True
    )
    st.dataframe(df)
    
    # Añadir espacio entre la tabla y la primera gráfica
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <h3 style="color: white; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9), -2px -2px 5px rgba(0, 0, 0, 0.9);">
        📈 Goles por temporada
        </h3>
        """,
        unsafe_allow_html=True
    )
    
    df["Year"] = pd.to_datetime(df["Date"]).dt.year
    goles_por_ano = df.groupby("Year").size().reset_index(name="Goles")
    fig = px.bar(goles_por_ano, x="Year", y="Goles", title=f"Goles por temporada de {jugador_seleccionado.capitalize()}", color="Goles", color_continuous_scale="Blues")
    st.plotly_chart(fig)
    
    st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <h3 style="color: white; text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.9), -2px -2px 5px rgba(0, 0, 0, 0.9);">
        ⏱️ Distribución de goles por minuto
        </h3>
        """,
        unsafe_allow_html=True
    )
    
    df["Minute"] = df["Minute"].str.replace("'", "").astype(str)
    df = df[df["Minute"].str.isnumeric()]
    df["Minute"] = df["Minute"].astype(int)
    minutos = df["Minute"].value_counts().reset_index()
    minutos.columns = ["Minute", "Goles"]
    fig = px.scatter(minutos, x="Minute", y="Goles", title=f"Distribución de goles por minuto de {jugador_seleccionado.capitalize()}", color="Goles", color_continuous_scale="Reds")
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
