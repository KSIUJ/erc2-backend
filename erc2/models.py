from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date


class Major(SQLModel, table=True):
    __tablename__ = "majors"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=128)
    members: List["Member"] = Relationship(back_populates="major")

    def __str__(self):
        return self.name


class Member(SQLModel, table=True):
    __tablename__ = "members"
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=128)
    last_name: str = Field(max_length=128)
    email: str = Field(unique=True, max_length=128)
    student_id: str = Field(unique=True, max_length=30)
    discord_id: Optional[str] = Field(default=None, unique=True, max_length=128)
    major_id: int = Field(foreign_key="majors.id")
    major: Major = Relationship(back_populates="members")
    memberships: List["Membership"] = Relationship(back_populates="member")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Period(SQLModel, table=True):
    __tablename__ = "periods"
    id: Optional[int] = Field(default=None, primary_key=True)
    start_date: date
    end_date: date
    memberships: List["Membership"] = Relationship(back_populates="period")

    def __str__(self):
        return f"{self.start_date.year}/{self.end_date.year}"


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=64)
    membership_roles: List["MembershipRole"] = Relationship(back_populates="role")

    def __str__(self):
        return self.name


class MembershipRole(SQLModel, table=True):
    __tablename__ = "membership_roles"
    membership_id: Optional[int] = Field(
        default=None, foreign_key="memberships.id", primary_key=True
    )
    role_id: Optional[int] = Field(
        default=None, foreign_key="roles.id", primary_key=True
    )
    membership: "Membership" = Relationship(back_populates="membership_roles")
    role: "Role" = Relationship(back_populates="membership_roles")

    def __str__(self):
        membership_display = (
            str(self.membership) if self.membership else "Unknown Membership"
        )
        role_display = str(self.role) if self.role else "Unknown Role"
        return f"MembershipRole: {membership_display} - {role_display}"


class Membership(SQLModel, table=True):
    __tablename__ = "memberships"
    id: Optional[int] = Field(default=None, primary_key=True)
    member_id: int = Field(foreign_key="members.id")
    period_id: int = Field(foreign_key="periods.id")
    fee_paid: bool = Field(default=False)
    tshirt_received: bool = Field(default=False)
    member: Member = Relationship(back_populates="memberships")
    period: Period = Relationship(back_populates="memberships")
    membership_roles: List["MembershipRole"] = Relationship(back_populates="membership")

    def __str__(self):
        member_display = (
            f"{self.member.first_name} {self.member.last_name}"
            if self.member
            else "Unknown Member"
        )
        period_display = (
            f"{self.period.start_date.year}/{self.period.end_date.year}"
            if self.period
            else "Unknown Period"
        )
        return f"Membership for {member_display} in {period_display}"
