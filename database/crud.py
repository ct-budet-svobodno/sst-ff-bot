from sqlalchemy import select, update
from .models import Activist


async def add_activist(session, na, st, tgid, bd, sg, nu, em, stu, ot):
    stmt = select(Activist).where(Activist.telegram_id == tgid)
    result = await session.execute(stmt)
    user_already_exists = result.scalar_one_or_none() is not None

    if not user_already_exists:
        new_user = Activist(telegram_id=tgid, 
                            name=na, 
                            status=st,
                            birthday=bd,
                            student_group=sg,
                            number=nu,
                            email=em,
                            studak=stu,
                            others=ot)
        session.add(new_user)
        await session.flush()
        await session.commit()
        await session.refresh(new_user)
    return user_already_exists

async def get_rate(session, telegram_id: str):
    stmt = select(Activist).where(Activist.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    else:
        return None

async def change_score(session, telegram_id, sc_dif):
    stmt = (
        update(Activist)
        .where(Activist.telegram_id == telegram_id)
        .values(score=Activist.score+sc_dif)
    )
    result = await session.execute(stmt)
    await session.commit()
    if result.rowcount == 0:
        return False
    else:
        return True


async def add_ach_or_kos(session, telegram_id, label):
    stmt = select(Activist).where(Activist.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        if user.ach_kos != None:
            new_list = label + '\n' + user.ach_kos
            if new_list.count('\n') > 9:
                index = new_list.rfind('\n')
                new_list = new_list[:index]
        else:
            new_list = label

        stmt=(
            update(Activist)
            .where(Activist.telegram_id==telegram_id)
            .values(ach_kos=new_list)
        )
        fin = await session.execute(stmt)
        await session.commit()
        if fin.rowcount == 0:
            return False
        else:
            return new_list
    else:
        return False

async def get_all_activists(session):
    stmt = select(Activist)
    result = await session.execute(stmt)
    users = result.scalars().all()
    return users

async def is_it_activist(session, telegram_id):
    stmt = select(Activist).where(Activist.telegram_id == telegram_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        return True
    else:
        return False