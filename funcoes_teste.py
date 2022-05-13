import math, random

def haversine(r,l1, long1, l2, long2): # Função haversine feita na academia python, mas que não fui usada
    a = (math.sin((math.radians(l2)-math.radians(l1))/2))**2
    b = (math.sin((math.radians(long2)-math.radians(long1))/2))**2
    c = math.cos(math.radians(l1))*math.cos(math.radians(l2))*b
    d = 2*r*math.asin((a+c)**(1/2))
    return d

def sorteia_letra(palavra, restricao): # Sorteia uma letra da capital do país sorteado impondo restrições no sorteio
    restricao_caracteres = ['.', ',', '-', ';', ' '] + restricao # caracteres especiais e as letras que já foram sorteadas

    palavra_tratada = str(palavra).lower()
    for caracter in restricao_caracteres:
        palavra_tratada = palavra_tratada.replace(caracter, "")
    if len(palavra_tratada) < 1:
        return ""
    else:
        return random.choice(list(palavra_tratada))