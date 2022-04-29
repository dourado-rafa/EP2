import random, math

def normaliza(dados):
    dados_normalizados = {}
    for continente, paises in dados.items():
        for nome, dados in paises.items():
            dados_normalizados[nome] = dados
            dados_normalizados[nome]['continente'] = continente
    return dados_normalizados


def sorteia_pais(dados):
    pais = random.choice(list(dados.keys()))
    return pais

def haversine(raio, latitude1, longitude1, latitude2, longitude2):

    latitude1 = math.radians(latitude1)
    latitude2 = math.radians(latitude2)
    longitude1 = math.radians(longitude1)
    longitude2 = math.radians(longitude2)
    
    a = math.sin((latitude2-latitude1)/2)**2
    b = math.cos(latitude1)*math.cos(latitude2)
    c = math.sin((longitude2-longitude1)/2)**2
    x = 2*raio*math.asin((a + b*c)**0.5)

    return x

def adiciona_em_ordem(pais, distancia, lista):
    nova_lista = list(lista)
    nova_tentativa = [pais, distancia]

    if not esta_na_lista(pais, lista):
        for i, item in enumerate(lista):
            if item[1] >= distancia:
                nova_lista.insert(i, nova_tentativa)
                return nova_lista
        nova_lista.append(nova_tentativa)
    return nova_lista

def esta_na_lista(pais, lista):
    paises = [item[0] for item in lista]
    if pais in paises:
        return True
    return False

def sorteia_letra(palavra, restricao):
    restricao_caracters = ['.', ',', '-', ';', ' '] + restricao

    palavra_tratada = str(palavra).lower()
    for caracter in restricao_caracters:
        palavra_tratada = palavra_tratada.replace(caracter, "")
    if len(palavra_tratada) < 1:
        return ""
    else:
        return random.choice(list(palavra_tratada))