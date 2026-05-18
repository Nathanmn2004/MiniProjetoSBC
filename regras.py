"""
regras.py — Motor de inferência SEM uso de decorator @Rule.

As regras são registradas explicitamente com a sintaxe:
    nome_metodo = Rule(condicoes...)(nome_metodo)

Isso é exatamente o que o @ faz por baixo dos panos.

Encadeamento em 3 níveis:
  Nível 1 → 2 : R01, R02, R03, R04  (sintomas → síndromes intermediárias)
  Nível 2 → 3 : R05, R06, R07, R08, R09, R10  (síndromes → diagnóstico final)

Resolução de conflito:
  salience : regras críticas disparam antes das comuns (R09 > R08 > R10 > R05/R07 > R06 > R01-R04)
  NOT      : diferencia resfriado de gripe e evita diagnósticos duplicados
"""

from experta import KnowledgeEngine, Rule, NOT

from fatos import (
    Sintoma, Exame, HistoricoMedico,
    SindromeGripal, SindromeObstrutiva, AlertaOxigenio,
    Diagnostico,
)


class DiagnosticoRespiratorio(KnowledgeEngine):

    # ════════════════════════════════════════════
    # NÍVEL 1 → NÍVEL 2  (fatos intermediários)
    # ════════════════════════════════════════════

    # R01 – IF febre AND tosse AND dor_muscular THEN SindromeGripal
    def r01_sindrome_gripal(self):
        self.declare(SindromeGripal())
        print("[R01] febre + tosse + dor_muscular → SindromeGripal inferida")

    r01_sindrome_gripal = Rule(
        Sintoma(nome="febre"),
        Sintoma(nome="tosse"),
        Sintoma(nome="dor_muscular"),
        salience=5,
    )(r01_sindrome_gripal)

    # R02 – IF chiado AND falta_de_ar THEN SindromeObstrutiva
    def r02_sindrome_obstrutiva(self):
        self.declare(SindromeObstrutiva())
        print("[R02] chiado + falta_de_ar → SindromeObstrutiva inferida")

    r02_sindrome_obstrutiva = Rule(
        Sintoma(nome="chiado"),
        Sintoma(nome="falta_de_ar"),
        salience=5,
    )(r02_sindrome_obstrutiva)

    # R03 – IF oximetria_baixa AND falta_de_ar THEN AlertaOxigenio
    def r03_alerta_oxigenio(self):
        self.declare(AlertaOxigenio())
        print("[R03] oximetria baixa + falta_de_ar → AlertaOxigenio inferido")

    r03_alerta_oxigenio = Rule(
        Exame(tipo="oximetria", valor="baixa"),
        Sintoma(nome="falta_de_ar"),
        salience=6,
    )(r03_alerta_oxigenio)

    # R04 – IF sibilos AND historico_asma AND NOT SindromeObstrutiva THEN SindromeObstrutiva
    def r04_obstrutiva_por_ausculta(self):
        self.declare(SindromeObstrutiva())
        print("[R04] sibilos + histórico de asma → SindromeObstrutiva inferida (ausculta)")

    r04_obstrutiva_por_ausculta = Rule(
        Exame(tipo="ausculta", valor="sibilos"),
        HistoricoMedico(condicao="asma"),
        NOT(SindromeObstrutiva()),
        salience=5,
    )(r04_obstrutiva_por_ausculta)

    # ════════════════════════════════════════════
    # NÍVEL 2 → NÍVEL 3  (diagnóstico final)
    # ════════════════════════════════════════════

    # R05 – IF SindromeGripal AND febre_alta THEN Gripe
    def r05_gripe(self):
        self.declare(Diagnostico(
            doenca="Gripe (Influenza)",
            confianca="alta",
            conduta="Repouso, hidratação, considerar oseltamivir se < 48h de sintomas.",
        ))
        print("[R05] SindromeGripal + febre_alta → Diagnóstico: Gripe (Influenza)")

    r05_gripe = Rule(
        SindromeGripal(),
        Sintoma(nome="febre_alta"),
        salience=9,
    )(r05_gripe)

    # R06 – IF tosse AND coriza AND NOT febre THEN Resfriado
    def r06_resfriado(self):
        self.declare(Diagnostico(
            doenca="Resfriado Comum (Rinovírus)",
            confianca="média",
            conduta="Sintomáticos, hidratação e repouso. Sem necessidade de antibiótico.",
        ))
        print("[R06] tosse + coriza + NOT febre → Diagnóstico: Resfriado Comum")

    r06_resfriado = Rule(
        Sintoma(nome="tosse"),
        Sintoma(nome="coriza"),
        NOT(Sintoma(nome="febre")),
        salience=7,
    )(r06_resfriado)

    # R07 – IF SindromeGripal AND falta_de_ar AND NOT AlertaOxigenio THEN Pneumonia
    def r07_pneumonia(self):
        self.declare(Diagnostico(
            doenca="Pneumonia Bacteriana",
            confianca="alta",
            conduta="Solicitar RX tórax. Iniciar antibioticoterapia empírica.",
        ))
        print("[R07] SindromeGripal + falta_de_ar + NOT AlertaOxigenio → Diagnóstico: Pneumonia")

    r07_pneumonia = Rule(
        SindromeGripal(),
        Sintoma(nome="falta_de_ar"),
        NOT(AlertaOxigenio()),
        salience=9,
    )(r07_pneumonia)

    # R08 – IF SindromeObstrutiva AND historico_asma THEN CriseAsmatica  [salience=15]
    def r08_crise_asmatica(self):
        self.declare(Diagnostico(
            doenca="Crise Asmática",
            confianca="crítica",
            conduta="Beta-2 agonista inalatório imediato. Monitorar SpO2. Acionar médico.",
        ))
        print("[R08] (salience=15) SindromeObstrutiva + asma → Diagnóstico: Crise Asmática")

    r08_crise_asmatica = Rule(
        SindromeObstrutiva(),
        HistoricoMedico(condicao="asma"),
        salience=15,
    )(r08_crise_asmatica)

    # R09 – IF AlertaOxigenio AND SindromeGripal THEN HipoxemiaGrave  [salience=20]
    def r09_hipoxemia_grave(self):
        self.declare(Diagnostico(
            doenca="Hipoxemia + Pneumonia Grave",
            confianca="crítica",
            conduta="ENCAMINHAR URGÊNCIA. Suporte de O2, internação imediata.",
        ))
        print("[R09] (salience=20) AlertaOxigenio + SindromeGripal → Pneumonia Grave c/ Hipoxemia")

    r09_hipoxemia_grave = Rule(
        AlertaOxigenio(),
        SindromeGripal(),
        salience=20,
    )(r09_hipoxemia_grave)

    # R10 – IF SindromeObstrutiva AND historico_dpoc THEN ExacerbacaoDPOC
    def r10_dpoc_exacerbado(self):
        self.declare(Diagnostico(
            doenca="Exacerbação de DPOC",
            confianca="alta",
            conduta="Broncodilatador, corticoide sistêmico, considerar antibiótico se escarro purulento.",
        ))
        print("[R10] SindromeObstrutiva + DPOC → Diagnóstico: Exacerbação de DPOC")

    r10_dpoc_exacerbado = Rule(
        SindromeObstrutiva(),
        HistoricoMedico(condicao="dpoc"),
        salience=12,
    )(r10_dpoc_exacerbado)