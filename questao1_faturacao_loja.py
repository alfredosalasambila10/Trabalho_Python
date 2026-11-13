"""
Questão 1 - Sistema de faturação de uma loja de produtos alimentares
Docente: Atungulu Kabakaba
Executar:  python questao1_faturacao_loja.py
"""

import heapq
from dataclasses import dataclass

LIMITE_BONUS = 100_000   # Kz (bónus só se o total for SUPERIOR a este valor)
TAXA_BONUS = 0.10        # 10 %


# ----------------------------------------------------------------------
# Funções auxiliares de leitura (validam a entrada do utilizador)
# ----------------------------------------------------------------------
def ler_texto(msg):
    while True:
        valor = input(msg).strip()
        if valor:
            return valor
        print("  Valor obrigatório.")


def ler_float(msg, minimo=0.0):
    while True:
        try:
            n = float(input(msg).strip().replace(",", "."))
            if n < minimo:
                print(f"  O valor deve ser >= {minimo}.")
                continue
            return n
        except ValueError:
            print("  Número inválido.")


def ler_sim_nao(msg):
    while True:
        r = input(msg + " (s/n): ").strip().lower()
        if r in ("s", "sim"):
            return True
        if r in ("n", "nao", "não"):
            return False
        print("  Responda com 's' ou 'n'.")


def ler_genero(msg="Género (M/F): "):
    while True:
        g = input(msg).strip().upper()
        if g in ("M", "F"):
            return g
        print("  Escreva M ou F.")


def fmt_kz(valor):
    return f"{valor:,.2f} Kz".replace(",", " ")


# ----------------------------------------------------------------------
# Modelo de dados
# ----------------------------------------------------------------------
@dataclass
class ClienteLoja:
    nome: str
    genero: str
    valor_compras: float
    gravida: bool = False
    idoso: bool = False
    deficiente: bool = False
    bonus: float = 0.0
    valor_a_pagar: float = 0.0

    @property
    def prioritario(self):
        # Prioridade de atendimento: grávida, idoso ou pessoa com deficiência.
        # É INDEPENDENTE do bónus comercial.
        return self.gravida or self.idoso or self.deficiente

    def motivo_prioridade(self):
        motivos = []
        if self.gravida:
            motivos.append("grávida")
        if self.idoso:
            motivos.append("idoso(a)")
        if self.deficiente:
            motivos.append("pessoa com deficiência")
        return ", ".join(motivos) if motivos else "sem prioridade"


def calcular_fatura(cliente):
    """Bónus comercial: 10% se o total das compras for superior a 100 000 Kz."""
    if cliente.valor_compras > LIMITE_BONUS:
        cliente.bonus = cliente.valor_compras * TAXA_BONUS
    else:
        cliente.bonus = 0.0
    cliente.valor_a_pagar = cliente.valor_compras - cliente.bonus


def imprimir_fatura(c):
    print("\n" + "-" * 50)
    print("               FATURA - LOJA ALIMENTAR")
    print("-" * 50)
    print(f"Cliente ........ : {c.nome}")
    print(f"Género ......... : {'Feminino' if c.genero == 'F' else 'Masculino'}")
    print(f"Total compras .. : {fmt_kz(c.valor_compras)}")
    if c.bonus > 0:
        print(f"Bónus (10%) .... : -{fmt_kz(c.bonus)}")
    else:
        print("Bónus .......... : não elegível (compras <= 100 000 Kz)")
    print(f"VALOR A PAGAR .. : {fmt_kz(c.valor_a_pagar)}")
    print(f"Atendimento .... : {c.motivo_prioridade()}")
    print("-" * 50)


# ----------------------------------------------------------------------
# Programa principal
# ----------------------------------------------------------------------
def main():
    print("=" * 60)
    print("FATURAÇÃO DA LOJA DE PRODUTOS ALIMENTARES".center(60))
    print("=" * 60)

    fila = []          # heap: (prioridade, ordem_chegada, cliente)
    ordem = 0
    atendidos = []

    while True:
        print("\n1) Registar cliente / compra")
        print("2) Ver fila de espera")
        print("3) Atender próximo cliente")
        print("4) Resumo do dia")
        print("0) Sair")
        op = input("Opção: ").strip()

        if op == "1":
            nome = ler_texto("Nome do cliente: ")
            genero = ler_genero()
            valor = ler_float("Valor total das compras (Kz): ")
            gravida = ler_sim_nao("É grávida?") if genero == "F" else False
            idoso = ler_sim_nao("É pessoa idosa?")
            deficiente = ler_sim_nao("É pessoa com deficiência?")

            cliente = ClienteLoja(nome, genero, valor, gravida, idoso, deficiente)
            calcular_fatura(cliente)
            ordem += 1
            prioridade = 0 if cliente.prioritario else 1
            heapq.heappush(fila, (prioridade, ordem, cliente))
            imprimir_fatura(cliente)
            print(f"Posição na fila: {'PRIORITÁRIA' if prioridade == 0 else 'normal'}")

        elif op == "2":
            if not fila:
                print("Fila vazia.")
                continue
            print("\nFila de espera (ordem de atendimento):")
            for i, (p, o, c) in enumerate(sorted(fila), 1):
                tag = "[PRIORIDADE]" if p == 0 else "[normal]"
                print(f"  {i}. {c.nome:<20} {tag} {c.motivo_prioridade()}")

        elif op == "3":
            if not fila:
                print("Não há clientes em espera.")
                continue
            _, _, c = heapq.heappop(fila)
            atendidos.append(c)
            print(f"\nA atender: {c.nome} ({c.motivo_prioridade()})")
            print(f"Valor a pagar: {fmt_kz(c.valor_a_pagar)}")

        elif op == "4":
            todos = atendidos + [c for _, _, c in fila]
            total = sum(c.valor_compras for c in todos)
            bonus = sum(c.bonus for c in todos)
            print(f"\nClientes registados : {len(todos)}")
            print(f"Já atendidos        : {len(atendidos)}")
            print(f"Em espera           : {len(fila)}")
            print(f"Total bruto         : {fmt_kz(total)}")
            print(f"Total em bónus      : {fmt_kz(bonus)}")
            print(f"Total faturado      : {fmt_kz(total - bonus)}")

        elif op == "0":
            print("Até breve!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
