from fastapi import FastAPI, Response, Depends
from supabase import create_client, Client
from dotenv import load_dotenv
import uvicorn 
import os

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")
supabase: Client = create_client(
    SUPABASE_URL, 
    SUPABASE_PUBLIC_KEY
    )

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Root"}


@app.post("/signup")
async def signup(email: str, password: str):
    res = supabase.auth.sign_up({"email": email, "password": password})
    print(res)
    return {"message": "Signed up successfully"}


@app.post("/login")
async def login(email: str, password: str):
    supabase.auth.sign_in_with_password({"email": email, "password": password})
    return {"message": "logged in successfully"}


@app.post("/logout")
async def logout(response: Response):
    res = supabase.auth.sign_out()
    response.delete_cookie(key="access_token")
    return res


# @app.get("/protected")
# async def protected_route(user: dict = Depends(get_current_user)):
#     # Do something with the authenticated user's information
#     return {"message": "You are authenticated!", "user": user}






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)