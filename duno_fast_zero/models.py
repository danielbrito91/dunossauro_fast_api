from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

# Registrar metadados
table_registry = registry()


# Estou criando uma dataclass que representa uma tabela do banco
# Registro escalar
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    # Init false -> não quero que o valor seja inicializado,
    # pois o banco de dados vai fazer
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
