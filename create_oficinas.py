from app import app, db
from app.models import Oficina


def criar_oficinas():
    with app.app_context():
        oficinas = [
            Oficina(
                nome='Dança do Ventre',
                descricao='Aulas de dança do ventre com a professora Aischa Hortale. Aprenda a arte milenar da dança do ventre.',
                professor='Aischa Hortale',
                horario='17:00',
                dia_semana='Quartas',
                vagas_total=20,
                vagas_disponiveis=20,
                categoria='dança',
                ativa=True
            ),
            Oficina(
                nome='Violão',
                descricao='Aulas de violão com o professor Marcinho. Para iniciantes e intermediários.',
                professor='Marcinho',
                horario='18:00',
                dia_semana='Terças',
                vagas_total=15,
                vagas_disponiveis=15,
                categoria='música',
                ativa=True
            ),
            Oficina(
                nome='Raízes Emocionais do Dinheiro',
                descricao='Workshop sobre finanças com Lídia Souza. Entenda sua relação com o dinheiro.',
                professor='Lídia Souza',
                horario='14:00',
                dia_semana='19 OUT',
                vagas_total=30,
                vagas_disponiveis=30,
                categoria='financeiro',
                ativa=True
            )
        ]

        try:
            for oficina in oficinas:
                db.session.add(oficina)

        
            db.session.commit()
            print("Oficinas criadas com sucesso!")

            todas_oficinas = Oficina.query.all()
            for oficina in todas_oficinas:
                print(f"Oficina: {oficina.nome} - Professor(a): {oficina.professor}")

        except Exception as e:
            print(f"Erro ao criar oficinas: {e}")
            db.session.rollback()


if __name__ == '__main__':
    criar_oficinas()
