### Desafio - Refatorar o projeto da aula anterior evitando Bugs!

# 1) Solicita ao usuário que digite seu nome

nome = input("Digite seu nome: ")
print(f"Olá, {nome}! Bem-vindo ao programa de cálculo de bônus.")

# 2) Solicita ao usuário que digite o valor do seu salário
input_salario = input("Digite o valor do seu salário: ")
# Converte a entrada para um número de ponto flutuante
salario_float = float(input_salario)
# 3) Solicita ao usuário que digite o valor do bônus recebido
while True:
    try:
        input_bonus = float(input("Digite o valor do bônus recebido: "))
        break
    except ValueError:
        print("Erro: Por favor, digite um valor numérico válido para o bônus. Use ponto no lugar da virgula.")

# Converte a entrada para um número de ponto flutuante
#bonus_float = float(input_bonus)
# 4) Calcule o valor do bônus final
bonus_final = input_bonus * salario_float   # Exemplo de cálculo (20% do bônus)

# 5) Imprime a mensagem personalizada incluindo o nome do usuário, salário e bônus
print(f"{nome}, seu salário é R${salario_float:.2f} e o bônus final calculado é R${bonus_final:.2f}.")
# Bônus: Quantos bugs e riscos você consegue identificar nesse programa?
'''
digitar o valor do bonus com virgula ao invés de ponto, o programa quebra.
'''