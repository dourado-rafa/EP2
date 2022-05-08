from cgitb import reset
import random, math

cores = {'ciano': '\x1b[1;36m', 'verde': '\x1b[1;32m', 'amarelo': '\x1b[1;33m', 'magenta': '\x1b[1;35m', 'vermelho': '\x1b[1;31m', 'reset': '\x1b[0m'}

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
    loja = {
        'Letra da Capital': [],
        'Cor da Bandeira': [],
        'População': 1,
        'Área': 1,
        'Continente': 1,
    }

    for cor, quantidade in infosPais['bandeira'].items():
        if quantidade > 0 and cor != "outras":
            loja['Cor da Bandeira'].append(cor)
    
    return loja

def menu_dicas(infosPais, loja, tentativas, dicas):
    opcoesNome = ['Sem dica']
    custo = {'Letra da Capital': 3, 'Cor da Bandeira': 4, 'População': 5, 'Área': 6, 'Continente': 7}
    n = 0
    
    print(f"\n - Mercado de Dicas\n" + "-"*43)
    for dica in loja.keys():
        if dica == 'Letra da Capital':
            if len(loja['Letra da Capital']) < len(infosPais['capital']):
                if tentativas > 3:
                    n += 1
                    opcoesNome.append('Letra da Capital')
                    print(f'1. {"Letra da Capital": <20}- custa 3 tentativas')

        elif dica == 'Cor da Bandeira':
            if len(loja['Cor da Bandeira']) > 0:
                if tentativas > 4:
                    n += 1
                    opcoesNome.append('Cor da Bandeira')
                    print(f'2. {"Cor da Bandeira": <20}- custa 4 tentativas')

        else:
            if loja[dica] > 0:
                if tentativas > custo[dica]:
                    n += 1
                    opcoesNome.append(dica)
                    print(f'{n}. {dica: <20}- custa {custo[dica]} tentativas')
    print('0. Sem dica\n' + "-"*43)

    lista_numeros = ['0']
    numeros = '0'
    i = 1
    while i <= n:
        numeros += '|{}'.format(i)
        lista_numeros.append(str(i))
        i += 1

    opcao = int(verifica(('Escolha sua opção [{}] '.format(numeros)),lista_numeros))

    if opcoesNome[opcao] != 'Sem dica':
        tentativas -= custo[opcoesNome[opcao]]

        if opcoesNome[opcao] == 'Letra da Capital':
            letra = sorteia_letra(infosPais['capital'],loja['Letra da Capital'])
            loja['Letra da Capital'].append(letra)
            if 'Letras da Capital' not in dicas.keys():
                dicas['Letras da Capital'] = []
            dicas['Letras da Capital'].append(letra)
            
        elif opcoesNome[opcao] == 'Cor da Bandeira':
            cor = random.choice(loja['Cor da Bandeira'])
            loja['Cor da Bandeira'].remove(cor)
            if 'Cores da Bandeira' not in dicas.keys():
                dicas['Cores da Bandeira'] = []
            dicas['Cores da Bandeira'].append(cor)

        else:
            loja[opcoesNome[opcao]] = 0
            dicas[opcoesNome[opcao]] = infosPais[opcoesNome[opcao].lower()]
    
    return dicas,tentativas,loja

def exibe_infos(paisesTestados, tentativas, dicas):
    print("\n - Distâncias:")
    for pais in paisesTestados:
        distancia = int(pais[1])
        if distancia <= 1000:
            cor = cores['ciano']
        elif distancia <= 2000:
            cor = cores['verde']
        elif distancia <= 5000:
            cor = cores['amarelo']
        elif distancia <= 10000:
            cor = cores['magenta']
        else:
            cor = cores['vermelho']
        distancia2 = f"{int(pais[1]):,}".replace(',', '.')

        print(f"{cor}    {distancia2: >4} km -> {pais[0]} {cores['reset']}")

    print("\n - Dicas:")
    for dica, valor in dicas.items():
        print(f"    {dica}: ", end='')
        if dica == 'Letras da Capital' or dica == 'Cores da Bandeira':
            for subvalor in valor:
                if subvalor == valor[-1]:
                    print(subvalor)
                else:
                    print(subvalor, end=", ")
        else:
            print(valor)

    if tentativas <= 10:
        corTentativa = cores['amarelo']
    elif tentativas <= 5:
        corTentativa = cores['vermelho']
    else:
        corTentativa = cores['ciano']

    print(f"\nVocê tem {corTentativa}{tentativas}{cores['reset']} tentativa (s)")

def verifica(pergunta,respostas):
    jogada = (input(pergunta)).lower()

    while jogada:
        if jogada in respostas:
            return jogada
        else:
            print('Resposta inválida')
            jogada = (input(pergunta)).lower()

def desistencia(pais,statusJogando):
    desistir = verifica("Tem certeza que deseja desistir da rodada? [s|n] ",['s','n'])
    statusJogando = (desistir == 'n')
    if not statusJogando:
        print(f"Que deselegante desistir, o país era: {pais}")
    return statusJogando

def fim(tentativas,jogada,pais):
    if tentativas == 0 and jogada != pais:
        print('Você perdeu :(')
    elif tentativas == 0 and jogada == pais:
        print('Você venceu!')
    return False

def reiniciar():
    reiniciar = verifica('Você quer jogar novamente? [s/n]',['s','n'])
    statusJogo = (reiniciar == 's')
    if not statusJogo:
        print('Até a próxima!')
    return statusJogo
