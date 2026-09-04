import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import pandas as pd
from sqlalchemy import inspect, text

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
EXCEL_PATH = "content/sst_ff_db.xlsx"

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    __abstract__ = True


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def is_table_empty():
    async with engine.connect() as conn:
        result = await conn.execute(text(f"SELECT COUNT(*) FROM activists"))
        count = result.scalar()
        return count

async def import_users():
    def import_with_sync_connection(conn):
        inspector = inspect(conn)
        if "activists" not in inspector.get_table_names():
                raise RuntimeError("Таблица 'activists' отсутствует в базе данных")
        db_columns = [
                column["name"]
                for column in inspector.get_columns("activists")
            ]
        df = pd.read_excel(
            EXCEL_PATH,
            sheet_name=0,
            skiprows=1,
            header=None,
        )
        df = df.dropna(how="all")
        if df.empty:
            print("Ошибка: excel-файл не содержит пользователей")
            return
    
        excel_columns = list(df.columns)

        print("Столбцы Excel:")
        print(excel_columns)

        print("\nСтолбцы БД:")
        print(db_columns)

        missing_columns = abs(len(db_columns)-len(excel_columns))
        if missing_columns != 0:
            raise RuntimeError("Количество столбцов в excel-файле и таблице не совпадает!")

        df.columns = db_columns
        df = df.where(pd.notna(df), None)

        string_cols = df.select_dtypes(include=['object']).columns
        df[string_cols] = df[string_cols].fillna("")

        print(f"\nБудет импортировано пользователей: {len(df)}")

        df.to_sql(
            name='activists',
            con=conn,
            if_exists="replace",
            index=False,
            chunksize=500,
            )
        print("Импорт успешно завершён")

    async with engine.begin() as connection:
        await connection.run_sync(import_with_sync_connection)