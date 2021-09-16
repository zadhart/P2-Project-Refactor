from create_app import db
from Daily_payment import Daily_payment
from Pagamentos import Pagamentos
from Pontos import Pontos


class Daily_payment_horistas(Daily_payment):
    def __init__(self, content):
        super().__init__(content)

    def Run(self):
        result = 0
        content = self.content

        # Encontrando todos os empregados horistas que recebem mensalmente
        horistas = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Horista",
                                                       Pagamentos.comissao == 0,
                                                       Pagamentos.salarioHora != 0,
                                                       Pagamentos.diaMes == content["diaMes"],
                                                       Pagamentos.tipoSem == "NaN",
                                                       Pagamentos.diaSem == "NaN").all()

        for i in horistas:

            horas = db.session.query(Pontos).filter(Pontos.id == str(i.id),
                                                    Pontos.mes == content["mes"],
                                                    Pontos.semana == content["semana"]).all()
            horas_trab = 0

            for h in horas:
                horas_trab += h.horasTrabalhadas

            horas_bonus = 0

            if horas_trab > 160:
                horas_bonus = horas_trab - 160
                horas_trab = horas_trab - 160

            result += i.salarioHora * horas_trab
            result += i.salarioHora * horas_bonus * 1.5

        # Encontrando todos os empregados horistas que recebem mensalmente
        horistas = db.session.query(Pagamentos).filter(Pagamentos.tipo == "Horista",
                                                       Pagamentos.comissao == 0,
                                                       Pagamentos.salarioHora != 0,
                                                       Pagamentos.diaMes == 0,
                                                       Pagamentos.tipoSem == content["tipoSem"],
                                                       Pagamentos.diaSem == content["diaSem"]).all()

        for i in horistas:

            horas = db.session.query(Pontos).filter(Pontos.id == str(i.id), Pontos.mes == content["mes"]).all()

            horas_trab = 0

            for h in horas:
                horas_trab += h.horasTrabalhadas

            horas_bonus = 0

            if horas_trab > 160:
                horas_bonus = horas_trab - 160
                horas_trab = horas_trab - 160

            result += i.salarioHora * horas_trab
            result += i.salarioHora * horas_bonus * 1.5

        return result
