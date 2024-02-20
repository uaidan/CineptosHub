import pandas as pd


# El resultado será un valor entre 0 y 1 (similitud nula o total respectivamente)
def sorensen_dice(ejemplar1, ejemplar2):
    interseccion = 0
    # Calculamos la interseccion con un contador, aumentandolo cuando un elemento del ejemplar1 esta en el ejemplar2
    for genero in ejemplar1:
        if genero in ejemplar2:
            interseccion += 1
    indice_sorensen = 2 * interseccion / (len(ejemplar1) + len(ejemplar2))

    return indice_sorensen


# Funcion que encuentra la pelicula selccionada, generea el df final ya ordenado
def main_soren(pelicula_seleccionada, cantidad_seleccionada, df, seleccion):

    pelicula_encontrada = False
    generos = set()

    # Generos del usuario
    for index, pelicula in df.iterrows():
        if pelicula['title'] == pelicula_seleccionada:
            generos = set(pelicula['genres'].split(', '))
            print(generos)
            pelicula_encontrada = True

    if pelicula_encontrada:
        # Dataframe de peliculas con similitudes
        similitud_df = pd.DataFrame(columns=['Pelicula', 'Generos', 'Similitud'])

        for i, peliculas in df.iterrows():
            generos_otra_pelicula = set(peliculas['genres'].split(', '))
            similitud = sorensen_dice(generos, generos_otra_pelicula)
            fila_similitud = {'Pelicula': peliculas['title'], 'Generos': peliculas['genres'], 'Similitud': similitud}

            # Añadir nueva fila, siempre que no sea la pelicula seleccionada
            if peliculas['title'] != pelicula_seleccionada:
                similitud_df = pd.concat([similitud_df, pd.DataFrame(fila_similitud, index=[0])], ignore_index=True)

        # Ranking similitud
        if seleccion == 1:
            similitud_df = similitud_df.sort_values(by='Similitud', ascending=False, ignore_index=True)
        elif seleccion == 0:
            similitud_df = similitud_df.sort_values(by='Similitud', ascending=True, ignore_index=True)

        return similitud_df.head(cantidad_seleccionada)


if __name__ == "__main__":
    main_soren()
