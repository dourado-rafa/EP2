from funcoes import *
from dados import *

dadosPaises = normaliza(DADOS)
statusJogo = True

print(f"""
 ============================ 
|                            |
| Bem-vindo ao Insper Países |
|                            |
 ==== Design de Software ==== 

 Comandos:
    dica       - entra no mercado de dicas
    desisto    - desiste da rodada
    inventario - exibe sua posição

Um país foi escolhido, tente adivinhar!
Você tem {cores['ciano']}20{cores['reset']} tentativa(s)""")

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
            statusJogando = desistencia(pais,statusJogando)

        elif jogada == 'inventario':
            exibe_infos(paisesTestados, tentativas, dicas)
        
        elif jogada in [paisTestado[0] for paisTestado in paisesTestados]:
            print("Você já testou esse país")

        elif jogada in dadosPaises.keys():
            paisTestado = dadosPaises[jogada]
            tentativas -= 1

            if tentativas == 0:
                statusJogando = fim((tentativas,jogada,pais))

            elif jogada == pais:
                print('Você venceu')
                statusJogando = False

            else:
                distancia = haversine(infosPais, paisTestado)
                paisesTestados = adiciona_em_ordem(jogada, distancia, paisesTestados)
                exibe_infos(paisesTestados, tentativas, dicas)
        
        else:
            print('País desconhecido')

    statusJogo = reiniciar()
                