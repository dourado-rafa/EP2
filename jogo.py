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

    loja = montando_loja(pais, infosPais)

    while tentativas > 0 and statusJogando:
        jogada = input('Qual seu palpite? ').lower()
        if jogada == 'dica':
            input("W.I.P.")
                
        else:
            if jogada in dadosPaises.keys():
                tentativas -= 1
                paisTestado = dadosPaises[jogada]

                if jogada == pais:
                    print('Você venceu')
                    statusJogando = False
                    reiniciar = input('Você quer jogar novamente? ')
                    if reiniciar == 'sim':
                        statusJogo = True
                    else:
                        statusJogo = False
                else:
                    input("W.I.P.")
                    distancia = haversine(infosPais, paisTestado)
                    adiciona_em_ordem(jogada, distancia, paisesTestados)
            else:
                print('País desconhecido')
                