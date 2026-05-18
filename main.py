"""
main.py — Ponto de entrada do SBC de Diagnóstico Respiratório.
 
Executa os 3 casos de teste padrão ou aceita sintomas via linha de comando.
 
Uso:
    python main.py                          # roda os 3 casos de teste
    python main.py febre tosse dor_muscular # caso personalizado via CLI
"""

import sys
from motor import executar_caso
from testes import caso_gripe, caso_resfriado, caso_hipoxemia, caso_dor

def main():
    # ── Modo CLI: sintomas passados como argumentos ──────────────────
    if len(sys.argv) > 1:
        sintomas = sys.argv[1:]
        print(f"\nModo CLI — sintomas recebidos: {sintomas}")
        executar_caso(
            nome_caso="Caso personalizado (CLI)",
            sintomas=sintomas,
        )
        return
 
    # ── Modo padrão: executa os 3 casos de teste ─────────────────────
    print("=" * 60)
    print("  SBC — Diagnóstico de Doenças Respiratórias")
    print("  Biblioteca: experta (Python)")
    print("=" * 60)
 
    caso_gripe()
    caso_resfriado()
    caso_hipoxemia()
    caso_dor()
 
    print("\nTodos os casos executados.")
 
 
if __name__ == "__main__":
    main()