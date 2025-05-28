from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    namn = request.form['namn']
    lösenord = request.form['lösenord']
    # Här skulle man normalt spara till en databas (SQL)
    return f"<h2>Hej {namn}!</h2><p>Ditt lösenord är: {lösenord}</p>"

if __name__ == '__main__':
    app.run(debug=True)
