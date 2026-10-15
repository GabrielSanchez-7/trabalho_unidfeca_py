import csv

from utils import formatar_moeda, formatar_decimal


class TaxaContratual:
    """Taxa de contrato de R$ 2.000,00, parcelável em até 5 vezes.
    É tratada separadamente do aluguel mensal."""

    VALOR_TOTAL = 2000.0
    MAX_PARCELAS = 5

    def __init__(self, parcelas):
        if parcelas < 1 or parcelas > self.MAX_PARCELAS:
            raise ValueError(f"O parcelamento deve ser de 1 a {self.MAX_PARCELAS} vezes.")
        self.parcelas = parcelas

    def valor_parcela(self):
        return round(self.VALOR_TOTAL / self.parcelas, 2)

    def parcela_do_mes(self, mes):
        """Valor da taxa cobrado no mês informado (0 depois da última parcela).
        A última parcela absorve a diferença de arredondamento (ex.: 3x)."""
        if mes > self.parcelas:
            return 0.0
        if mes == self.parcelas:
            return round(self.VALOR_TOTAL - self.valor_parcela() * (self.parcelas - 1), 2)
        return self.valor_parcela()

    def __str__(self):
        if self.parcelas == 1:
            return f"à vista: {formatar_moeda(self.VALOR_TOTAL)}"
        return f"{self.parcelas}x de {formatar_moeda(self.valor_parcela())}"


class Orcamento:
    """Junta cliente, imóvel e taxa contratual; gera o resumo e a projeção."""

    MESES_PROJECAO = 12

    def __init__(self, cliente, imovel, taxa):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    def projecao(self):
        """Lista de dicionários, um por mês, com os valores previstos."""
        meses = []
        aluguel = self.imovel.aluguel_mensal()
        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            meses.append({
                "mes": mes,
                "aluguel": aluguel,
                "parcela_contrato": parcela,
                "total_mes": round(aluguel + parcela, 2),
            })
        return meses

    def total_alugueis_ano(self):
        return round(sum(m["aluguel"] for m in self.projecao()), 2)

    def total_primeiro_ano(self):
        return round(sum(m["total_mes"] for m in self.projecao()), 2)

    def exportar_csv(self, caminho="orcamento_12_meses.csv"):
        """Gera o CSV com a projeção dos 12 meses (separador ';' para Excel pt-BR)."""
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mes", "Aluguel mensal (R$)",
                               "Parcela taxa contratual (R$)", "Total do mes (R$)"])
            for m in self.projecao():
                escritor.writerow([m["mes"], formatar_decimal(m["aluguel"]),
                                   formatar_decimal(m["parcela_contrato"]),
                                   formatar_decimal(m["total_mes"])])
            escritor.writerow(["TOTAL", formatar_decimal(self.total_alugueis_ano()),
                               formatar_decimal(self.taxa.VALOR_TOTAL),
                               formatar_decimal(self.total_primeiro_ano())])
        return caminho

    def __str__(self):
        largura = 58
        linhas = [
            "=" * largura,
            "RENTSMART - ORÇAMENTO DE LOCAÇÃO".center(largura),
            "R.M Imóveis".center(largura),
            "=" * largura,
            f"Cliente: {self.cliente}",
            f"Imóvel : {self.imovel.descricao()}",
            "",
            "COMPOSIÇÃO DO ALUGUEL MENSAL",
        ]
        for descricao, valor in self.imovel.detalhamento():
            linhas.append(f"  {descricao:.<38} {formatar_moeda(valor):>15}")
        linhas.append(f"  {'ALUGUEL MENSAL':.<38} {formatar_moeda(self.imovel.aluguel_mensal()):>15}")
        linhas += [
            "",
            "TAXA CONTRATUAL (cobrada à parte do aluguel)",
            f"  {'Valor total':.<38} {formatar_moeda(self.taxa.VALOR_TOTAL):>15}",
            f"  {'Parcelamento':.<38} {str(self.taxa):>15}",
            "",
            "PROJEÇÃO DO 1º ANO (12 meses)",
            f"  {'Total em aluguéis':.<38} {formatar_moeda(self.total_alugueis_ano()):>15}",
            f"  {'Total da taxa contratual':.<38} {formatar_moeda(self.taxa.VALOR_TOTAL):>15}",
            f"  {'TOTAL DO 1º ANO':.<38} {formatar_moeda(self.total_primeiro_ano()):>15}",
            "=" * largura,
        ]
        return "\n".join(linhas)
