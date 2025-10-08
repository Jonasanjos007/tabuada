from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'segredo_123'  # necessário para usar sessões


def gerar_pergunta():
    """Gera uma pergunta de acordo com o nível escolhido"""
    nivel = session.get('nivel', 'leve')

    # Define faixas de valores conforme a dificuldade
    if nivel == 'leve':
        minimo, maximo = 1, 10
    elif nivel == 'medio':
        minimo, maximo = 20, 40
    elif nivel == 'dificil':
        minimo, maximo = 50, 70
    elif nivel == 'hard':
        minimo, maximo = 81, 99
    else:
        minimo, maximo = 1, 10

    operadores = ['+', '-', '*', '/']
    operador = random.choice(operadores)

    if operador == '+':
        num1 = random.randint(minimo, maximo)
        num2 = random.randint(minimo, maximo)
        resultado = num1 + num2

    elif operador == '-':
        num1 = random.randint(minimo, maximo)
        num2 = random.randint(minimo, num1)
        resultado = num1 - num2

    elif operador == '*':
        num1 = random.randint(minimo, maximo)
        num2 = random.randint(minimo, maximo)
        resultado = num1 * num2

    elif operador == '/':
        # Garante divisão exata
        resultado = random.randint(minimo, maximo)
        num2 = random.randint(1, 10)
        num1 = resultado * num2

    # Gera 3 respostas erradas diferentes
    opcoes = [resultado]
    while len(opcoes) < 4:
        errada = random.randint(minimo, maximo * 2)
        if errada != resultado and errada not in opcoes:
            opcoes.append(errada)

    random.shuffle(opcoes)

    return {
        'num1': num1,
        'num2': num2,
        'operador': operador,
        'resultado': resultado,
        'opcoes': opcoes
    }


@app.route('/')
def escolher_nivel():
    """Tela inicial para escolher o nível de dificuldade"""
    return render_template('nivel.html')


@app.route('/iniciar', methods=['POST'])
def iniciar():
    """Inicia o jogo com base no nível escolhido"""
    nivel = request.form.get('nivel')
    session['nivel'] = nivel
    session['acertos'] = 0
    session['erros'] = 0
    session['pergunta'] = 1
    session['pergunta_atual'] = gerar_pergunta()

    return redirect('/jogo')


@app.route('/jogo')
def jogo():
    """Mostra a pergunta atual"""
    return render_template('index.html',
                           pergunta=session['pergunta_atual'],
                           num_pergunta=session['pergunta'],
                           acertos=session['acertos'],
                           erros=session['erros'],
                           mensagem=None,
                           nivel=session['nivel'])


@app.route('/responder', methods=['POST'])
def responder():
    resposta = int(request.form.get('resposta'))
    correto = session['pergunta_atual']['resultado']

    if resposta == correto:
        session['acertos'] += 1
        mensagem = "✅ Correto!"
    else:
        session['erros'] += 1
        mensagem = f"❌ Errado! O resultado certo era {correto}."

    session['pergunta'] += 1

    if session['pergunta'] > 10:
        return render_template('fim.html',
                               acertos=session['acertos'],
                               erros=session['erros'],
                               nivel=session['nivel'])

    session['pergunta_atual'] = gerar_pergunta()

    return render_template('index.html',
                           pergunta=session['pergunta_atual'],
                           num_pergunta=session['pergunta'],
                           acertos=session['acertos'],
                           erros=session['erros'],
                           mensagem=mensagem,
                           nivel=session['nivel'])


@app.route('/reiniciar')
def reiniciar():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
