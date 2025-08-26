from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from . import schemas, services, exceptions

app = FastAPI(
    title="User Balance API",
    description="REST API для управления пользователями и переводами",
    version="1.0.0",
)


@app.exception_handler(exceptions.AppException)
async def app_exception_handler(request, exc):
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, exceptions.UserNotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, exceptions.UserAlreadyExistsException):
        status_code = status.HTTP_409_CONFLICT

    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


@app.post(
    "/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user_data: schemas.UserCreate):
    """Создание нового пользователя"""
    try:
        user = services.UserService.create_user(
            name=user_data.name, email=user_data.email, balance=user_data.balance
        )
        return user
    except exceptions.UserAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@app.get("/users", response_model=list[schemas.UserResponse])
async def get_users():
    """Получение списка всех пользователей"""
    return services.UserService.get_all_users()


@app.post("/transfer", response_model=schemas.TransferResponse)
async def make_transfer(transfer_data: schemas.TransferRequest):
    """Выполнение перевода между пользователями"""
    try:
        from_user, to_user = services.TransferService.make_transfer(
            from_user_id=transfer_data.from_user_id,
            to_user_id=transfer_data.to_user_id,
            amount=transfer_data.amount,
        )

        return schemas.TransferResponse(
            message="Transfer successful",
            from_user_balance=from_user.balance,
            to_user_balance=to_user.balance,
        )
    except exceptions.AppException as e:
        raise  # Обрабатывается в глобальном обработчике


@app.get("/health")
async def health_check():
    """Проверка работоспособности API"""
    return {"status": "healthy", "users_count": len(services.storage.users)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
