import random, math

# Dicionario de cores que serão usadas no jogo
cores = {'ciano': '\x1b[1;36m', 'verde': '\x1b[1;32m', 'amarelo': '\x1b[1;33m', 'magenta': '\x1b[1;35m', 'vermelho': '\x1b[1;31m', 'reset': '\x1b[0m'}

def normaliza(porContinente): # reorganiza (normaliza) o dicionario de dados 
    porPais = {}
    for continente, paises in porContinente.items():
        for pais, info in paises.items():
            info['continente'] = continente
            porPais[pais] = info
    return porPais

def sorteia_pais(dados): # Sorteia um dos países da base de dados normalizada para ser adivinhado pelo jogador
    pais = random.choice(list(dados.keys()))
    return pais

def haversine(pais, paisTestado): # calcula a distância entre dois pontos considerando a curvatura da terra
    # Essa função foi adaptada da academia python para receber os dicionarios dos países em vez de suas respectivas latitudes e longitudes
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

def esta_na_lista(pais, lista): # Verifica se o país que está sendo testado nessa rodada já foi testado anteriormente
    paises = [item[0] for item in lista]
    if pais in paises:
        return True
    return False

def adiciona_em_ordem(pais, distancia, lista): # Recebe a lista de países que já foram testados e um novo país
    # Retorna uma nova lista com os países organizados por ordem crescente de distância
    nova_lista = list(lista)
    nova_tentativa = [pais, distancia]

    if not esta_na_lista(pais, lista):
        for i, item in enumerate(lista):
            if item[1] >= distancia:
                nova_lista.insert(i, nova_tentativa)
                return nova_lista
        nova_lista.append(nova_tentativa)
    return nova_lista

def sorteia_letra(palavra, restricao): # Sorteia uma letra da capital do país sorteado impondo restrições no sorteio
    restricao_caracteres = ['.', ',', '-', ';', ' '] + restricao # caracteres especiais e as letras que já foram sorteadas

    palavra_tratada = palavra.lower()
    for caracter in restricao_caracteres:
        palavra_tratada = palavra_tratada.replace(caracter, "")
    if len(palavra_tratada) < 1:
        return ""
    else:
        return random.choice(list(palavra_tratada))

def letras_validas_capital(capitalPais): # Determina quantas letras válidas há na capital
    restricao_caracteres = ['.', ',', '-', ';', ' '] # caracteres especiais que não devem ser considerados
    capitalPais_tratada = capitalPais.lower()
    for caracter in restricao_caracteres:
        capitalPais_tratada = capitalPais_tratada.replace(caracter, "")
    return len(capitalPais_tratada)

def verifica(pergunta, respostas): # Verifica a resposta do jogador e repete uma pergunta até que a resposta seja válida
    while True:
        jogada = (input(pergunta)).lower()
        if jogada in respostas:
            return jogada
        else:
            print('\nResposta inválida')


def exibe_infos(paisesTestados, tentativas, dicas): # exibe as informações principais do jogo
    print("\n" + "-"*43 + "\n - Distâncias:")
    for pais in paisesTestados: # percorre a lista de paises testados (que já está em ordem) para exibi-los
        distancia = int(pais[1])
        # define a cor de cada distância/país testado com base no quão afastado eles estão do país sorteado
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
        distancia2 = f"{int(pais[1]):,}".replace(',', '.') # padroniza a distância antes de mostra-la ao jogador
        print(f"    {cor}{distancia2: >4} km -> {pais[0]}{cores['reset']}")

    print("\n - Dicas:")
    for dica, valor in dicas.items(): # percorre o dicionário de dicas que o jogador tem para exibi-las
        print(f"    {dica}: ", end='')

        if dica == 'Letras da Capital' or dica == 'Cores da Bandeira': # padroniza a exibição das cores da bandeira e das letras da capital
            # retirando-as da lista e as colocando entre virgulas
            for subvalor in valor:
                if subvalor == valor[-1]:
                    print(subvalor)
                else:
                    print(subvalor, end=", ")

        elif dica == 'População': # padronizando a exibição do número de habitantes
            habitantes = f"{int(valor):,}".replace(',', '.') + " habitantes"
            print(habitantes)

        elif dica == 'Área': # padronizando a exibição da área do país
            area = f"{int(valor):,}".replace(',', '.') + " km"
            print(area)

        else: # se a dica n precisa de padronização, ela é apenas printada
            print(valor)
    print("-"*43)

    # define a cor do número de tentativas
    if tentativas <= 10:
        corTentativa = cores['amarelo']
    elif tentativas <= 5:
        corTentativa = cores['vermelho']
    else:
        corTentativa = cores['ciano']
    print(f"Você tem {corTentativa}{tentativas}{cores['reset']} tentativa (s)\n")
    
def montando_loja(infosPais): # Cria um dicionário com as dicas possíveis de serem compradas
    loja = {
        'Letra da Capital': [], # Letras da capital é uma lista vazia para que a função "sorteia_letra" da academia python n precise ser editada
        'Cor da Bandeira': [], # Lista  com as cores da bandeira que podem ser compradas
        'População': 1, # 1 = True (pode ser comprada)
        'Área': 1, # 1 = True (pode ser comprada)
        'Continente': 1, # 1 = True (pode ser comprada)
    }

    for cor, quantidade in infosPais['bandeira'].items(): # adiciona a lista todas as cores passíveis de serem sorteadas
        if quantidade > 0 and cor != "outras":
            loja['Cor da Bandeira'].append(cor)
    
    return loja

def menu_dicas(infosPais, loja, tentativas, dicas): # gera e controla o mercado de dicas
    opcoesNome = ['Sem dica']
    custo = {'Letra da Capital': 3, 'Cor da Bandeira': 4, 'População': 5, 'Área': 6, 'Continente': 7} # Dicionario que possui o custo de cada dica
    n = 0 # Essa variavel será usada para definir o número que cada dica terá
    # Esse número é alterado para que todas as dicas fiquem SEMPRE em ordem crescente
    
    print(f"\n - Mercado de Dicas\n" + "-"*43)
    for dica in loja.keys():
        if dica == 'Letra da Capital':
            if len(loja['Letra da Capital']) < letras_validas_capital(infosPais['capital']) and tentativas > 3: 
                # verifica se o jogador ainda pode comprar essa dica (caso especial)
                n += 1 # coloca as dicas em ordem crescente
                opcoesNome.append('Letra da Capital') # associa a dica ao seu número
                print(f'{n}. {dica: <20}- custa {custo[dica]} tentativas')

        elif dica == 'Cor da Bandeira':
            if len(loja['Cor da Bandeira']) > 0 and tentativas > 4: 
                # verifica se o jogador ainda pode comprar essa dica (caso especial)
                n += 1 # coloca as dicas em ordem crescente
                opcoesNome.append('Cor da Bandeira')
                print(f'{n}. {dica: <20}- custa {custo[dica]} tentativas')

        else:
            if loja[dica] > 0 and tentativas > custo[dica]: 
                # verifica se o jogador ainda pode comprar cada uma das dicas antes de exibi-las junto de seus custos
                n += 1 # coloca as dicas em ordem crescente
                opcoesNome.append(dica) # associa a dica ao seu número
                print(f'{n}. {dica: <20}- custa {custo[dica]} tentativas')
    print('0. Sem dica\n' + "-"*43)

    listaNumeros = ['0'] # Lista de números validos que podem ser usados na compra de dicas
    numeros = '0' # String com os números que podem ser usados na compra de dicas
    i = 1
    while i <= n:
        numeros += '|{}'.format(i)
        listaNumeros.append(str(i))
        i += 1

    opcao = int(verifica((f'Escolha sua opção [{numeros}] '), listaNumeros)) # recolhe a dica que o usuario quer comprar (verificando-a antes) 

    if opcoesNome[opcao] != 'Sem dica':
        tentativas -= custo[opcoesNome[opcao]]

        if opcoesNome[opcao] == 'Letra da Capital': # caso especial
            letra = sorteia_letra(infosPais['capital'],loja['Letra da Capital']) # Sorteia uma letra da capital
            loja['Letra da Capital'].append(letra)
            if 'Letras da Capital' not in dicas.keys():
                dicas['Letras da Capital'] = []
            dicas['Letras da Capital'].append(letra) # adiciona a letra sorteada a lista de letras do jogador
            
        elif opcoesNome[opcao] == 'Cor da Bandeira': # caso especial
            cor = random.choice(loja['Cor da Bandeira']) # sorteia uma cor da bandeira
            loja['Cor da Bandeira'].remove(cor)
            if 'Cores da Bandeira' not in dicas.keys():
                dicas['Cores da Bandeira'] = []
            dicas['Cores da Bandeira'].append(cor) # adiciona a cor sorteada a lista de cores da bandeira do jogador

        else: # casos genéricos
            loja[opcoesNome[opcao]] = 0 # uma vez comprada essa dica n pode ser comprada novamente 
            dicas[opcoesNome[opcao]] = infosPais[opcoesNome[opcao].lower()] # recolhe o valor da dica dos dados e o adiciona a lista de dicas do jogador
    
    return dicas, tentativas, loja

def desistencia(pais, statusJogando): # verifica se o jogador quer mesmo desistir, se "sim" acaba a partida
    desistir = verifica("Tem certeza que deseja desistir da rodada? [s|n] ",['s','n'])
    statusJogando = (desistir == 'n')
    if not statusJogando:
        print(f"Que deselegante desistir, o país era: {pais}")
    return statusJogando

def fim(tentativas,jogada,pais): # verifica se o jogador ganhou ou perdeu e finaliza a partida
    if tentativas == 0 and jogada != pais:
        print(f'Você perdeu :(\nO país era {pais}')
    elif tentativas >= 0 and jogada == pais:
        print('Você venceu! :)')
    return False

def reiniciar(): # pergunta se o jogador quer jogar novamente
    reiniciar = verifica('Você quer jogar novamente? [s/n] ',['s','n'])
    statusJogo = (reiniciar == 's')
    if not statusJogo:
        print('\nAté a próxima!')
    return statusJogo # se "True" o jogo recomeça, se "False" o jogo termina
