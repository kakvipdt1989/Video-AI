from sqlalchemy.orm import Session

from app.models import AppSetting


def get_setting(db: Session, key: str, default: str | None = None) -> str | None:
    item = db.query(AppSetting).filter(AppSetting.key == key).first()
    return item.value if item else default


def set_setting(db: Session, key: str, value: str | None, is_secret: bool = False) -> AppSetting:
    item = db.query(AppSetting).filter(AppSetting.key == key).first()
    if item is None:
        item = AppSetting(key=key, value=value, is_secret=1 if is_secret else 0)
        db.add(item)
    else:
        item.value = value
        item.is_secret = 1 if is_secret else 0
    db.commit()
    db.refresh(item)
    return item
