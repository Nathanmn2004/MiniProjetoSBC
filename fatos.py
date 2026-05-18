"""
fatos.py — Definição de todos os Fatos do SBC.

Nível 1 (entrada): Sintoma, Exame, HistoricoMedico
Nível 2 (intermediário): SindromeGripal, SindromeObstrutiva, AlertaOxigenio
Nível 3 (saída): Diagnostico
"""

from experta import Fact


# ── Nível 1: fatos de entrada (declarados pelo usuário) ──────────────

class Sintoma(Fact):
    """Sintoma relatado pelo paciente.
    Slot:
      nome (str) – 'febre' | 'tosse' | 'falta_de_ar' | 'coriza' |
                   'dor_muscular' | 'chiado' | 'febre_alta'
    """
    pass


class Exame(Fact):
    """Resultado de exame clínico.
    Slots:
      tipo  (str) – 'oximetria' | 'ausculta'
      valor (str) – 'baixa'     | 'sibilos'
    """
    pass


class HistoricoMedico(Fact):
    """Condição prévia relevante do paciente.
    Slot:
      condicao (str) – 'asma' | 'dpoc' | 'imunocomprometido'
    """
    pass


# ── Nível 2: fatos intermediários (inferidos pelo motor) ─────────────

class SindromeGripal(Fact):
    """Padrão gripal detectado (febre + tosse + dor muscular)."""
    pass


class SindromeObstrutiva(Fact):
    """Padrão obstrutivo detectado (chiado + falta de ar)."""
    pass


class AlertaOxigenio(Fact):
    """Comprometimento de oxigenação detectado (oximetria baixa + falta de ar)."""
    pass


# ── Nível 3: fato de saída (diagnóstico final) ───────────────────────

class Diagnostico(Fact):
    """Hipótese diagnóstica gerada pelo sistema.
    Slots:
      doenca    (str) – nome da doença inferida
      confianca (str) – 'baixa' | 'média' | 'alta' | 'crítica'
      conduta   (str) – orientação clínica sugerida
    """
    pass