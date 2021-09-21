"""
From the moment I understood the weakness of my flesh, it disgusted me.
I craved the strength and certainty of steel.
I aspired to the purity of the Blessed Machine.
Your kind cling to your flesh, as if it will not decay and fail you.
One day the crude biomass that you call a temple will wither, and you will beg my kind to save you.
But I am already saved, for the Machine is immortal...

...even in death I serve the Omnissiah
"""

import copy
from flask import request
from create_app import db, app
from Empregado import Empregado
from Pagamentos import Pagamentos
from Pontos import Pontos
from Vendas import Vendas
from Sindicato import Sindicato
from Tcard_change import Tcard_change
from Sell_change import Sell_change
from Update_change import Update_change
from Add_employee_change import Add_employee_change
from Rmv_employee_change import Rmv_employee_change
from Daily_payment import Daily_payment
from Daily_payment_horistas import Daily_payment_horistas
from Daily_payment_comissionados import Daily_payment_comissionados

last_changes = []


# Creating the Routes
@app.route("/ADD_EMPLOYEE", methods=["GET", "POST"])
def add_employee():
    content = request.get_json()

    new_employee = Empregado(
        endereco=content["endereco"],
        nome=content["nome"]
    )

    db.session.add(new_employee)

    last_changes.append(Add_employee_change(prev_data=new_employee, new_data=None))

    newSind = Sindicato(
        id=new_employee.id,
        membro= content["sindicato"],
        taxa=content["taxa"],
        taxa_add=content["taxa_add"]
    )

    db.session.add(newSind)

    # Estabelecendo o tipo de pagamento do funcionario
    tipoPagam = Pagamentos(
        id=new_employee.id,
        tipo=content["tipo"],
        diaMes=content["diaMes"],
        diaSem=content["diaSem"],
        tipoSem=content["tipoSem"],
        salario=content["salario"],
        comissao=content["comissao"],
        salarioHora=content["salarioHora"]
    )
    db.session.add(tipoPagam)

    db.session.commit()

    print("Created new employee: " + str(new_employee.id))
    return str(new_employee.id)


@app.route("/RMV_EMPLOYEE", methods=["GET", "POST"])
def rmv_employee():
    content = request.get_json()

    obj = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    save_obj = copy.deepcopy(obj)

    last_changes.append(Rmv_employee_change(prev_data=save_obj, new_data=None))

    db.session.delete(obj)
    db.session.commit()

    return "Employee removed"


@app.route("/SELL", methods=["GET", "POST"])
def sell():
    content = request.get_json()

    sell = Vendas(
        id=content["id"],
        valor=content["valor"],
        mes=content["mes"],
        semana=content["semana"],
        dia=content["dia"]
    )

    db.session.add(sell)

    last_changes.append(Sell_change(prev_data=sell, new_data=None))

    db.session.commit()

    print("Created sale")

    return "Created sale"


@app.route("/TCARD", methods=["GET", "POST"])
def read_tcard():
    content = request.get_json()

    card = Pontos(
        id=content["id"],
        horasTrabalhadas=content["horasTrabalhadas"],
        mes=content["mes"],
        semana=content["semana"]
    )

    db.session.add(card)

    last_changes.append(Tcard_change(prev_data=card, new_data=None))

    db.session.commit()

    print("Added TCARD")
    return "Added TCARD"


@app.route("/UPDATE", methods=["GET", "POST"])
def update():
    content = request.get_json()

    funcionario = db.session.query(Empregado).filter(Empregado.id == content["id"]).first()

    old_one = funcionario

    funcionario.endereco = content["endereco"]

    funcPagamento = db.session.query(Pagamentos).filter(Pagamentos.id == content["id"]).first()

    funcPagamento.tipo = content["tipo"]
    funcPagamento.diaMes = content["diaMes"]
    funcPagamento.diaSem = content["diaSem"]
    funcPagamento.tipoSem = content["tipoSem"]
    funcPagamento.salario = content["salario"]
    funcPagamento.salarioHora = content["salarioHora"]
    funcPagamento.comissao = content["comissao"]

    funcSindicato = db.session.query(Sindicato).filter(Sindicato.id == content["id"]).first()

    funcSindicato.taxa = content["taxa"]
    funcSindicato.taxa_add = content["taxa_add"]
    funcSindicato.membro = content["sindicato"]

    last_changes.append(Update_change(prev_data=old_one, new_data=funcionario))

    db.session.commit()

    print("updated")
    return "Updated"

@app.route("/UNDO", methods=["GET", "POST"])
def CtrlZ():
    content = request.get_json()
    c = last_changes.pop(0)
    c.undo()

    return "ctrlZ"

@app.route("/RUN", methods=["GET", "POST"])
def Run():
    result = 0
    content = request.get_json()

    # Calculando o salario dos assalariados
    assalariados = Daily_payment(content)

    result += assalariados.Run()

    # Calculando o salario dos horistas
    horistas = Daily_payment_horistas(content)

    result += horistas.Run()

    # Calculando o salario dos comissionados
    comissionados = Daily_payment_comissionados(content)

    result += comissionados.Run()

    return str(result)

if __name__ == '__main__':
    app.run()
