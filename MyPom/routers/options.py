from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from MyPom.schemas.options_schema import UpdateFocus

from MyPom.core.database import User, get_db, Pomo


router = APIRouter(tags=["options"])


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


@router.put("/updateFocus")
def update_focus(
    time: UpdateFocus,
    db: Session = Depends(get_db),
):

    if time is None or time.focus <= 0:
        raise HTTPException(detail="Somente números acima de 0.", status_code=400)
    try:
        data = db.query(User).filter_by(id=2).first()
        data.focus = time.focus
        db.commit()
        db.refresh(data)

    except Exception as e:
        raise HTTPException(
            detail=f"Erro inesperado ao tentar atualizar {e}", status_code=500
        )
    return JSONResponse(content="Atualizado com sucesso.", status_code=200)
