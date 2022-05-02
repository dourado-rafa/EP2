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

# def haversine(r,l1, long1, l2, long2): #Bia
    
#     a = (math.sin((math.radians(l2)-math.radians(l1))/2))**2
#     b = (math.sin((math.radians(long2)-math.radians(long1))/2))**2
#     c = math.cos(math.radians(l1))*math.cos(math.radians(l2))*b
#     d = 2*r*math.asin((a+c)**(1/2))
#     return d

def haversine(pais, paisTestado): #Bia
    l1 = math.radians(paisTestado['geo']['latitude'])
    long1 = math.radians(paisTestado['geo']['longitude'])
    l2 = math.radians(pais['geo']['latitude'])
    long2 = math.radians(pais['geo']['longitude'])
    raio = 6371

    a = (math.sin((l2-l1)/2))**2
    b = (math.sin((long2-long1)/2))**2
    c = math.cos(l1)*math.cos(l2)*b
    d = 2*raio*math.asin((a+c)**(1/2))
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
    
def montando_loja(infosPais):
    loja = {}

    loja['Continente'] = True
    loja['População'] = True
    loja['Área'] = True
    loja['Letra da capital'] = []
    loja['Cor da bandeira'] = []
    for cor, quantidade in infosPais['bandeira'].items():
        if quantidade > 0 and cor != "outras":
            loja['Cor da bandeira'].append(cor)
    
    return loja

def menu_dicas(infosPais, loja, tentativas, dicas):
    menu = ''
    n = 0
    opcoesNome = []

    if len(loja['Cor da bandeira']) > 0:
        custo = 4
        if custo <= tentativas:
            n += 1
            opcoesNome.append('Cor da bandeira')
            menu += ('{}. Cor da bandeira - custa {} tentativas\n'.format(n,custo))
    if len(loja['Letra da capital']) < len(infosPais['capital']):
        custo = 3
        if custo <= tentativas:
            n += 1
            opcoesNome.append('Letra da capital')
            menu += ('{}. Letra da Capital - custa {} tentativas\n'.format(n,custo))
    if loja['Área']:
        custo = 6
        if custo <= tentativas:
            n += 1
            opcoesNome.append('Área')
            menu += ('{}. Área - custa {} tentativas\n'.format(n,custo))
    if loja['População']:
        custo = 5
        if custo <= tentativas:
            n += 1
            opcoesNome.append('População')
            menu += ('{}. População - custa {} tentativas\n'.format(n,custo))
    if loja['Continente']:
        custo = 7
        if custo <= tentativas:
            n += 1
            opcoesNome.append('Continente')
            menu += ('{}. Continente - custa {} tentativas\n'.format(n,custo))
    menu += ('0. Sem dica')
    print(menu)

    numeros = '0'
    i = 1
    while i <= n:
        numeros += '|{}'.format(i)
        i += 1

    opcao = int(input('Escolha sua opção [{}] '.format(numeros)))

    while opcao > n:
        print('Esse número não é válido')
        opcao = int(input('Escolha sua opção [{}]'.format(numeros)))

    if opcoesNome[opcao -1] == 'Cor da bandeira':
        tentativas -= 4
        cor = random.choice(loja['Cor da bandeira'])
        loja['Cor da bandeira'].remove(cor)
        dicas['Cor da bandeira'].append(cor)

    elif opcoesNome[opcao -1] == 'Letra da capital':
        tentativas -= 3
        letra = sorteia_letra(infosPais['capital'],loja['Letra da capital'])
        loja['Letra da capital'].append(letra)
    
    elif opcoesNome[opcao -1] == 'Área':
        tentativas -= 6
        loja['Área'] = False
        dicas['Área'] = infosPais['area']
    
    elif opcoesNome[opcao -1] == 'População':
        tentativas -= 5
        loja['População'] = False
        dicas['População'] = infosPais['populacao']
    
    elif opcoesNome[opcao -1] == 'Continente':
        tentativas -= 7
        loja['Continente'] = False
        dicas['Continente'] = infosPais['continente']
    
    return dicas

def exibe_infos(paisesTestados, tentativas, dicas):
    print("\nDistâncias:")
    for pais in paisesTestados:
        distancia = f"{int(pais[1]):,}".replace(',', '.')
        print(f"    {distancia} km -> {pais[0]}")
    print("\nDicas:")
    for dica, valor in dicas.items():
        print(f"    {dica}: {valor}")
    print(f"\nVocê tem {tentativas} tentativa (s)")