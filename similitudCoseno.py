import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Funcion que realiza acciones de PLN y devulve una matriz ponderada
def matrizPNL(df):

    # Crear el TF-IDF Vectorizer, seleccionando las stop words en ingles
    tfidf = TfidfVectorizer(stop_words='english')

    # Proceso PLN y construccion de la matriz TF-IDF
    tfidf_matriz = tfidf.fit_transform(df['overview'])

    return tfidf_matriz

# Función que calcula recomendaciones en base a su similitud
def similitudCoseno(pelicula_seleccionada, df, matrizTFIDF, cantidad_seleccionada, seleccion):
    # Obtener el indice de la película seleccionada por el usuario
    pelicula = df[df['title'] == pelicula_seleccionada].index[0]

    # Calcular la similitud del coseno entre las dos peliculas,
    cosine_sim = cosine_similarity(matrizTFIDF[pelicula], matrizTFIDF)

    # Obtener pares de índice de película y similitud
    similitudes = list(enumerate(cosine_sim[0]))

    # Ranking similitud
    if seleccion == 1:
        similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)
    elif seleccion == 0:
        similitudes = sorted(similitudes, key=lambda x: x[1], reverse=False)

    # Preparar una lista con el título de la película, descripcion y similitud
    peliculasSeleccionadas = [(df['title'].iloc[i[0]], df['overview'].iloc[i[0]], i[1]) for i in similitudes]

    # Devolver los títulos de las películas más similares y las puntuaciones de similitud
    return peliculasSeleccionadas[1:cantidad_seleccionada]  # Excluyendo la primera ya que es la misma película


# Funcion coordina las acciones y devuelve el DF final
def main_coseno(pelicula_seleccionada, cantidad_seleccionada, df, seleccion):

    # Llamada para generear la matriz
    matrizTFIDF = matrizPNL(df)

    # Llamada para calcular las similitudes
    listaDatos = similitudCoseno(pelicula_seleccionada, df, matrizTFIDF, (cantidad_seleccionada + 1), seleccion)

    # Crear una lista con los elempento devueltos
    datos = [{'Título': title, 'Descripcion': overview, 'Similitud': similitud} for title, overview, similitud in listaDatos]

    # Convertir la lista en un DF
    recommendations_df = pd.DataFrame(datos)

    return recommendations_df


if __name__ == "__main__":
    main_coseno()
