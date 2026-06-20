# Sistema Fuzzy para Estimar o Risco de Nocaute no UFC

## Descrição

Este projeto implementa um Sistema de Inferência Fuzzy do tipo Mamdani utilizando a biblioteca scikit-fuzzy em Python. O objetivo é estimar o risco de um lutador sofrer nocaute durante uma luta de UFC a partir de informações relacionadas ao estado físico do atleta.

O sistema considera dois fatores principais:

* Dano Recebido: quantidade de golpes significativos absorvidos pelo lutador durante a luta.
* Fadiga: nível de desgaste físico apresentado pelo atleta.

Com base nessas entradas, o controlador fuzzy calcula uma saída denominada Risco de Nocaute, representando a probabilidade de o lutador sofrer um nocaute caso as condições da luta permaneçam as mesmas.

---

## Domínio do Problema

Em lutas de MMA, especialmente no UFC, a possibilidade de um nocaute depende de diversos fatores subjetivos. Nem sempre é possível definir limites exatos para afirmar quando um lutador está em perigo.

Por exemplo:

* Um lutador pode ter recebido poucos golpes, mas estar extremamente cansado.
* Outro pode estar descansado, porém ter absorvido golpes muito fortes.
* Em muitos casos, a combinação desses fatores aumenta significativamente o risco de nocaute.

A lógica fuzzy é adequada para esse tipo de problema porque permite modelar conceitos imprecisos como "dano alto", "fadiga média" e "risco elevado".

---

## Variáveis do Sistema

### Entrada 1: Dano Recebido

Domínio: 0 a 10

Termos linguísticos:

* Baixo
* Médio
* Alto

Justificativa:

Representa a quantidade e intensidade dos golpes recebidos pelo lutador ao longo do combate.

### Entrada 2: Fadiga

Domínio: 0 a 10

Termos linguísticos:

* Baixa
* Média
* Alta

Justificativa:

Representa o nível de desgaste físico do lutador, considerando fatores como movimentação, trocação e grappling.

### Saída: Risco de Nocaute

Domínio: 0 a 100

Termos linguísticos:

* Baixo
* Médio
* Alto

Justificativa:

Representa o risco estimado de o lutador sofrer um nocaute.

---

## Base de Regras Fuzzy

O sistema utiliza nove regras fuzzy para cobrir completamente o espaço de entrada.

1. SE dano é Baixo E fadiga é Baixa ENTÃO risco é Baixo

2. SE dano é Baixo E fadiga é Média ENTÃO risco é Baixo

3. SE dano é Baixo E fadiga é Alta ENTÃO risco é Médio

4. SE dano é Médio E fadiga é Baixa ENTÃO risco é Baixo

5. SE dano é Médio E fadiga é Média ENTÃO risco é Médio

6. SE dano é Médio E fadiga é Alta ENTÃO risco é Alto

7. SE dano é Alto E fadiga é Baixa ENTÃO risco é Médio

8. SE dano é Alto E fadiga é Média ENTÃO risco é Alto

9. SE dano é Alto E fadiga é Alta ENTÃO risco é Alto

---

## Tecnologias Utilizadas

* Python 3
* NumPy
* Scikit-Fuzzy
* Matplotlib
* Pillow

---

## Estrutura do Projeto

```text
ufc-risco-nocaute-fuzzy/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── main.py
│   ├── fuzzy_controller.py
│   ├── variables.py
│   └── rules.py
│
└── docs/
    └── explicacao_modelo.md
```

---

## Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd ufc-risco-nocaute-fuzzy
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Execução

Execute o programa principal:

```bash
python src/main.py
```

O programa abre uma interface grafica integrada com:

* campos e barras para inserir dano recebido e fadiga;
* botao para calcular o risco de nocaute;
* exibicao automatica da primeira imagem encontrada na pasta `imgs/`.

Formatos de imagem aceitos: `.png`, `.jpg`, `.jpeg`, `.jfif`, `.webp` e `.bmp`.

Exemplo:

```text
Digite o dano recebido (0-10): 8
Digite a fadiga (0-10): 7

Risco de Nocaute: 78.4
Classificação: Alto
```

---

## Método de Inferência

O sistema utiliza:

* Fuzzificação das entradas
* Inferência Mamdani
* Agregação das regras fuzzy
* Defuzzificação pelo método do Centroide

---

## Autor

Nathan Nóbrega

Projeto desenvolvido para a disciplina de Sistemas Baseados em Conhecimento / Lógica Fuzzy.
