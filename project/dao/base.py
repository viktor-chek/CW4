from typing import Generic, List, Optional, TypeVar

from flask import current_app
from flask_sqlalchemy import BaseQuery
from sqlalchemy.orm import scoped_session
from werkzeug.exceptions import NotFound
from project.setup.db.models import Base

T = TypeVar('T', bound=Base)


class BaseDAO(Generic[T]):
    """Базовый класс работы с БД"""
    __model__ = Base

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    @property
    def _items_per_page(self) -> int:
        return current_app.config['ITEMS_PER_PAGE']

    def get_by_id(self, pk: int) -> Optional[T]:
        """Получение по pk"""
        return self._db_session.query(self.__model__).get(pk)

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> List[T]:
        """Получение всех"""
        stmt: BaseQuery = self._db_session.query(self.__model__)

        if status == 'new':
            return stmt.order_by(-self.__model__.year).paginate(page, self._items_per_page).items
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []

        return stmt.all()
