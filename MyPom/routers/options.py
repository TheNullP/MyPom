from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from MyPom.core.database import get_db, Pomo


router = APIRouter(tags=["option"])


@router.delete("/clearDb")
def clear_db(db: Session = Depends(get_db)):
    try:
        db.query(Pomo).delete()
        db.commit()
        return JSONResponse(
            content="Registro de Sessões limpado com sucesso.", status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content=f"Erro ao deletar banco de dados, {e}", status_code=400
        )
