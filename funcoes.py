import random, math

def sorteia_pais(dados): #Rafa
    pais = random.choice(list(dados.keys()))
    return pais

def normaliza(porContinente): #Bia
    saida = {}
    for continente,paises in porContinente.items():
        for pais,info in paises.items():
            info['continente'] = continente
            saida[pais] = info
    return saida

def haversine(r,l1, long1, l2, long2): #Bia
    
    a = (math.sin((math.radians(l2)-math.radians(l1))/2))**2
    b = (math.sin((math.radians(long2)-math.radians(long1))/2))**2
    c = math.cos(math.radians(l1))*math.cos(math.radians(l2))*b
    d = 2*r*math.asin((a+c)**(1/2))
    return d

def esta_na_lista(pais, lista): #Rafa
    paises = [item[0] for item in lista]
    if pais in paises:
        return True
    return False

def adiciona_em_ordem(pais, distancia, lista): #Rafa
    nova_lista = list(lista)
    nova_tentativa = [pais, distancia]

    if not esta_na_lista(pais, lista):
        for i, item in enumerate(lista):
            if item[1] >= distancia:
                nova_lista.insert(i, nova_tentativa)
                return nova_lista
        nova_lista.append(nova_tentativa)
    return nova_lista

def sorteia_letra(palavra, restricao): #Rafa
    restricao_caracteres = ['.', ',', '-', ';', ' '] + restricao

    palavra_tratada = str(palavra).lower()
    for caracter in restricao_caracteres:
        palavra_tratada = palavra_tratada.replace(caracter, "")
    if len(palavra_tratada) < 1:
        return ""
    else:
        return random.choice(list(palavra_tratada))
    
def montando_loja(pais, infos):
    loja = {}

    loja['continente'] = True
    loja['população'] = True
    loja['área'] = True
    loja['capital'] = len(infos['capital'])
    loja['bandeira'] = []
    for cor, quantidade in infos['bandeira']:
        if quantidade > 0 and cor != "outras":
            loja['bandeira'].append(cor)
    
    return loja