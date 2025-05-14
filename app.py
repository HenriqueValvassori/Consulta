
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import database
import smtplib
import os

app = Flask(__name__)

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
EMAIL_SENHA = os.getenv("EMAIL_SENHA")
EMAIL_DESTINATARIO = os.getenv("")

def enviar_email(tipo, data, horario):
    assunto = "Novo Agendamento Recebido"
    corpo = f"Tipo: {tipo}\nData: {data}\nHorário: {horario}"
    msg = f"Subject: {assunto}\n\n{corpo}"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_REMETENTE, EMAIL_SENHA)
            server.sendmail(EMAIL_REMETENTE, EMAIL_DESTINATARIO, msg)
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

@app.route('/', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        tipo_procedimento = request.form['tipo_procedimento']
        data_str = request.form['data']
        horario = request.form['horario']

        try:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
            dia_semana = data_obj.weekday()

            if 4 <= dia_semana <= 6:
                hora_int = int(horario.split(':')[0])
                if 9 <= hora_int <= 20:
                    if database.agendamento_existe(data_str, horario):
                        mensagem = "Esse horário já está preenchido. Escolha outro dia ou horário."
                        return render_template('agendamento.html', mensagem=mensagem)
                    database.inserir_agendamento(tipo_procedimento, data_str, horario)
                    enviar_email(tipo_procedimento, data_str, horario)
                    return redirect(url_for('agendamentos_realizados'))
                else:
                    mensagem = "Horário indisponível. Agendamentos são das 9:00 às 21:00."
                    return render_template('agendamento.html', mensagem=mensagem)
            else:
                mensagem = "Data indisponível. Agendamentos são permitidos apenas de sexta a domingo."
                return render_template('agendamento.html', mensagem=mensagem)

        except ValueError:
            mensagem = "Formato de data inválido. Use AAAA-MM-DD."
            return render_template('agendamento.html', mensagem=mensagem)

    return render_template('agendamento.html')

@app.route('/agendamentos')
def agendamentos_realizados():
    agendamentos = database.buscar_agendamentos()
    return render_template('agendamentos.html', agendamentos=agendamentos)

if __name__ == '__main__':
    database.criar_tabela()
    app.run(debug=True)
