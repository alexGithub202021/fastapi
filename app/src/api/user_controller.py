from fastapi import APIRouter, HTTPException, Request, Body, Response
from ..service import user_service
from ..core import state

router = APIRouter(prefix="/api/V1/users", tags=["users"])

service = user_service.User_service()


@router.get("/")
def list_users():
    try:
        data = service.get_users()
        return convert_to_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/")
def create_user(payload: dict = Body(...), response: Response = None):
    login = payload.get("login")
    pwd = payload.get("pwd")
    name = payload.get("nom")

    if isinstance(login, str) and isinstance(pwd, str) and isinstance(name, str):
        try:
            data = service.create_user(login, pwd, name)
            response.status_code = 201
            return {"message": data}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail="Invalid input types")


@router.patch("/{login}")
def udapte_user(login: str, payload: dict = Body(...)):
    new_login = payload.get("login")
    pwd = payload.get("pwd")
    name = payload.get("nom")

    if isinstance(new_login, str) and isinstance(pwd, str) and isinstance(name, str):
        try:
            return service.update_user(login, new_login, pwd, name)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail="Invalid input types")


@router.delete("/{login}")
def delete_user(login: str, response: Response):
    try:
        service.del_user(login)
        response.status_code = 204
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def convert_to_json(rows):
    state.logger.info("Description of cursor: ")
    state.logger.info(state.cur.description)
    columns = [desc[0] for desc in state.cur.description]
    result = [dict(zip(columns, row)) for row in rows]
    return result


@router.get("/analytics/{login}/{date_begin}/{date_end}")
def get_analytics(login: str, date_begin: str, date_end: str):
    """_summary_: aggregation view

    Args:
        login (str): _description_
        date_begin (str): format YYYY-MM-DD
        date_end (str): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    search_login = f"%{login}%"
    search_date_begin = f"%{date_begin}%"
    search_date_end = f"%{date_end}%"

    if (
        isinstance(login, str)
        and isinstance(date_begin, str)
        and isinstance(date_end, str)
    ):
        try:
            data = service.get_analytics(
                search_login, search_date_begin, search_date_end
            )
            return convert_to_json(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    else:
        raise HTTPException(status_code=422, detail="Invalid input types")


# @router.get("/greatings")
# def read_root():
#     msg = "hello world"
#     return {"message": msg}
