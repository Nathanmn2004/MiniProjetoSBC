"""
testes.py — Os 3 casos de teste do sistema.

Cada função de teste chama executar_caso() com um conjunto específico de fatos
e documenta o encadeamento esperado em seu docstring.
"""

from motor import executar_caso


def caso_gripe():
    """
    Caso 1 – Gripe com febre alta.

    Encadeamento esperado (3 níveis):
      Nível 1: febre + tosse + dor_muscular + febre_alta
      Nível 2: R01 infere SindromeGripal
      Nível 3: R05 infere Gripe (Influenza)

    Resolução de conflito: R06 (resfriado) NÃO dispara porque febre está presente.
    """
    executar_caso(
        nome_caso="Caso 1 – Gripe com Febre Alta",
        sintomas=["febre", "tosse", "dor_muscular", "febre_alta"],
    )


def caso_resfriado():
    """
    Caso 2 – Resfriado comum (demonstra NOT).

    Encadeamento esperado:
      Nível 1: tosse + coriza   (febre AUSENTE)
      Nível 3: R06 dispara diretamente via NOT(Sintoma(nome='febre'))

    Resolução de conflito: NOT(febre) diferencia resfriado de gripe.
    Se 'febre' fosse adicionado, R06 não dispararia.
    """
    executar_caso(
        nome_caso="Caso 2 – Resfriado Comum (NOT febre)",
        sintomas=["tosse", "coriza"],
    )


def caso_hipoxemia():
    """
    Caso 3 – Pneumonia grave com hipoxemia (máxima prioridade).

    Encadeamento esperado (3 níveis completos):
      Nível 1: febre + tosse + dor_muscular + falta_de_ar + Exame(oximetria, baixa)
      Nível 2: R01 → SindromeGripal  |  R03 → AlertaOxigenio
      Nível 3: R09 (salience=20) → Hipoxemia + Pneumonia Grave

    Resolução de conflito:
      - R09 (salience=20) tem precedência sobre R07 (salience=9).
      - NOT(AlertaOxigenio()) em R07 garante que Pneumonia simples NÃO seja
        inferida simultaneamente com Hipoxemia grave.
    """
    executar_caso(
        nome_caso="Caso 3 – Pneumonia Grave com Hipoxemia",
        sintomas=["febre", "tosse", "dor_muscular", "falta_de_ar"],
        exames=[("oximetria", "baixa")],
    )


def caso_dor():
    """
    Caso 3 – Pneumonia grave com hipoxemia (máxima prioridade).

    Encadeamento esperado (3 níveis completos):
      Nível 1: febre + tosse + dor_muscular + falta_de_ar + Exame(oximetria, baixa)
      Nível 2: R01 → SindromeGripal  |  R03 → AlertaOxigenio
      Nível 3: R09 (salience=20) → Hipoxemia + Pneumonia Grave

    Resolução de conflito:
      - R09 (salience=20) tem precedência sobre R07 (salience=9).
      - NOT(AlertaOxigenio()) em R07 garante que Pneumonia simples NÃO seja
        inferida simultaneamente com Hipoxemia grave.
    """
    executar_caso(
        nome_caso="Caso 4 - Dor geral",
        sintomas=["dor_muscular", "tosse",],
        exames=[("oximetria", "baixa")],
    )

# Permite rodar os testes diretamente: python testes.py
if __name__ == "__main__":
    caso_gripe()
    caso_resfriado()
    caso_hipoxemia()