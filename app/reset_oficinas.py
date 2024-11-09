from app import app, db
from app.models import Oficina


def reset_oficinas():
    with app.app_context():
        # Limpa todas as oficinas existentes
        Oficina.query.delete()
        db.session.commit()

        # Cria as oficinas na ordem correta
        oficinas = [
            Oficina(
                nome='Dança do Ventre',
                descricao='Aulas de dança do ventre',
                professor='Aischa Hortale',
                horario='17:00',
                dia_semana='Quartas',
                vagas_total=20,
                vagas_disponiveis=20,
                categoria='dança'
            ),
            Oficina(
                nome='Violão',
                descricao='Aulas de violão',
                professor='Marcinho',
                horario='18:00',
                dia_semana='Terças',
                vagas_total=15,
                vagas_disponiveis=15,
                categoria='música'
            ),
            Oficina(
                nome='Capoeira',
                descricao='Aulas de capoeira',
                professor='Mestre João',
                horario='19:00',
                dia_semana='Sextas',
                vagas_total=20,
                vagas_disponiveis=20,
                categoria='dança'
            ),
            Oficina(
                nome='Raízes Emocionais do Dinheiro',
                descricao='Workshop sobre finanças',
                professor='Lídia Souza',
                horario='14:00',
                dia_semana='19 OUT',
                vagas_total=30,
                vagas_disponiveis=30,
                categoria='financeiro'
            )
        ]

        for oficina in oficinas:
            db.session.add(oficina)

        db.session.commit()

        # Mostra as oficinas criadas e seus IDs
        todas_oficinas = Oficina.query.all()
        for oficina in todas_oficinas:
            print(f"ID: {oficina.id} - Nome: {oficina.nome}")


if __name__ == '__main__':
    reset_oficinas()