import random, math

def normaliza(porContinente):
    saida = {}
    for continente,paises in porContinente.items():
        for pais,info in paises.items():
            info['continente'] = continente
            saida[pais] = info
    return saida

def sorteia_pais(dicionario):
    paises = []
    for pais in dicionario:
        paises.append(pais)
    sorteado = random.choice(paises)
    return sorteado    

def haversine(r,l1, long1, l2, long2):

    a = (math.sin((math.radians(l2)-math.radians(l1))/2))**2
    b = (math.sin((math.radians(long2)-math.radians(long1))/2))**2
    c = math.cos(math.radians(l1))*math.cos(math.radians(l2))*b
    d = 2*r*math.asin((a+c)**(1/2))
    return d

def adiciona_em_ordem(pais,distancia,lista):
    if len(lista) == 0:
        lista = [[pais,distancia]]
        return lista
    
    novaLista = []
    adicionou = False
    
    for item in lista:
        p = item[0]
        d = item[1]
        if pais == p:
            return lista
        if distancia > d:
            novaLista.append(item)
        elif distancia < d:
            if not adicionou:
                novaLista.append([pais,distancia])
                adicionou = True
            novaLista.append(item)
        if not adicionou and len(novaLista) ==len(lista):
            novaLista.append([pais,distancia])
    
    return novaLista

def esta_na_lista(pais,lista):
    esta = False
    i = 0
    while not esta and i < len(lista):
        if pais == lista[i][0]:
            esta = True
        i += 1
    return esta



