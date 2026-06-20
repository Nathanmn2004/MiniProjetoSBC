from skfuzzy import control as ctrl

from rules import criar_regras
from variables import criar_variaveis


def classificar_risco(valor):
    if valor < 35:
        return "Baixo"
    if valor < 68:
        return "Medio"

    return "Alto"


def calcular_risco_nocaute(valor_dano, valor_fadiga):
    dano, fadiga, risco = criar_variaveis()
    regras = criar_regras(dano, fadiga, risco)

    sistema_controle = ctrl.ControlSystem(regras)
    simulador = ctrl.ControlSystemSimulation(sistema_controle)

    simulador.input["dano"] = valor_dano
    simulador.input["fadiga"] = valor_fadiga

    simulador.compute()

    resultado = simulador.output["risco"]
    classificacao = classificar_risco(resultado)

    return resultado, classificacao
