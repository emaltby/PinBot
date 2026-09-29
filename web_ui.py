import os
from flask import Flask, request, render_template_string, session, redirect, url_for
from dynamic_config import load_dynamic_config, save_dynamic_config
from database import get_all_listings

app = Flask(__name__)
# Change this in production
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key-change-me")
AUTH_PASSWORD = os.getenv("WEB_UI_PASSWORD", "changeme")

CSS_STYLES = """
<style>
    body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }
    h1 { color: #333; }
    form { display: flex; flex-direction: column; gap: 1rem; background: #f4f4f4; padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem; }
    input, textarea { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; }
    button { padding: 0.5rem 1rem; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #0056b3; }
    .logout-btn { background: #6c757d; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { padding: 0.75rem; border: 1px solid #ddd; text-align: left; }
    .status-green { color: green; font-weight: bold; }
    .status-red { color: red; font-weight: bold; }
</style>
"""

LOGIN_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>{{{{ css }}}}<title>Login</title></head>
<body>
    <h1>PinBot Login</h1>
    <form method="POST" action="/login">
        <input type="password" name="password" placeholder="Password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
""".replace("{{ css }}", CSS_STYLES)

CONFIG_TEMPLATE = f"""
<!DOCTYPE html>
<html>
<head>{{{{ css }}}}<title>Config</title></head>
<body>
    <h1>PinBot Config</h1>
    <form method="POST" action="/update">
        <label>Keywords (comma separated):</label>
        <textarea name="KEYWORDS" rows="5">{{{{ keywords|join(', ') }}}}</textarea>
        <label>Target Machines (comma separated):</label>
        <textarea name="TARGET_MACHINES" rows="5">{{{{ machines|join(', ') }}}}</textarea>
        <button type="submit">Update</button>
    </form>
    
    <h2>Listing History 
        <a href="/" style="font-size: 0.8rem; padding: 0.25rem 0.5rem; background: #28a745; color: white; text-decoration: none; border-radius: 4px; vertical-align: middle;">Refresh</a>
    </h2>
    <table>
        <tr><th>Title</th><th>Link</th><th>Emailed</th></tr>
        {{% for title, link, emailed in listings %}}
        <tr>
            <td>{{{{ title }}}}</td>
            <td><a href="{{{{ link }}}}" target="_blank">View</a></td>
            <td class="{{{{ 'status-green' if emailed else 'status-red' }}}}">{{{{ 'Yes' if emailed else 'No' }}}}</td>
        </tr>
        {{% endfor %}}
    </table>
    
    <br>
    <form method="POST" action="/logout">
        <button type="submit" class="logout-btn">Logout</button>
    </form>
</body>
</html>
""".replace("{{ css }}", CSS_STYLES)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template_string(LOGIN_TEMPLATE)
    
    config = load_dynamic_config()
    listings = get_all_listings()
    return render_template_string(CONFIG_TEMPLATE, 
                                  keywords=config['KEYWORDS'], 
                                  machines=config['TARGET_MACHINES'],
                                  listings=listings)

@app.route('/login', methods=['POST'])
def login():
    if request.form.get('password') == AUTH_PASSWORD:
        session['logged_in'] = True
        return redirect(url_for('index'))
    return "Unauthorized", 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update():
    if not session.get('logged_in'):
        return "Unauthorized", 401
    
    new_config = {
        "KEYWORDS": [k.strip() for k in request.form['KEYWORDS'].split(',')],
        "TARGET_MACHINES": [m.strip() for m in request.form['TARGET_MACHINES'].split(',')]
    }
    save_dynamic_config(new_config)
    return "Config updated! <a href='/'>Back to config</a>"

if __name__ == '__main__':
    # Default to 127.0.0.1 for local, use 0.0.0.0 for Docker
    host = os.getenv("WEB_UI_HOST", "127.0.0.1")
    app.run(host=host, port=5000)
