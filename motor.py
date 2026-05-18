"""
motor.py — Função auxiliar para executar o motor e imprimir o trace.

Uso:
    from motor import executar_caso
    executar_caso("Meu caso", sintomas=["febre", "tosse"], exames=[("oximetria","baixa")])
"""

from fatos import Sintoma, Exame, HistoricoMedico, Diagnostico
from regras import DiagnosticoRespiratorio


def executar_caso(nome_caso, sintomas=None, exames=None, historico=None):
    """
    Instancia o motor, declara os fatos fornecidos e executa o ciclo de inferência.
    Imprime um trace completo de cada etapa e exibe os diagnósticos ao final.

    Args:
        nome_caso (str)          – rótulo descritivo para o caso
        sintomas  (list[str])    – nomes dos sintomas (ex: ["febre", "tosse"])
        exames    (list[tuple])  – pares (tipo, valor) (ex: [("oximetria", "baixa")])
        historico (list[str])    – condições do histórico (ex: ["asma"])
    """
    sintomas  = sintomas  or []
    exames    = exames    or []
    historico = historico or []

    print("\n" + "═" * 60)
    print(f"  CASO: {nome_caso}")
    print("═" * 60)

    # ── 1. Instanciar e limpar o motor ───────────────────────────────
    engine = DiagnosticoRespiratorio()
    engine.reset()
    print("  [MOTOR] reset() — memória de trabalho limpa\n")

    # ── 2. Declarar fatos de entrada ─────────────────────────────────
    for nome in sintomas:
        engine.declare(Sintoma(nome=nome))
        print(f"  [FATO +] Sintoma(nome='{nome}')")

    for tipo, valor in exames:
        engine.declare(Exame(tipo=tipo, valor=valor))
        print(f"  [FATO +] Exame(tipo='{tipo}', valor='{valor}')")

    for cond in historico:
        engine.declare(HistoricoMedico(condicao=cond))
        print(f"  [FATO +] HistoricoMedico(condicao='{cond}')")

    # ── 3. Executar inferência ────────────────────────────────────────
    print("\n  [MOTOR] run() — iniciando ciclo de inferência...\n")
    engine.run()

    # ── 4. Coletar e exibir diagnósticos ─────────────────────────────
    diagnosticos = [
        f for f in engine.facts.values()
        if isinstance(f, Diagnostico)
    ]

    print("\n" + "─" * 60)
    print("  RESULTADO FINAL:")
    if diagnosticos:
        for d in diagnosticos:
            print(f"  ✔  Doença   : {d['doenca']}")
            print(f"     Confiança: {d['confianca']}")
            print(f"     Conduta  : {d['conduta']}")
    else:
        print("  Nenhum diagnóstico inferido com os fatos fornecidos.")
    print("─" * 60)

    return diagnosticos