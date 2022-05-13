from funcoes import *
from dados import *
import os

# Começa normalizando a base de dados por país
dadosPaises = normaliza(DADOS)

# "Tela inicial" do jogo
os.system('cls')
print(f""" ============================ 
|                            |
| Bem-vindo ao Insper Países |
|                            |
 ==== Design de Software ==== """)


statusJogo = True
while statusJogo: 
# É o looping do jogo, o statusJogo só passa a ser False se o jogador finalizar a rodada e não quiser jogar novamente.
    print(f"""\n - Comandos:
    dica       - entra no mercado de dicas
    desisto    - desiste da rodada
    inventario - exibe sua posição

Um país foi escolhido, tente adivinhar!\n
Você tem {cores['ciano']}20{cores['reset']} tentativa(s)""")

    pais = sorteia_pais(dadosPaises) 
    infosPais = dadosPaises[pais]

    tentativas = 20
    paisesTestados = []
    statusJogando = True

    loja = montando_loja(infosPais)
    # A função loja é utilizada para saber quais dicas o usuário nao pode mais pedir por não ter mais informações disponíveis sobre aquela categoria.
    # Não analisa o que o usuário pode pedir de acordo com o número de tentativas que ele pode gastar

    dicas = {} 
    # O dicionário dica guarda as informações já obtidas pelo usuário
    # São as informações printadas após o usuário pedir uma nova dica

    while (tentativas > 0 and statusJogando):
    # É o looping da rodada, o usuário só sai do looping se perder o jogo por não ter mais tentativas ou desistir da rodada
        jogada = input('Qual seu palpite? ').lower()

        if jogada in ['dica', 'dicas']:
            dicas, tentativas, loja = menu_dicas(infosPais, loja, tentativas, dicas)
        # A função menu_dicas printa as opções de dica que o usuário pode pedir de acordo com as informações disponíveis (loja) e com o número de tentativas.
        # Após o jogador escolher a dica desejada as tentativas, informações disponíveis e informações obtidas pelo usuário são atualizadas.
            exibe_infos(paisesTestados, tentativas, dicas)
        # exibe as informações obtidas pelo usuário após a jogada, paises testados e suas distâncias ao país sorteado, 
        # numero de tentativas e informações obtidas sobre o pais sorteado.

        elif jogada == 'desisto':
            statusJogando = desistencia(pais,statusJogando)
        # a função desistência confirma se o usuário realmente deseja desistir e finaliza a rodada caso sim.

        elif jogada == 'inventario':
            exibe_infos(paisesTestados, tentativas, dicas)
        
        elif esta_na_lista(jogada, paisesTestados):
            print("Você já testou esse país!\n")

        elif jogada in dadosPaises.keys():
            paisTestado = dadosPaises[jogada]
            tentativas -= 1

            if tentativas == 0 or jogada == pais:
                statusJogando = fim(tentativas,jogada,pais)

            else:
                distancia = haversine(infosPais, paisTestado)
                paisesTestados = adiciona_em_ordem(jogada, distancia, paisesTestados)
                exibe_infos(paisesTestados, tentativas, dicas)
        
        else:
            print('País desconhecido!\n')

    statusJogo = reiniciar()
                