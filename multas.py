# Pergunta a velocidade do carro ao utilizador
velocidade = float(input("Qual é a velocidade do carro em km/h? "))

# Verifica se a velocidade ultrapassa o limite de 80 km/h
if velocidade > 80:
     # Calcula o valor da multa
    excesso = velocidade - 80
    multa = excesso * 5.00
    # Exibe a mensagem de multa e o valor da multa
    print(f"Você foi multado por excesso de velocidade.")
    print(f"Valor da multa: €{multa:.2f}")
else:
    # Caso não tenha ultrapassado o limite, exibe uma mensagem informativa
    print("Você está dentro do limite de velocidade.")