#pip install SqlAlchemy
#pip install werkzeug
#pip install Streamlit
#pip install psycopg2-binary
# tudo em seu amiente de trabalho, não esqueça!!

from sqlalchemy import create_engine, String, Boolean, Select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

#criar a base de dado 
class Base(DeclarativeBase):
    pass

#cria a tabela 
class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column (primary_key=True)
    nome: Mapped[str] = mapped_column(String(255))
    senha: Mapped[str] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean)  # Coluna booleana para status ativo/inativo

#conecta com Postgres    
engine = create_engine('postgresql://postgres:1234@localhost:5432/postgres')
Base.metadata.create_all(bind=engine)
        
# Função para adicionar um novo usuário
def adicionar_usuario(nome, senha, ativo):
    with Session(engine) as session: #gerencia o banco
        novo_usuario = Usuario(nome=nome, senha=senha, ativo=ativo)
        session.add(novo_usuario) #adicionar
        session.commit() # actualiza processo
        print(f"Usuário {nome} adicionado com sucesso!")

# Função para consultar todos os usuários
def consultar_usuarios():
    with Session(engine) as session:
        stmt = Select(Usuario)
        usuarios = session.scalars(stmt).all()
        for usuario in usuarios:
            print(f"ID: {usuario.id}, Nome: {usuario.nome}, Senha: {usuario.senha}")

def atualizar_usuario(usuario_id, novo_nome=None, nova_senha=None, novo_ativo=None):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if usuario:
            if novo_nome is not None:
                usuario.nome = novo_nome
            if nova_senha is not None:
                usuario.senha = nova_senha
            if novo_ativo is not None:
                usuario.ativo = novo_ativo
            session.commit()
            print(f"Usuário com ID {usuario_id} atualizado com sucesso!")
        else:
            print(f"Usuário com ID {usuario_id} não encontrado.")

def deletar_usuario(usuario_id):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if usuario:
            session.delete(usuario)
            session.commit()
            print(f"Usuário com ID {usuario_id} deletado com sucesso!")
        else:
            print(f"Usuário com ID {usuario_id} não encontrado.")

# Exemplo de uso
adicionar_usuario("Esteban", "senha222", False)

# Atualizar usuário
atualizar_usuario(usuario_id=2, novo_nome="Ester Novo", nova_senha="senha333", novo_ativo=False)

# Deletar usuário
deletar_usuario(usuario_id=1)

consultar_usuarios()

