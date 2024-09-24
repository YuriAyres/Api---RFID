from flask import Flask, request, jsonify

app = Flask(__name__)

# Banco de dados mock para exemplo (será substituído pelo real)
alunos = {}

@app.route('/emprestar', methods=['POST'])
def emprestar_notebook():
    dados = request.json
    aluno_id = dados.get('aluno_id')
    nome = dados.get('nome')
    
    if aluno_id in alunos and alunos[aluno_id]['status'] == 'com notebook':
        return jsonify({"message": "Aluno já está com um notebook!"}), 400
    
    alunos[aluno_id] = {'nome': nome, 'status': 'com notebook'}
    return jsonify({"message": f"Notebook emprestado ao aluno {nome}"}), 200

@app.route('/devolver', methods=['POST'])
def devolver_notebook():
    dados = request.json
    aluno_id = dados.get('aluno_id')
    
    if aluno_id in alunos and alunos[aluno_id]['status'] == 'com notebook':
        alunos[aluno_id]['status'] = 'devolvido'
        return jsonify({"message": f"Notebook devolvido pelo aluno {alunos[aluno_id]['nome']}"}), 200
    else:
        return jsonify({"message": "Aluno não está com notebook para devolver!"}), 400

if __name__ == '__main__':
    app.run(debug=True)