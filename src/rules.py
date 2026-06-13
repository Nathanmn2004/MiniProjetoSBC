from skfuzzy import control as ctrl


def criar_regras(dano, fadiga, risco):
    regras = [
        ctrl.Rule(dano['baixo'] & fadiga['baixa'], risco['baixo']),
        ctrl.Rule(dano['baixo'] & fadiga['media'], risco['baixo']),
        ctrl.Rule(dano['baixo'] & fadiga['alta'], risco['medio']),

        ctrl.Rule(dano['medio'] & fadiga['baixa'], risco['baixo']),
        ctrl.Rule(dano['medio'] & fadiga['media'], risco['medio']),
        ctrl.Rule(dano['medio'] & fadiga['alta'], risco['alto']),

        ctrl.Rule(dano['alto'] & fadiga['baixa'], risco['medio']),
        ctrl.Rule(dano['alto'] & fadiga['media'], risco['alto']),
        ctrl.Rule(dano['alto'] & fadiga['alta'], risco['alto']),
    ]

    return regras