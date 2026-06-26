import math


# #### Inteiros (`int`)

# 1. Escreva um programa que soma dois números inteiros inseridos pelo usuário.
""""
valor01_valido = False
while valor01_valido == False:
    try:
        input_numero_01 = int(input("Digite um numero inteiro: "))
        valor01_valido = True
    except ValueError:
        print("Voce digitou um valor invalido, digite apenas numeros inteiros")

valor02_valido = False
while valor02_valido == False:
    try:
        input_numero_02 = int(input("Digite outro numero inteiro: "))
        print(input_numero_01 + input_numero_02)
        valor02_valido = True
    except ValueError:
        print("Voce digitou um valor invalido, digite apenas numeros inteiros")
"""
# 2. Crie um programa que receba um número do usuário e calcule o resto da divisão desse número por 5.
'''
input_numero_03 = int(input("Digite um numero inteiro: "))
resto_da_divisao = input_numero_03 % 5
print(f"O resto da divisão de {input_numero_03} por 5 é: {resto_da_divisao}")
'''
# 3. Desenvolva um programa que multiplique dois números fornecidos pelo usuário e mostre o resultado.
'''
input_numero_03 = int(input("Digite um numero inteiro: "))
input_numero_04 = int(input("Digite outro numero inteiro: "))
resultado_multiplicacao = input_numero_03 * input_numero_04
print(f"O resultado da multiplicação de {input_numero_03} por {input_numero_04} é: {resultado_multiplicacao}")
'''
# 4. Faça um programa que peça dois números inteiros e imprima a divisão inteira do primeiro pelo segundo.

#input_numero_01 = int(input("Inserir um numero inteiro: "))
#input_numero_02 = int(input("Inserir outro numero inteiro: "))
#resultado = input_numero_01 // input_numero_02
#print(resultado)

# 5. Escreva um programa que calcule o quadrado de um número fornecido pelo usuário.
'''
imput_numero_05 = int(input("Digite um numero inteiro: "))
quadrado_do_numero = imput_numero_05 ** 2
'''
# #### Números de Ponto Flutuante (`float`)

# 6. Escreva um programa que receba dois números flutuantes e realize sua adição.
'''
imput_numero_06 = float(input("Digite um numero flutuante: "))
imput_numero_07 = float(input("Digite outro numero flutuante: "))   
adicao_de_numeros_flutuantes = imput_numero_06 + imput_numero_07
print(f"A soma de {imput_numero_06} e {imput_numero_07} é: {adicao_de_numeros_flutuantes}")
'''
# 7. Crie um programa que calcule a média de dois números flutuantes fornecidos pelo usuário.
'''
imput_numero_08 = float(input("Digite um numero flutuante: "))
imput_numero_09 = float(input("Digite outro numero flutuante: "))
media_dos_numeros_flutuantes = (imput_numero_08 + imput_numero_09) / 2
print(f"A média de {imput_numero_08} e {imput_numero_09} é: {media_dos_numeros_flutuantes}")
55
'''
# 8. Desenvolva um programa que calcule a potência de um número (base e expoente fornecidos pelo usuário).
'''
imput_numero_10 = float(input("Digite a base: "))
imput_numero_11 = float(input("Digite o expoente: "))
potencia_do_numero = imput_numero_10 ** imput_numero_11
print(f"A potência de {imput_numero_10} elevado a {imput_numero_11} é: {potencia_do_numero}")   
'''
# 9. Faça um programa que converta a temperatura de Celsius para Fahrenheit.
'''
imput_temperatura_celsius = float(input("Digite a temperatura em Celsius: "))
temperatura_fahrenheit = (imput_temperatura_celsius * 9/5) + 32
print(f"A temperatura de {imput_temperatura_celsius}°C é equivalente a {temperatura_fahrenheit}°F")
'''
# 10. Escreva um programa que calcule a área de um círculo, recebendo o raio como entrada.

#raio_do_circulo = float(input("Digite o raio: "))
#area_do_circulo = math.pi * raio_do_circulo ** 2
# area_do_circulo_formatada = "{:.2f}".format(area_do_circulo)
#print(f"{area_do_circulo:.2f}")

# #### Strings (`str`)

# 11. Escreva um programa que receba uma string do usuário e a converta para maiúsculas.("Digite seu nome")
nome = input("Digite seu nome: ")
print(f"Olá, {nome.upper()}!")
# 12. Crie um programa que receba o nome completo do usuário e imprima o nome com todas as letras minúsculas.
nome_completo = input("Digite seu nome completo: ")
print(f"Olá, {nome_completo.lower()}!")
# 13. Desenvolva um programa que peça ao usuário para inserir uma frase e, em seguida, imprima esta frase sem espaços em branco no início e no final.
frase = input("Digite uma frase: ")
print(f"Frase sem espaços: {frase.replace(" ", "")}")
# 14. Faça um programa que peça ao usuário para digitar uma data no formato "dd/mm/aaaa" e, em seguida, imprima o dia, o mês e o ano separadamente.
# 15. Escreva um programa que concatene duas strings fornecidas pelo usuário.

# data_do_usuario = input("Insira uma data no formato dd/mm/aaaa: ")
# lista_de_dia_mes_ano = data_do_usuario.split("/")
# print(f"O elemento 1 e o: {lista_de_dia_mes_ano[0]}")
# print(f"O elemento 2 e o: {lista_de_dia_mes_ano[1]}")
# print(f"O elemento 3 e o: {lista_de_dia_mes_ano[2]}")

# #### Booleanos (`bool`)

# 16. Escreva um programa que avalie duas expressões booleanas inseridas pelo usuário e retorne o resultado da operação AND entre elas.
# 17. Crie um programa que receba dois valores booleanos do usuário e retorne o resultado da operação OR.
# 18. Desenvolva um programa que peça ao usuário para inserir um valor booleano e, em seguida, inverta esse valor.
# 19. Faça um programa que compare se dois números fornecidos pelo usuário são iguais.
# 20. Escreva um programa que verifique se dois números fornecidos pelo usuário são diferentes.

# #### try-except e if

# 21: Conversor de Temperatura
# 22: Verificador de Palíndromo
# 23: Calculadora Simples
# 24: Classificador de Números
# 25: Conversão de Tipo com Validação