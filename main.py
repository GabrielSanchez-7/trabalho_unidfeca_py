
from imoveis import Apartamento, Casa, Estudio
from orcamento import TaxaContratual, Orcamento


# ---------------- Funções de entrada com validação ----------------

def ler_texto(mensagem):
    """Repete a pergunta até o usuário digitar algo não vazio."""
    texto = input(mensagem).strip()
    while texto == "":
        print("  >> Campo obrigatório. Tente novamente.")
        texto = input(mensagem).strip()
    return texto


def ler_inteiro(mensagem, minimo, maximo):
    """Lê um número inteiro dentro do intervalo [minimo, maximo]."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"  >> Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  >> Valor inválido. Digite apenas números inteiros.")


def ler_sim_nao(mensagem):
    """Aceita apenas S ou N (maiúsculo ou minúsculo). Retorna True para S."""
    resposta = input(mensagem).strip().upper()
    while resposta not in ("S", "N"):
        print("  >> Responda apenas com S ou N.")
        resposta = input(mensagem).strip().upper()
    return resposta == "S"


# ---------------- Montagem do imóvel escolhido ----------------

def escolher_imovel():
    print("\nTipos de imóvel disponíveis:")
    print("  1 - Apartamento (base R$ 700,00)")
    print("  2 - Casa        (base R$ 900,00)")
    print("  3 - Estúdio     (base R$ 1.200,00)")
    opcao = ler_inteiro("Escolha o tipo de imóvel (1-3): ", 1, 3)

    if opcao == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00)? (S/N): ")
        criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
        return Apartamento(quartos, garagem, criancas)

    elif opcao == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem (+R$ 300,00)? (S/N): ")
        return Casa(quartos, garagem)

    else:
        estacionamento = ler_sim_nao("Deseja o pacote de estacionamento com 2 vagas "
                                     "(R$ 250,00)? (S/N): ")
        extras = 0
        if estacionamento:
            extras = ler_inteiro("Quantas vagas adicionais (R$ 60,00 cada)? (0-10): ", 0, 10)
        return Estudio(estacionamento, extras)


def main():
    print("=" * 58)
    print("RENTSMART - R.M Imóveis".center(58))
    print("=" * 58)

    continuar = True
    while continuar:
        cliente = ler_texto("\nNome do cliente: ")
        imovel = escolher_imovel()
        parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa contratual "
                               "de R$ 2.000,00? (1-5): ", 1, TaxaContratual.MAX_PARCELAS)

        orcamento = Orcamento(cliente, imovel, TaxaContratual(parcelas))
        print()
        print(orcamento)

        try:
            arquivo = orcamento.exportar_csv("orcamento_12_meses.csv")
            print(f"\nProjeção de 12 meses salva em: {arquivo}")
        except OSError:
            print("\nNão foi possível gravar o arquivo CSV. Verifique se ele está aberto.")

        continuar = ler_sim_nao("\nDeseja fazer outro orçamento? (S/N): ")

    print("\nObrigado por usar o RentSmart!")


if __name__ == "__main__":
    main()
