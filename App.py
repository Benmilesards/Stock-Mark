from flask import Flask, render_template, request, redirect, url_for, session
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Directly setting your API key (not recommended for production)
openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        return redirect(url_for('profile'))
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/ai_predicter', methods=['GET', 'POST'])
def ai_predicter():
    prediction = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=user_input,
            max_tokens=100
        )
        prediction = response.choices[0].text.strip()
    return render_template('ai_predicter.html', prediction=prediction)

@app.route('/fake_money', methods=['GET', 'POST'])
def fake_money():
    return render_template('fake_money.html')

@app.route('/graph_and_stats')
def graph_and_stats():
    return render_template('graph_and_stats.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
