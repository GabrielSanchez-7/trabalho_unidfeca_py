
class Imovel:
    """Classe base. Define o que todo imóvel possui e como o aluguel é formado."""

    tipo = "Imóvel"
    aluguel_base = 0.0

    def calcular_adicionais(self):
        """Retorna uma lista de tuplas (descrição, valor) com os adicionais.
        Cada tipo de imóvel sobrescreve este método com a sua regra."""
        return []

    def calcular_descontos(self, subtotal):
        """Retorna uma lista de tuplas (descrição, valor) com os descontos."""
        return []

    def subtotal(self):
        """Aluguel-base + todos os adicionais."""
        total_adicionais = sum(valor for _, valor in self.calcular_adicionais())
        return round(self.aluguel_base + total_adicionais, 2)

    def aluguel_mensal(self):
        """Valor final do aluguel: subtotal - descontos."""
        subtotal = self.subtotal()
        total_descontos = sum(valor for _, valor in self.calcular_descontos(subtotal))
        return round(subtotal - total_descontos, 2)

    def detalhamento(self):
        """Lista com todas as linhas que formam o aluguel (para o resumo)."""
        linhas = [(f"Aluguel-base ({self.tipo})", self.aluguel_base)]
        for descricao, valor in self.calcular_adicionais():
            linhas.append((f"(+) {descricao}", valor))
        linhas.append(("Subtotal", self.subtotal()))
        for descricao, valor in self.calcular_descontos(self.subtotal()):
            linhas.append((f"(-) {descricao}", -valor))
        return linhas

    def descricao(self):
        return self.tipo

    def __str__(self):
        return self.descricao()


class ImovelResidencial(Imovel):
    """Regras compartilhadas por Casa e Apartamento: 1 ou 2 quartos e garagem."""

    adicional_segundo_quarto = 0.0
    VALOR_GARAGEM = 300.0

    def __init__(self, quartos, tem_garagem):
        if quartos not in (1, 2):
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.quartos = quartos
        self.tem_garagem = tem_garagem

    def calcular_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional 2 quartos", self.adicional_segundo_quarto))
        if self.tem_garagem:
            adicionais.append(("Vaga de garagem", self.VALOR_GARAGEM))
        return adicionais

    def descricao(self):
        garagem = "com garagem" if self.tem_garagem else "sem garagem"
        return f"{self.tipo} - {self.quartos} quarto(s), {garagem}"


class Apartamento(ImovelResidencial):
    tipo = "Apartamento"
    aluguel_base = 700.0
    adicional_segundo_quarto = 200.0
    PERCENTUAL_DESCONTO = 0.05  # 5% para clientes sem crianças

    def __init__(self, quartos, tem_garagem, tem_criancas):
        super().__init__(quartos, tem_garagem)
        self.tem_criancas = tem_criancas

    def calcular_descontos(self, subtotal):
        # Desconto aplicado APÓS os adicionais (sobre o subtotal)
        if not self.tem_criancas:
            valor = round(subtotal * self.PERCENTUAL_DESCONTO, 2)
            return [("Desconto 5% (sem crianças)", valor)]
        return []

    def descricao(self):
        criancas = "com crianças" if self.tem_criancas else "sem crianças"
        return f"{super().descricao()}, {criancas}"


class Casa(ImovelResidencial):
    tipo = "Casa"
    aluguel_base = 900.0
    adicional_segundo_quarto = 250.0


class Estudio(Imovel):
    tipo = "Estúdio"
    aluguel_base = 1200.0
    VALOR_PACOTE_VAGAS = 250.0   # pacote inicial com 2 vagas
    VAGAS_NO_PACOTE = 2
    VALOR_VAGA_EXTRA = 60.0

    def __init__(self, quer_estacionamento, vagas_extras=0):
        if vagas_extras < 0:
            raise ValueError("A quantidade de vagas extras não pode ser negativa.")
        if not quer_estacionamento and vagas_extras > 0:
            raise ValueError("Vagas extras exigem o pacote de estacionamento.")
        self.quer_estacionamento = quer_estacionamento
        self.vagas_extras = vagas_extras

    def total_vagas(self):
        if not self.quer_estacionamento:
            return 0
        return self.VAGAS_NO_PACOTE + self.vagas_extras

    def calcular_adicionais(self):
        adicionais = []
        if self.quer_estacionamento:
            adicionais.append(("Pacote estacionamento (2 vagas)", self.VALOR_PACOTE_VAGAS))
            if self.vagas_extras > 0:
                adicionais.append((f"{self.vagas_extras} vaga(s) adicional(is) x R$ 60,00",
                                   self.vagas_extras * self.VALOR_VAGA_EXTRA))
        return adicionais

    def descricao(self):
        if self.quer_estacionamento:
            return f"{self.tipo} - {self.total_vagas()} vaga(s) de estacionamento"
        return f"{self.tipo} - sem estacionamento"
