# #### Inteiros (`int`)

# 1. Escreva um programa que soma dois números inteiros inseridos pelo usuário.
'''
while True:
    try:
        imput1 = int(input("Digite o primeiro número inteiro: "))
        break
    except ValueError:
        print("Por favor, insira apenas números inteiros válidos.")

while True:
    try:
        imput2 = int(input("Digite o segundo número inteiro: "))
        break
    except ValueError:
        print("Por favor, insira apenas números inteiros válidos.")
soma = imput1 + imput2
print(f"A soma de {imput1} e {imput2} é: {soma}")
'''

# 2. Crie um programa que receba um número do usuário e calcule o resto da divisão desse número por 5.
# 3. Desenvolva um programa que multiplique dois números fornecidos pelo usuário e mostre o resultado.
# 4. Faça um programa que peça dois números inteiros e imprima a divisão inteira do primeiro pelo segundo.
# 5. Escreva um programa que calcule o quadrado de um número fornecido pelo usuário.

# #### Números de Ponto Flutuante (`float`)

# 6. Escreva um programa que receba dois números flutuantes e realize sua adição.
# 7. Crie um programa que calcule a média de dois números flutuantes fornecidos pelo usuário.
# 8. Desenvolva um programa que calcule a potência de um número (base e expoente fornecidos pelo usuário).
# 9. Faça um programa que converta a temperatura de Celsius para Fahrenheit.
# 10. Escreva um programa que calcule a área de um círculo, recebendo o raio como entrada.

# #### Strings (`str`)

# 11. Escreva um programa que receba uma string do usuário e a converta para maiúsculas.
# 12. Crie um programa que receba o nome completo do usuário e imprima o nome com todas as letras minúsculas.
# 13. Desenvolva um programa que peça ao usuário para inserir uma frase e, em seguida, imprima esta frase sem espaços em branco no início e no final.
# 14. Faça um programa que peça ao usuário para digitar uma data no formato "dd/mm/aaaa" e, em seguida, imprima o dia, o mês e o ano separadamente.
# 15. Escreva um programa que concatene duas strings fornecidas pelo usuário.

# #### Booleanos (`bool`)

# 16. Escreva um programa que avalie duas expressões booleanas inseridas pelo usuário e retorne o resultado da operação AND entre elas.
# 17. Crie um programa que receba dois valores booleanos do usuário e retorne o resultado da operação OR.
# 18. Desenvolva um programa que peça ao usuário para inserir um valor booleano e, em seguida, inverta esse valor.
# 19. Faça um programa que compare se dois números fornecidos pelo usuário são iguais.
# 20. Escreva um programa que verifique se dois números fornecidos pelo usuário são diferentes.

# #### try-except e if

# 21: Conversor de Temperatura
'''
input_temp = input("Digite a temperatura (ex: 36.5C ou 97.7F): ")

temp_value = float(input_temp[:-1])  # Remove a última letra (C ou F)36.

temp_farenheit = temp_value * 9 / 5 + 32

print(f"A temperatura em Fahrenheit é: {temp_farenheit:.2f}F")
'''

# 22: Verificador de Palíndromo
# 23: Calculadora Simples
'''
while True:
    try:
        input1 = float(input("Digite o primeiro número: "))
        input2 = float(input("Digite o segundo número: "))
        operation = input("Digite a operação (+, -, *, /): ")

        if operation == "+":
            resultado = input1 + input2
        elif operation == "-":
            resultado = input1 - input2
        elif operation == "*":
            resultado = input1 * input2
        elif operation == "/":
            if input2 == 0:
                print("Erro: divisão por zero.")
                continue
            resultado = input1 / input2
        else:
            print("Operação inválida.")
            continue

        print(f"O resultado da operação é: {resultado}")

    except ValueError:
        print("Erro: Digite apenas números válidos.")

'''
# 24: Classificador de Números
print("Digite um número para classificá-lo como positivo, negativo ou zero.")
while True:
    try:
        numero = float(input("Número: "))
        if numero > 0:
            print("O número é positivo.")
        elif numero < 0:
            print("O número é negativo.")
        else:
            print("O número é zero.")
        #break
    except ValueError:
        print("Erro: Digite apenas números válidos.")


        '''
        verificar
        '''

# 25: Conversão de Tipo com Validação




