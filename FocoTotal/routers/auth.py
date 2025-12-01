from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from ..database import database
from ..models import UsuarioIn, UsuarioOut, Token, TokenData
from ..auth_utils import verify_password, get_password_hash, create_access_token, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Autenticação"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    query = "SELECT * FROM usuarios WHERE username = :username"
    user = await database.fetch_one(query=query, values={"username": token_data.username})
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UsuarioOut)
async def register(user: UsuarioIn):
    # Verificar se usuário já existe
    query = "SELECT * FROM usuarios WHERE username = :username"
    existing_user = await database.fetch_one(query=query, values={"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já está em uso.")
    
    # Verificar se email já existe
    query = "SELECT * FROM usuarios WHERE email = :email"
    existing_email = await database.fetch_one(query=query, values={"email": user.email})
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já está cadastrado.")
    
    hashed_password = get_password_hash(user.password)
    query = "INSERT INTO usuarios(username, email, senha_hash) VALUES (:username, :email, :senha_hash)"
    values = {"username": user.username, "email": user.email, "senha_hash": hashed_password}
    try:
        last_record_id = await database.execute(query=query, values=values)
        return {**user.dict(), "id": last_record_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    query = "SELECT * FROM usuarios WHERE username = :username"
    user = await database.fetch_one(query=query, values={"username": form_data.username})
    if not user or not verify_password(form_data.password, user["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UsuarioOut)
async def read_users_me(current_user: UsuarioOut = Depends(get_current_user)):
    return current_user
