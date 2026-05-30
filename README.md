# SBC – Diagnóstico de Doenças Respiratórias

> Sistema Baseado em Conhecimento implementado com **experta** (Python).  

- Nathan Meira Nóbrega
- Miguel Lisboa

---

## Estrutura do repositório

```
sbc_respiratorio/
├── fatos.py    — classes Fact: Sintoma, Exame, HistoricoMedico, Diagnostico e intermediários
├── regras.py   — KnowledgeEngine com as 10 regras IF-THEN
├── motor.py    — função executar_caso() com trace completo
├── testes.py   — 3 funções de teste (caso_gripe, caso_resfriado, caso_hipoxemia)
└── main.py     — ponto de entrada; roda os testes ou aceita sintomas via CLI
```

---

## Descrição do domínio

O sistema realiza **triagem clínica de condições respiratórias** com base em sintomas relatados pelo paciente, resultados de exames e histórico médico. O objetivo é apoiar profissionais de saúde na identificação de hipóteses diagnósticas (gripe, resfriado, pneumonia, asma, DPOC) e sugerir condutas clínicas iniciais.

O motor utiliza **encadeamento para frente** (*forward chaining*): a partir dos fatos inseridos (sintomas e exames), o sistema infere fatos intermediários e, a partir deles, produz o diagnóstico final.

---

## Mapeamento dos Componentes do SBC

Este projeto foi construído respeitando rigorosamente a divisão clássica de um Sistema Baseado em Conhecimento (SBC):

1. **Motor de Inferência (Inference Engine)**
   * **Onde está no código:** É o próprio framework **experta**
   * **Função:** Implementa o algoritmo **Rete** para realizar o *pattern matching* (casamento de padrões) eficiente entre os fatos e as regras, gerencia a agenda ativa de regras (resolvendo conflitos através de propriedades como `salience` e `NOT`), e executa o ciclo de inferência em **encadeamento para frente** (*forward chaining*).

2. **Base de Conhecimento (Knowledge Base)**
   * **Onde está no código:** No arquivo [regras.py]
   * **Função:** Define a classe [DiagnosticoRespiratorio] (que herda de `KnowledgeEngine`), onde residem as **10 regras de produção (regras IF-THEN)** declaradas explicitamente com a sintaxe `Rule(...)(função)`. Esta base de conhecimento codifica a expertise clínica do domínio.

3. **Memória de Trabalho (Working Memory)**
   * **Onde está no código:** Representada pela agenda dinâmica de fatos mantida em tempo de execução pela instância do motor (`engine.facts`).
   * **Função:** Armazena temporariamente os fatos conhecidos:
     * É inicializada (após um `engine.reset()`) com fatos de entrada que definem o perfil do paciente, sendo instâncias das classes [Sintoma], [Exame] e [HistoricoMedico] importadas de [fatos.py]
     * É modificada dinamicamente pelo disparo das regras, adicionando novos fatos intermediários de diagnóstico, como [SindromeGripal], [SindromeObstrutiva] ou [AlertaOxigenio], e consequentemente o fato de saída final [Diagnostico]

---

## Arquitetura em 3 níveis de encadeamento

```
Nível 1 (entrada)         Nível 2 (intermediário)       Nível 3 (saída)
───────────────────       ───────────────────────       ──────────────────────
Sintoma(febre)      ──┐
Sintoma(tosse)      ──┼──► SindromeGripal ────────────► Gripe / Pneumonia
Sintoma(dor_musc)   ──┘

Sintoma(chiado)     ──┐
Sintoma(falta_ar)   ──┼──► SindromeObstrutiva ────────► Crise Asmática / DPOC
Exame(sibilos)      ──┘

Exame(oxim_baixa)   ──┐
Sintoma(falta_ar)   ──┼──► AlertaOxigenio ────────────► Hipoxemia + Pneumonia Grave
                       ┘       +SindromeGripal
```

Cada arquivo corresponde a uma camada:

- `fatos.py` define os nós (Fatos) dos três níveis
- `regras.py` define as arestas (Regras) que ligam os níveis
- `motor.py` executa o grafo e registra o caminho percorrido

---

## As 10 regras em linguagem natural

### Nível 1 → 2 (inferência de síndromes intermediárias)

| # | SE | ENTÃO | Salience |
|---|-------|-------|----------|
| R01 | paciente tem febre, tosse e dor muscular | inferir SindromeGripal | 5 |
| R02 | paciente tem chiado e falta de ar | inferir SindromeObstrutiva | 5 |
| R03 | oximetria está baixa e há falta de ar | inferir AlertaOxigenio | 6 |
| R04 | ausculta revela sibilos, histórico de asma e SindromeObstrutiva ainda não foi inferida | inferir SindromeObstrutiva (via ausculta) | 5 |

### Nível 2 → 3 (diagnóstico final)

| # | SE | ENTÃO | Salience |
|---|-------|-------|----------|
| R05 | há SindromeGripal e febre alta | diagnosticar Gripe (Influenza) — confiança alta | 9 |
| R06 | há tosse e coriza e **não** há febre | diagnosticar Resfriado Comum — confiança média | 7 |
| R07 | há SindromeGripal, falta de ar e **não** há AlertaOxigenio | diagnosticar Pneumonia Bacteriana — confiança alta | 9 |
| R08 | há SindromeObstrutiva e histórico de asma | diagnosticar Crise Asmática — confiança crítica | 15 |
| R09 | há AlertaOxigenio e SindromeGripal | diagnosticar Hipoxemia + Pneumonia Grave — confiança crítica | 20 |
| R10 | há SindromeObstrutiva e histórico de DPOC | diagnosticar Exacerbação de DPOC — confiança alta | 12 |

---

## Estratégia de resolução de conflito

O sistema usa duas estratégias complementares.

**`salience` — prioridade de execução.** Quando múltiplas regras estão habilitadas ao mesmo tempo, a `salience` determina qual dispara primeiro:

```
R09 (hipoxemia grave)   salience 20  ← máxima prioridade
R08 (crise asmática)    salience 15
R10 (DPOC)              salience 12
R05 / R07               salience  9
R06 (resfriado)         salience  7
R01–R04 (nível 1)       salience 5–6
```

No Caso 3, por exemplo, R09 (salience 20) dispara antes de R07 (salience 9), garantindo que a conduta de urgência apareça sem ser sobreposta pelo diagnóstico menos grave.

**`NOT` — diferenciação por ausência de fato.** R06 usa `NOT(Sintoma(nome="febre"))` para diagnosticar resfriado apenas quando febre está ausente — se fosse declarada, R06 não dispararia. R07 usa `NOT(AlertaOxigenio())` para não emitir pneumonia simples quando há hipoxemia. R04 usa `NOT(SindromeObstrutiva())` para evitar fatos duplicados na memória de trabalho.

---

## Instalação e execução

```bash
pip install experta

# Roda os 3 casos de teste padrão
python main.py

# Passa sintomas direto pela linha de comando
python main.py febre tosse dor_muscular febre_alta

# Roda só os testes
python testes.py
```

> **Python 3.8–3.9 recomendado.** Para versões mais recentes:
> `pip install git+https://github.com/nilp0inter/experta.git`

---

## Casos de teste

### Caso 1 — Gripe com febre alta

**Fatos de entrada:**
```python
Sintoma(nome="febre")
Sintoma(nome="tosse")
Sintoma(nome="dor_muscular")
Sintoma(nome="febre_alta")
```

**Trace esperado:**
```
[R01] febre + tosse + dor_muscular → SindromeGripal inferida
[R05] SindromeGripal + febre_alta  → Diagnóstico: Gripe (Influenza)
```

**Encadeamento:** nível 1 (sintomas) → nível 2 (SindromeGripal via R01) → nível 3 (Gripe via R05).

**Resolução de conflito:** R06 não dispara porque `febre` está presente, bloqueado pelo `NOT(Sintoma(nome="febre"))`.

**Resultado:** Gripe (Influenza) — confiança alta. Repouso, hidratação, considerar oseltamivir se < 48h de sintomas.

---

### Caso 2 — Resfriado comum (demonstra NOT)

**Fatos de entrada:**
```python
Sintoma(nome="tosse")
Sintoma(nome="coriza")
# febre não declarada
```

**Trace esperado:**
```
[R06] tosse + coriza + NOT febre → Diagnóstico: Resfriado Comum
```

**Encadeamento:** direto do nível 1 para o nível 3 — R06 verifica sintomas presentes e a ausência de febre sem precisar de fato intermediário.

**Resolução de conflito:** se `febre` fosse adicionada, R06 seria bloqueado pelo `NOT` e nenhum diagnóstico simples seria emitido.

**Resultado:** Resfriado Comum (Rinovírus) — confiança média. Sintomáticos, hidratação e repouso. Sem necessidade de antibiótico.

---

### Caso 3 — Pneumonia grave com hipoxemia (3 níveis + salience)

**Fatos de entrada:**
```python
Sintoma(nome="febre")
Sintoma(nome="tosse")
Sintoma(nome="dor_muscular")
Sintoma(nome="falta_de_ar")
Exame(tipo="oximetria", valor="baixa")
```

**Trace esperado:**
```
[R03] oximetria baixa + falta_de_ar   → AlertaOxigenio inferido
[R01] febre + tosse + dor_muscular    → SindromeGripal inferida
[R09] AlertaOxigenio + SindromeGripal → Hipoxemia + Pneumonia Grave  (salience 20)
# R07 não dispara: NOT(AlertaOxigenio()) falha pois AlertaOxigenio existe
```

**Encadeamento completo:**
```
Nível 1: febre + tosse + dor_muscular + falta_de_ar + oximetria baixa
              │                               │
Nível 2: SindromeGripal              AlertaOxigenio
              └──────────────┬──────────────────┘
Nível 3:           Hipoxemia + Pneumonia Grave
```

**Resolução de conflito:** R09 (salience 20) tem precedência sobre R07 (salience 9). O `NOT(AlertaOxigenio())` em R07 garante que Pneumonia simples não seja emitida simultaneamente.

**Resultado:** Hipoxemia + Pneumonia Grave — confiança crítica. ENCAMINHAR URGÊNCIA. Suporte de O₂, internação imediata.

---

## Conceitos demonstrados

| Conceito | Onde aparece / Como se comporta |
|----------|---------------------------------|
| **Motor de Inferência** | O framework `experta` (e a chamada [engine.run()](file:///d:/SBC/Miniteste%2001/motor.py#L52) no arquivo [motor.py](file:///d:/SBC/Miniteste%2001/motor.py)) |
| **Base de Conhecimento** | A classe [DiagnosticoRespiratorio](file:///d:/SBC/Miniteste%2001/regras.py#L27) e suas 10 regras no arquivo [regras.py](file:///d:/SBC/Miniteste%2001/regras.py) |
| **Memória de Trabalho** | Os fatos do paciente em execução (`engine.facts`), instanciados de [fatos.py](file:///d:/SBC/Miniteste%2001/fatos.py) e inseridos via `declare()` |
| Encadeamento para frente (3 níveis) | R01→R05, R03→R09, R01+R03→R09 |
| Salience (resolução de conflito) | R09 > R08 > R10 > R05/R07 > R06 > R01–R04 |
| NOT (negação de fato) | R06 (sem febre), R07 (sem AlertaOxigenio), R04 (sem duplicata) |
| Fatos intermediários | SindromeGripal, SindromeObstrutiva, AlertaOxigenio |
| Separação por módulos | fatos / regras / motor / testes / main |

---
