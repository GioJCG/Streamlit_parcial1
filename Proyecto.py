import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

sidebar = st.sidebar

sidebar.title("Informacion personal")
sidebar.write("Giovanni Jair Cabrera Garcia")
sidebar.write("zS22004370")
sidebar.write("Ingenieria de software")
imagen_path = "Credencial.png"

st.sidebar.image(imagen_path, caption="Credencial", width=200)

st.title("Explorador de Datos de Películas")

#Carga de dataset con cache
@st.cache_data
def load_data(nrows):
    data = pd.read_csv('movies3.csv', nrows=nrows)  
    return data


nrows = st.slider("Selecciona el número de filas a cargar", min_value=100, max_value=200000, value=100)

data = load_data(nrows)

st.write("Peliculas:")
st.dataframe(data)  


#Buscador por titulo
sidebar.header("Buscador de Información")
buscador = sidebar.text_input("Buscar película por título:")
if sidebar.button("Buscar"):
    resultado = data[data['name'].str.contains(buscador, case=False, na=False)]
    if not resultado.empty:
        st.write("Resultados de la búsqueda:")
        st.dataframe(resultado)
    else:
        st.warning("No se encontraron resultados.")


#Filltro por diracion maxima
st.header("Filtro por duracion Maxima")

columna_duracion = 'minute'  

# Slider para filtrar por minutos maximos
max_minutos = st.slider(
    "Selecciona la duración máxima (en minutos):",
    min_value=int(data[columna_duracion].min()), 
    max_value=int(data[columna_duracion].max()),  
    value=int(data[columna_duracion].max())   
)

data_filtrada = data[data[columna_duracion] >= max_minutos]

st.write(f"Mostrando {len(data_filtrada)} películas con duración máxima de {max_minutos} minutos:")
st.dataframe(data_filtrada)

#Histograma de los minutos
fig, ax = plt.subplots()
ax.hist(data.minute)
st.header("Histograma de los minutos")
st.pyplot(fig)

#Grafica de barras de raiting y minutos

fig2, ax2 = plt.subplots()
y_pos = data['rating']
x_pos = data['minute']

ax2.barh(y_pos, x_pos)
ax2.set_ylabel("RATING")
ax2.set_xlabel("MINUTOS")
ax2.set_title("Que raiting tuvieron las peliculas con el tiempo de duracion?")

st.header("Grafica de barras")
st.pyplot(fig2)

#Grafica de dispersion

fig3, ax3 = plt.subplots()

ax3.scatter(data.minute, data.rating)
ax3.set_xlabel("Minutos")
ax3.set_ylabel("Rating")

st.header("Grafica de dispersion de el rating")
st.pyplot(fig3)


# Gráfica de películas por fecha
st.header("Cantidad de películas por fecha")
#Agrupar la cantidad de peliculas

peliculas_fecha = data.groupby('date').size().reset_index(name='count')

fig4, ax4 = plt.subplots()
ax4.bar(peliculas_fecha['date'], peliculas_fecha['count'])
ax4.set_xlabel("Fecha")
ax4.set_ylabel("Películas")
ax4.set_title("Cantidad de películas estrenadas por fecha")

st.pyplot(fig4)
