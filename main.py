import secrets
from typing import Annotated, Dict
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

# Basic authentication setup
security = HTTPBasic()

# Hardcoded username and password for demonstration purposes
USERNAME = "user"
PASSWORD = "pass"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def print_shape(shape: str, times: int):
    if shape == "rectangle":
        for i in range(times):
            print("* " * times)
    elif shape == "triangle":
        for i in range(1, times + 1):
            print("* " * i)
    elif shape == "diamond":
        # Upper part of the diamond
        for i in range(1, times + 1):
            print(" " * (times - i) + "* " * i)
        # Lower part of the diamond
        for i in range(times - 1, 0, -1):
            print(" " * (times - i) + "* " * i)

def calculate_area(shape: str, times: int) -> float:
    if shape == "rectangle":
        return times * times
    elif shape == "triangle":
        return 1 / 2 * times * times
    elif shape == "diamond":
        return times * times
    else:
        raise HTTPException(status_code=400, detail="Invalid shape")

@app.post("/shape/{shape}")
def draw_shape(shape: str, times: int, username: str = Depends(authenticate)) -> Dict[str, str | int | float]:
    if times <= 0:
        raise HTTPException(status_code=400, detail="times must be a positive integer.")
    
    supported_shapes = ["rectangle", "triangle", "diamond"]
    if shape not in supported_shapes:
        raise HTTPException(
            status_code=400,
            detail=f"Shape '{shape}' is not supported. Please choose 'rectangle', 'triangle', or 'diamond'."
        )
    
    print(f"\nDrawing a {shape} of times {times}:")
    print_shape(shape, times)
    
    area = calculate_area(shape, times)
    return {"shape": shape, "times": times, "area": area}
