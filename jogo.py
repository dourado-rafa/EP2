from funcoes import *
from dados import *

dadosPaises = normaliza(DADOS)
statusJogo = True

while statusJogo: 
    pais = sorteia_pais(dadosPaises)
    tentativas = 20
    paisesTestados = []
    statusJogando = True

    while tentativas > 0 and statusJogando:
        jogada = input('Quer tentar acertar o país ou comprar dica?')
        if jogada == 'tentar pais':
            tentativas -= 1
            paisTeste = input('Digite o nome de um país:')
            if paisTeste == pais:
                print('você venceu')
                statusJogando = False
                reiniciar = input('Você quer jogar novamente?')
                if reiniciar == 'sim':
                    statusJogo = True
                else:
                    statusJogo = False
            else:
                print('país incorreto')
                
        elif jogada == 'comprar dica':
            tipo = input('Escolha uma categoria')



                
