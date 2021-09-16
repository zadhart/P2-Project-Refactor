from create_app import db
from Daily_payment import Daily_payment
from Pagamentos import Pagamentos
from Vendas import Vendas

class Daily_payment_comissionados(Daily_payment):
    def __init__(self, content):
        super().__init__(content)

    def Run(self):
        content = self.content
        result = 0

        # Encontrando todos os empregados comissionados que recebem mensalmente
        comissionados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Comissionado",
                                                            Pagamentos.comissao != 0,
                                                            Pagamentos.salarioHora == 0,
                                                            Pagamentos.diaMes == content["diaMes"],
                                                            Pagamentos.tipoSem == "NaN",
                                                            Pagamentos.diaSem == "NaN").all()

        for i in comissionados:

            vendas = db.session.query(Vendas).filter(Vendas.id == str(i.id), Vendas.mes == content["mes"]).all()

            for v in vendas:
                result += v.valor * i.comissao

        # Encontrando todos os empregados comissionados que recebem mensalmente
        comissionados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Comissionado",
                                                            Pagamentos.comissao != 0,
                                                            Pagamentos.salarioHora == 0,
                                                            Pagamentos.diaMes == 0,
                                                            Pagamentos.tipoSem == content["tipoSem"],
                                                            Pagamentos.diaSem == content["diaSem"]).all()

        for i in comissionados:
            vendas = db.session.query(Vendas).filter(Vendas.id == str(i.id),
                                                     Vendas.mes == content["mes"],
                                                     Vendas.semana == content["semana"]).all()

            for v in vendas:
                result += v.valor * i.comissao

            return result