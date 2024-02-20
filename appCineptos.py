import streamlit as st
import pandas as pd
from sorensenDice import main_soren
from similitudCoseno import main_coseno

# Cargar de del csv a un DF
archivo = 'peliculas.csv'
df = pd.read_csv(archivo)


# Funcion que muestra al usuario el buscador de peliculas
def busacdorPelicula():
    # Info para el usuario
    st.title('Buscador de Películas')
    st.write("""
    1. **Selecciona o Busca una Película**: Utiliza el menú desplegable para seleccionar una película de la lista, si lo prefiere escriba su titulo en el campo de búsqueda.
    2. **Cantidad de Películas Similares**: Selecciona cuántas películas similares deseas ver en el resultado.
    3. **Opciones de Búsqueda**: Elige si quieres obtener películas **similares** o **opuestas** a tu selección.

    Una vez configuradas tus preferencias, presiona el botón para obtener tus recomendaciones.
    """)

    # Filtrar el DataFrame basado en la eleccion del usuario
    filtered_df = df[df['title'].str.contains("", case=False, na=False)]

    # Seleccionar una película de las filtradas
    selected_movie = st.selectbox('Selecciona una película', filtered_df['title'].unique())

    # Permitir al usuario especificar cuántas películas similares desea ver
    num_similar_movies = st.slider('Número de películas similares a mostrar', 1, 20, 5)

    # Dejar que el usuario decida que accion tomar
    opciones = ["Peliculas Similares", "Peliculas Opuestas"]
    eleccion = st.radio("Elige una opción:", opciones)

    # Filtrar dependiendo de lo que el usuario quiera realizar (similar o opuesta)
    seleccion = 1
    if eleccion == "Peliculas Opuestas":
        seleccion = 0

    return selected_movie, num_similar_movies, df, seleccion


# Funcion que calcula la similitud en funcion de Sørensen-Dice
def similitudSorensenDice():
    haydatos = 0

    # Llamada a la funcion que nos muestra la lista de peliculas
    peliSeleccionada, cantidad, df, seleccion = busacdorPelicula()

    # Espaciador que nos ayuda a centrar la cosas en pantalla
    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])

    with col_central:
        if st.button("Calcular Similitudes (Sørensen-Dice)"):
            with st.spinner('Ejecutando... Por favor, espera.'):
                # Llamada al script que nos devuelve la similitud entre la pelicula seleccionada (query) y las demas
                df_final = main_soren(peliSeleccionada, cantidad, df, seleccion)
                haydatos = 1

    # Controlamos si hay datos para mostrarlos sin que nos de errores
    if haydatos == 1:
        st.dataframe(df_final)


# Funcion que calcula la similitud en funcion del coseno
def similitudCoseno():
    haydatos = 0

    # Llamada a la funcion que nos muestra la lista de peliculas
    peliSeleccionada, cantidad, df, seleccion = busacdorPelicula()

    # Espaciador que nos ayuda a centrar la cosas en pantalla
    espaciador_izquierda, col_central, espaciador_derecha = st.columns([1, 2, 1])

    with col_central:
        if st.button("Calcular Similitudes (Coseno)"):
            with st.spinner('Ejecutando... Por favor, espera.'):
                # Llamada al script que nos devuelve la similitud entre la pelicula seleccionada (query) y las demas
                df_final = main_coseno(peliSeleccionada, cantidad, df, seleccion)
                haydatos = 1

    # Controlamos si hay datos para mostrarlos sin que nos de errores
    if haydatos == 1:
        st.dataframe(df_final)


# Funcion que nos permite introducir manualmente una nueva pelicula al DataSet
def meterPelicula():
    # Formulario de informacion acerca de la pelicula
    with st.form(key='peli_form'):
        titulo = st.text_input("Título de la película")
        generos = st.text_input("Géneros de la película (en inglés, separados por comas)")
        descripcion = st.text_area("Descripción de la película (en inglés)")

        # Transformar a minusculas todas las letras y la primera letra a mayúscula
        generos = generos.lower()
        generos = generos.title()

        submit_button = st.form_submit_button(label='Añadir película')

    if submit_button:
        if titulo and generos and descripcion:
            # Creamos una nueva fila con los datos que nos ha proporcionado el usuario
            nueva_pelicula = {
                'budget': 0,
                'genres': generos,
                'homepage': 0,
                'id': 0,
                'keywords': 0,
                'original_language': 0,
                'original_title': 0,
                'overview': descripcion,
                'popularity': 0,
                'production_companies': 0,
                'production_countries': 0,
                'release_date': 0,
                'revenue': 0,
                'runtime': 0,
                'spoken_languages': 0,
                'status': 0,
                'tagline': 0,
                'title': titulo,
                'vote_average': 0,
                'vote_count': 0
            }

            # Añadimos esta linea al DataFrame
            df_new = pd.concat([df, pd.DataFrame([nueva_pelicula])], ignore_index=True)

            # Guardamos el DataFrame actualizado
            df_new.to_csv('peliculas.csv', index=False)

            st.success('Película añadida exitosamente!')
        else:
            # Mostrar un mensaje de error si algún campo está vacío
            st.error('Por favor, rellena todos los campos.')


# Menú lateral para selección
opcion = st.sidebar.selectbox("Elige una opción:",
                              ["Inicio", "Similitud del coseno", "Similitud Sørensen-Dice", "Añadir una Pelicula"])

if opcion == "Inicio":
    st.title("CINEPTOS Hub by KleinCorp")

    st.write("""
    ---
    ### Explora Películas Similares y Descubre Nuevos Títulos

    En esta aplicación, puedes buscar películas similares utilizando dos métodos distintos:

    - **Similitud del Coseno**: Este método mide la similitud entre dos películas analizando la orientación de sus vectores de características en un espacio multidimensional. Es efectivo para identificar películas con descripciones o características similares.

    - **Sorensen-Dice**: Este índice compara la similitud de los conjuntos de características de dos películas, como géneros o palabras clave. Es útil para encontrar películas con atributos en común.

    Además, tienes la oportunidad de **añadir una nueva película** a nuestra base de datos. Solo completa el formulario con los detalles de la película y será incluida para futuras búsquedas de similitud.

    **:memo: Comienza a explorar desde el menú lateral estas herramientas y descubre el mundo del cine.**
    """)


elif opcion == "Similitud del coseno":
    similitudCoseno()

elif opcion == "Similitud Sørensen-Dice":
    similitudSorensenDice()

elif opcion == ("Añadir una Pelicula"):
    st.title('Añadir una Película Nueva')

    st.write("""
    - **Rellena todos los campos**: Todos los campos son obligatorios.
    - **Idioma**: Por favor, introduce toda la información en inglés para asegurar resultados óptimos.
    - **Géneros**: Introduce los géneros de la película, separados por comas. Por ejemplo, 'Action, Adventure'.
    - **Descripción detallada**: Proporciona una descripción clara y detallada de la película.
    """)

    meterPelicula()

