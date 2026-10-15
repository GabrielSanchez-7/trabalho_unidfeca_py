def formatar_moeda(valor):
    """Formata um número no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    sinal = "-" if valor < 0 else ""
    return f"{sinal}R$ {texto}"


def formatar_decimal(valor):
    """Formata para o CSV no padrão do Excel em português: 1234.5 -> '1234,50'."""
    return f"{valor:.2f}".replace(".", ",")
