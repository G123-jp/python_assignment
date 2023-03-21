from fastapi import FastAPI
from api import appv1

app = FastAPI()
app.mount('/api/v1', appv1)

@app.get('/')
def root():
    return { 'message': "Hello World" }
