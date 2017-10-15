import bs4
import urllib3
import imdbpie


imdb = imdbpie.Imdb(anonymize=True)
def getMovieInfo(movie_title):

    movies = imdb.search_for_title(movie_title)
    if(len(movies)<1):
        return('Lo siento, no he encontrado esa película...')
    else:
        movie = imdb.get_title_by_id(movies[0]['imdb_id'])
        movie_info = "*"+movie.title + " - imdb rating: " + str(movie.rating) + "\nReparto:* " + str([x.name for x in movie.cast_summary]) + "\n*Sinopsis:* " + movie.plot_outline
        return(movie_info)


def fromDictToString(cine, dict):
    info_str = cine + '\n _______________ \n\n'
    for key, value in dict.items():
        info_str = info_str + key + '\n' + str(value) + '\n - - - - - - \n'
    return info_str


http = urllib3.PoolManager()
def getMoviesFromNeocineWebsite(cine ,url):

    html = http.request('GET', url)
    soup = bs4.BeautifulSoup(html.data, 'html.parser')

    response_dict = {}
    titles_used = []

    movie_boxes = soup.find_all(class_='pelicart')
    for movie in movie_boxes:
        title = movie.find('h3').get_text()
        pases = movie.find_all(class_='label label-warning lnksesion')
        pases_horas = [x.get_text() for x in pases]

        if title in titles_used:
            break
        else:
            titles_used.append(title)

        response_dict[title] = pases_horas

    return(fromDictToString(cine, response_dict))

def getMoviesFromCineramaWebsite(cine, url):

    html = http.request('GET', url)
    soup = bs4.BeautifulSoup(html.data, 'html.parser')

    response_dict = {}
    titles_used = []

    movie_boxes = soup.find_all(class_='box_movie ftLeft')
    for movie in movie_boxes:
        title = movie.find('h3').get_text()
        pases = movie.find_all('li')
        pases_horas = [x.get_text() for x in pases]

        if title in titles_used:
            break
        else:
            titles_used.append(title)

        response_dict[title] = pases_horas

    return(fromDictToString(cine, response_dict))

# For testing #
#
# url = "http://www.neocine.es/cine/4/espacio-mediterraneo--cartagena-/lang/es"
# cine = "Espacio Mediterraneo"
#
# print(getMoviesFromNeocineWebsite(cine,url))

# url = "https://www.cinerama.es/cartelera/cine/nueva-condomina/"
# cine = "Nueva Condomina:"
# print(getMoviesFromCinesaWebsite(cine, url))