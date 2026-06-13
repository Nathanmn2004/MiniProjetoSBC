from fuzzy_controller import calcular_risco_nocaute


def ler_valor(nome_variavel):
    while True:
        try:
            valor = float(input(f"Digite o valor de {nome_variavel} (0 a 10): "))

            if 0 <= valor <= 10:
                return valor

            print("Erro: o valor deve estar entre 0 e 10.")

        except ValueError:
            print("Erro: digite um número válido.")


def main():
    print("=== Sistema Fuzzy para Estimar Risco de Nocaute no UFC ===")

    dano = ler_valor("dano recebido")
    fadiga = ler_valor("fadiga")

    risco, classificacao = calcular_risco_nocaute(dano, fadiga)

    print("\n=== Resultado ===")
    print(f"Dano recebido: {dano}")
    print(f"Fadiga: {fadiga}")
    print(f"Risco de nocaute: {risco:.2f}%")
    print(f"Classificação: {classificacao}")


if __name__ == "__main__":
    main()