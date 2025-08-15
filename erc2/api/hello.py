from fastapi import APIRouter, Depends, HTTPException, status
from ..database import SessionDep, get_session
from models import (
    Role,
    Major,
    Period,
    Member,
    Membership,
    MembershipRole,
    MembershipMajor,
)
from typing import List
from sqlmodel import Session, select
from datetime import date
from pydantic import BaseModel, EmailStr

router = APIRouter()


class MemberCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    student_id: str
    discord_id: str
    period_id: int
    major_ids: List[int]
    role_ids: List[int]
    fee_paid: bool = False
    tshirt_received: bool = False


@router.post("/members", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member_with_details(
    *, session: Session = Depends(get_session), data: MemberCreate
):
    try:
        existing_member = session.exec(
            select(Member).where(Member.student_id == data.student_id)
        ).first()

        if existing_member:
            error_message = "Member with this data already exists."
            raise HTTPException(status_code=409, detail=error_message)

        member = Member(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            student_id=data.student_id,
            discord_id=data.discord_id,
        )
        session.add(member)
        session.flush()

        membership = Membership(
            member_id=member.id,
            period_id=data.period_id,
            fee_paid=data.fee_paid,
            tshirt_received=data.tshirt_received,
        )
        session.add(membership)
        session.flush()

        for major_id in data.major_ids:
            membership_major_link = MembershipMajor(
                membership_id=membership.id, major_id=major_id
            )
            session.add(membership_major_link)

        for role_id in data.role_ids:
            membership_role_link = MembershipRole(
                membership_id=membership.id, role_id=role_id
            )
            session.add(membership_role_link)

        session.commit()
        session.refresh(member)
        return member

    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/roles", response_model=List[Role])
def read_roles(session: Session = Depends(get_session)):
    roles = session.exec(select(Role)).all()
    return roles


@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_role(*, session: Session = Depends(get_session), role: Role):
    try:

        existing_role = session.exec(select(Role).where(Role.name == role.name)).first()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Role with name '{role.name}' already exists.",
            )

        session.add(role)
        session.commit()
        session.refresh(role)
        return role
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"An error occured while adding role: {e}"
        )


@router.get("/majors", response_model=List[Major])
def read_majors(session: Session = Depends(get_session)):
    majors = session.exec(select(Major)).all()
    return majors


@router.post("/majors", response_model=Major, status_code=status.HTTP_201_CREATED)
def create_major(*, session: Session = Depends(get_session), major: Major):
    try:

        existing_major = session.exec(
            select(Major).where(Major.name == major.name)
        ).first()
        if existing_major:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Major with name '{major.name}' already exists.",
            )

        session.add(major)
        session.commit()
        session.refresh(major)
        return major
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"An error occured while adding major: {e}"
        )


@router.get("/periods", response_model=List[Period])
def read_periods(session: Session = Depends(get_session)):
    periods = session.exec(select(Period)).all()
    return periods


@router.post("/periods", response_model=Period, status_code=status.HTTP_201_CREATED)
def create_period(*, session: Session = Depends(get_session), period: Period):
    try:
        if period.end_date <= period.start_date:
            raise HTTPException(
                status_code=400, detail="End date must be after start date."
            )
        session.add(period)
        session.commit()
        session.refresh(period)
        return period
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, detail=f"An error occured while adding period: {e}"
        )
