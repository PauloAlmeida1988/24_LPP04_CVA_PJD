velocidade = float(input("Qual é a velocidade do carro em km/h? "))
if velocidade > 80:
    excesso = velocidade - 80
    multa = excesso * 5.00
    print(f"Você foi multado por excesso de velocidade.")
    print(f"Valor da multa: €{multa:.2f}")
else:
    print("Você está dentro do limite de velocidade.")
#teste

#teste