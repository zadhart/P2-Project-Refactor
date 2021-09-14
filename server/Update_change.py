from create_app import db
from Change import Change
from Empregado import Empregado

class Update_change(Change):
    def __init__(self, new_data, prev_data):
        super().__init__(new_data, prev_data)

    def undo(self):
        # Removendo o update antigo
        obj = self.new_data
        db.session.delete(obj)
        db.session.commit()

        # Adicionando um novo update
        new_employee = Empregado(
            endereco=self.prev_data.endereco,
            nome=self.prev_data.nome
        )
        db.session.add(new_employee)
        db.session.commit()
