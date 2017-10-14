import bs4
import urllib3

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