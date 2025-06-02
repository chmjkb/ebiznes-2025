from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.config import Config
import secrets
from datetime import datetime

from config import settings
from database import get_db
from models import User, Token

# Setup OAuth
config = Config(environ={
    "GOOGLE_CLIENT_ID": settings.GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET": settings.GOOGLE_CLIENT_SECRET,
    "GITHUB_CLIENT_ID": settings.GITHUB_CLIENT_ID,
    "GITHUB_CLIENT_SECRET": settings.GITHUB_CLIENT_SECRET
})

oauth = OAuth(config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

router = APIRouter(prefix="/auth", tags=["oauth"])

@router.get("/login/google")
async def login_google(request: Request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/login/github")
async def login_github(request: Request):
    redirect_uri = settings.GITHUB_REDIRECT_URI
    return await oauth.github.authorize_redirect(request, redirect_uri)

async def handle_oauth_callback(provider: str, request: Request, db: Session):
    """Handle OAuth callback for any provider"""
    try:
        if provider == "google":
            token = await oauth.google.authorize_access_token(request)
            user_info = token.get('userinfo')
            if not user_info:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            email = user_info.get('email')
        elif provider == "github":
            token = await oauth.github.authorize_access_token(request)
            resp = await oauth.github.get('user', token=token)
            user_data = resp.json()
            
            # Get primary email
            email_resp = await oauth.github.get('user/emails', token=token)
            emails = email_resp.json()
            primary_email = next((e['email'] for e in emails if e['primary']), user_data.get('email'))
            
            email = primary_email or user_data.get('email')
            if not email:
                raise HTTPException(status_code=400, detail="Failed to get user email")
        else:
            raise HTTPException(status_code=400, detail="Invalid provider")
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
    # Check if user exists
    user = db.query(User).filter(User.username == email).first()
    if not user:
        # Create new user
        user = User(
            username=email,
            password_hash="",  # OAuth users don't have passwords
            oauth_provider=provider
        )
        db.add(user)
        db.commit()
    
    # Create token
    token_string = secrets.token_urlsafe(32)
    token_obj = Token(
        token=token_string,
        username=user.username,
        created_at=datetime.utcnow()
    )
    db.add(token_obj)
    db.commit()
    
    # Return HTML that posts message to parent window
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAuth Callback</title>
    </head>
    <body>
        <script>
            // Post message to parent window with auth data
            if (window.opener) {{
                window.opener.postMessage({{
                    type: 'oauth-callback',
                    token: '{token_string}',
                    username: '{user.username}'
                }}, '{settings.FRONTEND_URL}');
                window.close();
            }} else {{
                // If no opener, redirect to frontend
                window.location.href = '{settings.FRONTEND_URL}';
            }}
        </script>
        <p>Authentication successful! You can close this window.</p>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

@router.get("/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    return await handle_oauth_callback("google", request, db)

@router.get("/callback/github")
async def github_callback(request: Request, db: Session = Depends(get_db)):
    return await handle_oauth_callback("github", request, db)