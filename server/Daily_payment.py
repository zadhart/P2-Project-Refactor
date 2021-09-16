from create_app import db
from Pagamentos import Pagamentos


class Daily_payment():
    def __init__(self, content):
        self.content = content

    def Run(self):
        result = 0
        content = self.content

        # Encontrando todos os empregados assalariados que recebem mensalmente
        assalariados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Assalariado",
                                                           Pagamentos.comissao == 0,
                                                           Pagamentos.salarioHora == 0,
                                                           Pagamentos.diaMes == content["diaMes"],
                                                           Pagamentos.tipoSem == "NaN",
                                                           Pagamentos.diaSem == "NaN").all()

        for i in assalariados:
            result += i.salario

        # Encontrando todos os empregados assalariados que recebem semanalmente
        assalariados = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Assalariado",
                                                           Pagamentos.comissao == 0,
                                                           Pagamentos.salarioHora > 0,
                                                           Pagamentos.diaSem == content["diaSem"],
                                                           Pagamentos.tipoSem == content["tipoSem"],
                                                           Pagamentos.diaMes == 0).all()

        for i in assalariados:
            result += i.salario

        return result
