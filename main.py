import os
import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from random import randint
from time import sleep

backend = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'),
                      port=int(os.environ.get('REDIS_PORT', '6379')))

MEGA=1024*1024
response="Hello World"

app = FastAPI()

# Gets the value of 'name'
@app.get('/{name}/{method}/{number}', response_class=PlainTextResponse)
@app.get('/{name}', response_class=PlainTextResponse)
def read(name: str, method: str = 'normal', number: int = 10):
    
    # Get current value of name, 0 if it doesnt exist  
    value = backend.get(name)
    if value is None:
        value = 0
   
    # Use up some resources
    responseLoad(method,number) 
    
    # Return current value of name 
    return str(int(value)) + "\n"


# Increments the value of 'name' by 1
@app.post('/{name}/{method}/{number}', response_class=PlainTextResponse)
@app.post('/{name}', response_class=PlainTextResponse)
def read_item(name: str, method: str = 'normal', number: int = 10):
    # Increment value of name in redis
    value = backend.incr(name)
    
    # Use up some resources 
    responseLoad(method,number) 
   
    # Return new value of name 
    return str(value) + "\n"

# Make some load
def responseLoad(method,number):
  if method == 'normal':
    pass 
  elif method == 'error':
    error_load(number)
  elif method == 'loop':
    loop_load(number)
  elif method == 'sleep':
    sleep_load(number)
  elif method == 'memory':
    memory_load(number)

# Generate an error at chance of 1/number
def error_load(number: int):
  if randint(1,int(number)) == 1:
    raise HTTPException(status_code=418, detail="A mysterious error")

# Loop number million times
def loop_load(number: int):
  i = 0
  while i < number:
     j = 0 
     while j < MEGA:
       j += 1  
     i += 1

# Use up memory up to number MB, 1 MB at a time
def memory_load(number):
  i = 0
  while i < number:
    try:
      a = ' ' * (i * MEGA)
      del a
    except MemoryError:
      break
    i += 1

# Sleep for up to number millseconds
def sleep_load(number):
  sleep(randint(1,int(number))/1000) == 1


