from funcoes import *
from dados import *

dadosPaises = normaliza(DADOS)
statusJogo = True

while statusJogo: 
    pais = sorteia_pais(dadosPaises)
    infosPais = dadosPaises[pais]

    tentativas = 20
    paisesTestados = []
    statusJogando = True

    loja = montando_loja(infosPais)
    dicas = {}

    while (tentativas > 0 and statusJogando):
        jogada = input('Qual seu palpite? ').lower()

        if jogada == 'dica':
            dicas, tentativas, loja = menu_dicas(infosPais, loja, tentativas, dicas)
            exibe_infos(paisesTestados, tentativas, dicas)

        elif jogada == 'desisto':
            desistir = input("Tem certeza que deseja desistir da rodada? [s|n] ")
            statusJogando = (desistir == 'n')

        elif jogada == 'inventario':
            exibe_infos(paisesTestados, tentativas, dicas)

        elif jogada in dadosPaises.keys():
            paisTestado = dadosPaises[jogada]
            tentativas -= 1

            if jogada == pais:
                print('Você venceu')
                statusJogando = False
                reiniciar = input('Você quer jogar novamente? [s|n] ')
                statusJogo = (reiniciar == 's')

            else:
                distancia = haversine(infosPais, paisTestado)
                paisesTestados = adiciona_em_ordem(jogada, distancia, paisesTestados)
                exibe_infos(paisesTestados, tentativas, dicas)
        
        else:
            print('País desconhecido')
            
                