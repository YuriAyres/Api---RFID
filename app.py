from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuração da URI de conexão com o banco de dados PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/alunos_atitus_notebooks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Aluno(db.Model):
    __tablename__ = 'alunos'
    aluno_id = db.Column(db.Integer, primary_key=True)
    ra = db.Column(db.String(20), unique=True, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Text, nullable=False)
    numero_notebook = db.Column(db.String(20), nullable=True)

@app.route('/emprestar', methods=['POST'])
def emprestar_notebook():
    dados = request.json
    aluno_id = dados.get('aluno_id')
    nome = dados.get('nome')
    ra = dados.get('ra')
    numero_notebook = dados.get('numero_notebook')  # Novo campo
    
    aluno = Aluno.query.get(aluno_id)
    
    if aluno and aluno.status == 'com notebook':
        return jsonify({"message": "Aluno já está com um notebook!"}), 400
    
    if aluno:
        aluno.status = 'com notebook'
        aluno.numero_notebook = numero_notebook  # Armazena o número do notebook
    else:
        novo_aluno = Aluno(ra=ra, nome=nome, status='com notebook', numero_notebook=numero_notebook)
        db.session.add(novo_aluno)
    
    db.session.commit()
    return jsonify({"message": f"Notebook {numero_notebook} emprestado ao aluno {nome}"}), 200


@app.route('/devolver', methods=['POST'])
def devolver_notebook():
    dados = request.json
    aluno_id = dados.get('aluno_id')

    aluno = Aluno.query.get(aluno_id)
    
    if not aluno or aluno.status != 'com notebook':
        return jsonify({"message": "Aluno não possui notebook emprestado!"}), 400
    
    # Atualiza o status do aluno e remove o número do notebook
    aluno.status = 'sem notebook'
    aluno.numero_notebook = None  # Remove o número do notebook
    
    db.session.commit()
    return jsonify({"message": f"Notebook devolvido pelo aluno {aluno.nome}"}), 200

@app.route('/alunos', methods=['GET'])
def get_alunos():
    # Faz a consulta para obter todos os alunos do banco de dados
    alunos = Aluno.query.all()

    # Transforma o resultado da consulta em um formato JSON
    alunos_list = [{'ra': aluno.ra, 'nome': aluno.nome, 'status': aluno.status, 'numero_notebook': aluno.numero_notebook} for aluno in alunos]

    return jsonify(alunos_list), 200

@app.route('/alunos/<tag>', methods=['GET'])
def get_aluno(tag):
    aluno = Aluno.query.filter_by(aluno_id=tag).first()
    if aluno is None:
        return jsonify({"message": "Aluno não encontrado."}), 404
    return jsonify({"ra": aluno.ra, "nome": aluno.nome}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


