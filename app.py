from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка отправки')
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True) 