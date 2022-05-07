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
    opcoesNome = ['sem dica']

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

    lista_numeros = ['0']
    numeros = '0'
    i = 1
    while i <= n:
        numeros += '|{}'.format(i)
        lista_numeros.append(str(i))
        i += 1

    opcao = int(verifica(('Escolha sua opção [{}] '.format(numeros)),lista_numeros))

    if opcoesNome[opcao] == 'Cor da bandeira':
        tentativas -= 4
        cor = random.choice(loja['Cor da bandeira'])
        loja['Cor da bandeira'].remove(cor)
        if 'Cores da bandeira' not in dicas.keys():
            dicas['Cores da bandeira'] = []
        dicas['Cores da bandeira'].append(cor)

    elif opcoesNome[opcao] == 'Letra da capital':
        tentativas -= 3
        letra = sorteia_letra(infosPais['capital'],loja['Letra da capital'])
        loja['Letra da capital'].append(letra)
        if 'Letras da capital' not in dicas.keys():
            dicas['Letras da capital'] = []
        dicas['Letras da capital'].append(letra)
            
    elif opcoesNome[opcao] == 'Área':
        tentativas -= 6
        loja['Área'] = False
        dicas['Área'] = infosPais['area']
    
    elif opcoesNome[opcao] == 'População':
        tentativas -= 5
        loja['População'] = False
        dicas['População'] = infosPais['populacao']
    
    elif opcoesNome[opcao] == 'Continente':
        tentativas -= 7
        loja['Continente'] = False
        dicas['Continente'] = infosPais['continente']
    
    return dicas,tentativas,loja

def exibe_infos(paisesTestados, tentativas, dicas):
    print("\nDistâncias:")
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

        print(f"{cor}    {distancia2} km -> {pais[0]} {cores['reset']}")

    print("\nDicas:")
    for dica, valor in dicas.items():
        print(f"    {dica}: ", end='')
        if dica == 'Letras da capital' or dica == 'Cores da bandeira':
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
    return statusJogo
