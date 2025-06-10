from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, 
    static_folder='front/static',
    template_folder='front/templates')

@app.route('/')
def index():
    return render_template('votacion_cat.html')

@app.route('/guardar_voto', methods=['POST'])
def guardar_voto():
    voto_presidente = request.form.get('voto_presidente')
    voto_gobernador = request.form.get('voto_gobernador')
    voto_intendente = request.form.get('voto_intendente')

    # Guardar los votos en un archivo de texto
    with open('votos.txt', 'a', encoding='utf-8') as f:
        f.write(f"Presidente: {voto_presidente}, Gobernador: {voto_gobernador}, Intendente: {voto_intendente}\n")

    # Redirigir a una página de agradecimiento
    return redirect(url_for('tu_voto'))

@app.route('/tu_voto')
def tu_voto():
    return "¡Gracias por votar!"

if __name__ == '__main__':
    app.run(debug=True) 