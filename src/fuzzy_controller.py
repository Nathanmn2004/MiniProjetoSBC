from skfuzzy import control as ctrl
from variables import criar_variaveis
from rules import criar_regras


def classificar_risco(valor):
    if valor < 40:
        return "Baixo"
    elif valor < 70:
        return "Médio"
    else:
        return "Alto"


def calcular_risco_nocaute(valor_dano, valor_fadiga):
    dano, fadiga, risco = criar_variaveis()
    regras = criar_regras(dano, fadiga, risco)

    sistema_controle = ctrl.ControlSystem(regras)
    simulador = ctrl.ControlSystemSimulation(sistema_controle)

    simulador.input['dano'] = valor_dano
    simulador.input['fadiga'] = valor_fadiga

    simulador.compute()

    resultado = simulador.output['risco']
    classificacao = classificar_risco(resultado)

    return resultado, classificacao