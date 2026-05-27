from fastapi  import FastAPI,HTTPException
from uvicorn import run
from pydantic import BaseModel

app = FastAPI()

history_of_operations = []

class CalculateRequest(BaseModel):
    a: float
    b: float
    operation: str

class CalculateResponse(BaseModel):
    result: float


def calculate(a, b,operation):
    if operation == "add":
        result = float(a) + float(b)
        return result
    elif operation == "subtract":
        result = float(a) - float(b)
        return result
    elif operation == "divide":
        if b == 0:
            raise ValueError('Division by zero is not allowed')
        result = float(a) / float(b)
        return result
    else:
        raise ValueError(f'Unknown operation: {operation}')



@app.post('/calculate', response_model=CalculateResponse)
async def calculate_result(request: CalculateRequest):
    try:
        result = calculate(request.a,request.b, request.operation)
    except ValueError as e:
        raise HTTPException(
        status_code=400,
        detail= str(e)
        )
    history_of_operations.append({"operation": request.operation,
                                  "a":request.a,
                                  "b": request.b,
                                  "result": result

                                  })

    return {"result": result}
@app.get('/history')
async def get_history_of_operations():
    return {"The history of operations": history_of_operations}





if __name__ == '__main__':
    run(app)