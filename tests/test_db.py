from sqlalchemy import select

from duno_fast_zero.models import User


def test_create_user(session):
    # Cria um banco de dados em memória
    user = User(username='test', email='email@email.com', password='123456')
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.username == 'test'))

    assert result.email == 'email@email.com'
    assert result.id == 1
