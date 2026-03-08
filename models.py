from typing import List

from sqlalchemy import Column, Float, ForeignKeyConstraint, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class AccountEventTypes(Base):
    __tablename__ = 'account_event_types'
    __table_args__ = (
        Index('event_type_UNIQUE', 'event_type', unique=True),
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    event_type = mapped_column(String(45), nullable=False)

    account_events: Mapped[List['AccountEvents']] = relationship('AccountEvents', uselist=True, back_populates='account_event_type')


class Accounts(Base):
    __tablename__ = 'accounts'
    __table_args__ = (
        Index('account_number_UNIQUE', 'account_number', unique=True),
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    account_number = mapped_column(String(45), nullable=False)

    account_events: Mapped[List['AccountEvents']] = relationship('AccountEvents', uselist=True, back_populates='account')


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        Index('category_UNIQUE', 'category', unique=True),
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    category = mapped_column(String(45), nullable=False)

    account_events: Mapped[List['AccountEvents']] = relationship('AccountEvents', uselist=True, back_populates='category')


class AccountEvents(Base):
    __tablename__ = 'account_events'
    __table_args__ = (
        ForeignKeyConstraint(['account_event_type_id'], ['account_event_types.id'], name='fk_account_events_account_event_types1'),
        ForeignKeyConstraint(['account_id'], ['accounts.id'], name='fk_account_events_accounts'),
        ForeignKeyConstraint(['category_id'], ['categories.id'], name='fk_account_events_categories1'),
        Index('fk_account_events_account_event_types1_idx', 'account_event_type_id'),
        Index('fk_account_events_accounts_idx', 'account_id'),
        Index('fk_account_events_categories1_idx', 'category_id')
    )

    id = mapped_column(INTEGER(11), primary_key=True)
    value = mapped_column(Float, nullable=False)
    dt = mapped_column(TIMESTAMP, nullable=False, server_default=text('now()'))
    account_id = mapped_column(INTEGER(11), nullable=False)
    account_event_type_id = mapped_column(INTEGER(11), nullable=False)
    category_id = mapped_column(INTEGER(11), nullable=False)

    account_event_type: Mapped['AccountEventTypes'] = relationship('AccountEventTypes', back_populates='account_events')
    account: Mapped['Accounts'] = relationship('Accounts', back_populates='account_events')
    category: Mapped['Categories'] = relationship('Categories', back_populates='account_events')
