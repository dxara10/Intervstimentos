from flask import Flask, render_template, request, session
import sqlite3
import pandas as pd
from datetime import date, timedelta

app = Flask(__name__)

#CRIAÇÃO DA HOMEPAGE
@app.route('/')
def homepage():
    return render_template("homepage.html")

#CRIAÇÃO PAGINA SOBRENOS
@app.route('/sobrenos')
def sobrenos():
    return render_template("sobrenos.html")

#CRIAÇÃO PAGINA INTRANET
@app.route('/intranet')
def intranet():
    return render_template("intranet.html")

#CRIAÇÃO CAFE ARTE PASSEIO
@app.route('/cafeartepasseio')
def cafeartepasseio():
    return render_template("cafeartepasseio.html")



#CRIAÇÃO DAS PÁGINAS DE PERFIS
@app.route('/hospede/<nomehospede>')
def hospede(nomehospede):
    return render_template("hospede.html", nomehospede=nomehospede)

@app.route('/associado/<nomeassociado>')
def associado(nomeassociado):
    return render_template("associado.html", nomeassociado=nomeassociado)

@app.route('/administrador/<nomeadministrador>')
def administrador(nomeadministrador):
    return render_template("administrador.html", nomeadministrador=nomeadministrador)

@app.route('/atendente/<nomeatendente>')
def atendente(nomeatendente):
    return render_template("atendente.html", nomeatendente=nomeatendente)

#CRIAÇÃO DAS DEMAIS PÁGINAS
@app.route('/hospedagem')
def hospedagem():
    return render_template("hospedagem.html")

@app.route('/registrarapartamentos')
def registrarapartamentos():
    return render_template("registrarapartamentos.html")

@app.route('/registrarhospede')
def registrarhospede():
    return render_template("registrarhospede.html")

@app.route('/paginamanager')
def paginamanager():
    return render_template("paginamanager.html")





#CRIAÇÃO DO PROCESSO DE CONTROLE DE HOSPEDES
# Criação do banco de dados de locações
conexao_locados = sqlite3.connect('Apartamentos_Locados.db')
c_locados = conexao_locados.cursor()
c_locados.execute('''CREATE TABLE IF NOT EXISTS ApartamentosLocados (
    Endereço Text,
    NumerodoQuarto TEXT,
    NomedoHospede TEXT,
    NumerodePessoas INT,
    Animais TEXT,
    NumerodeAnimais INT,
    CPFresponsavel TEXT,
    Telefone TEXT,
    Data DATE)
    ''')
conexao_locados.commit()
conexao_locados.close()


#Criando Banco de Apartamentos cadastrados
conexao_aptocadastrados = sqlite3.connect('Apartamentos_cadastrados.db')
c_apcadastrados = conexao_aptocadastrados.cursor()
c_apcadastrados.execute(
    '''CREATE TABLE IF NOT EXISTS ApartamentosCadastrados (
    Endereco TEXT,
    NumerodoQuarto TEXT,
    Andar TEXT,
    Proprietario TEXT,
    cpf TEXT,
    DatadeNascimento DATE,
    Telefone TEXT,
    DatadeRegistro DATE)
    ''')
conexao_aptocadastrados.commit()
conexao_aptocadastrados.close()


#registro de apartamentos novos
@app.route('/registrarapartamento', methods=['GET', 'POST'])
def registrarapartamento():
    # Recuperar os valores dos campos do formulário
    Endereco = request.form['Endereco']
    NumerodoQuarto = request.form['NumerodoQuarto']
    Andar = request.form['Andar']
    Proprietario = request.form['Proprietario']
    cpf = request.form['cpf']
    DatadeNascimento = request.form['DatadeNascimento']
    Telefone = request.form['Telefone']
    DatadeRegistro = request.form['DatadeRegistro']

    # Conectar ao banco de dados
    conexao_aptocadastrados = sqlite3.connect('Apartamentos_cadastrados.db')
    c_apcadastrados = conexao_aptocadastrados.cursor()

    # Inserir os dados na tabela
    c_apcadastrados.execute("INSERT INTO ApartamentosCadastrados (:Endereco, :NumerodoQuarto, :Andar, :Proprietario, :cpf, :DatadeNascimento, :Telefone, :DatadeRegistro)",
                            {
                                'Endereco':Endereco,
                                'NumerodoQuarto':NumerodoQuarto,
                                'Andar':Andar,
                                'Proprietario':Proprietario,
                                'cpf':cpf,
                                'DatadeNascimento':DatadeNascimento,
                                'Telefone':Telefone,
                                'DatadeRegistro':DatadeRegistro
                            })

    # Confirmar as alterações e fechar a conexão com o banco de dados
    conexao_aptocadastrados.commit()
    conexao_aptocadastrados.close()

    return render_template("registrarapartamento.html")



#HISTÓRICO DE HOSPEDES
@app.route('/registrarhospede', methods=['GET', 'POST'])
def registrar_hospede():
    if request.method == 'POST':
        Endereco = request.form['Endereco']
        NumerodoQuarto = request.form['NumerodoQuarto']
        NomedoHospede = request.form['NomedoHospede']
        NumerodePessoas = request.form['NumerodePessoas']
        Animais = request.form['Animais']
        NumerodeAnimais = request.form['NumerodeAnimais']
        CPFresponsavel = request.form['CPFresponsavel']
        Telefone = request.form['Telefone']
        Data = request.form['Data']

        # Inserir registro no banco de dados
        conexao = sqlite3.connect('Apartamentos_Locados.db')
        c = conexao.cursor()
        c.execute(" INSERT INTO ApartamentosLocados VALUES (:Endereco, :NumerodoQuarto, :NomedoHospede, :NumerodePessoas, :Animais, :NumerodeAnimais, :CPFresponsavel, :Telefone, :Data)",
                  {
                      'Endereco':Endereco,
                      'NumerodoQuarto':NumerodoQuarto,
                      'NomedoHospede':NomedoHospede,
                      'NumerodePessoas':NumerodePessoas,
                      'Animais':Animais,
                      'NumerodeAnimais':NumerodeAnimais,
                      'CPFresponsavel':CPFresponsavel,
                      'Telefone':Telefone,
                      'Data':Data
                  })
        conexao.commit()
        conexao.close()


        return render_template("registrarhospede.html")



def obter_apartamentos_ocupados(data):
    # Implemente a lógica para obter os apartamentos ocupados
    conexao = sqlite3.connect('Apartamentos_Locados.db')
    cursor = conexao.cursor()
    query = "SELECT NumerodoQuarto FROM ApartamentosLocados WHERE Data = ?"
    cursor.execute(query, (data,))
    apartamentos_ocupados = [apartamento[0] for apartamento in cursor.fetchall()]
    conexao.close()
    return apartamentos_ocupados

def obter_apartamentos_disponiveis(data):
    conexao = sqlite3.connect('Apartamentos_Cadastrados.db')
    cursor = conexao.cursor()
    query = "SELECT NumerodoQuarto FROM ApartamentosCadastrados"
    cursor.execute(query)
    apartamentos_cadastrados = [apartamento[0] for apartamento in cursor.fetchall()]
    conexao.close()

    apartamentos_ocupados = obter_apartamentos_ocupados(data)
    apartamentos_disponiveis = list(set(apartamentos_cadastrados) - set(apartamentos_ocupados))
    return apartamentos_disponiveis


#rota que receba a data selecionada e retorne os apartamentos ocupados e disponíveis para essa data
@app.route('/dados', methods=['POST'])
def obter_dados():
    data = request.json['data']
    apartamentos_ocupados = obter_apartamentos_ocupados(data)
    apartamentos_disponiveis = obter_apartamentos_disponiveis(data)
    return {'apartamentos_ocupados': apartamentos_ocupados, 'apartamentos_disponiveis': apartamentos_disponiveis}



if __name__ == "__main__":
    app.run(debug=True)