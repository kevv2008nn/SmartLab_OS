from datetime import datetime, date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.attendance.models import Attendance
from app.student_profile.models import StudentProfile


def check_in(student_id, db: Session):

    existing = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.attendance_date == date.today(),
            Attendance.exit_time == None
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Student already inside lab."
        )

    attendance = Attendance(
        student_id=student_id,
        attendance_date=date.today(),
        entry_time=datetime.now(),
        status="IN"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    # Update Student Profile
    profile = (
        db.query(StudentProfile)
        .filter(StudentProfile.student_id == student_id)
        .first()
    )

    if profile:
        profile.total_visits += 1
        db.commit()

    return attendance


def check_out(student_id, db: Session):

    attendance = (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id,
            Attendance.exit_time == None
        )
        .first()
    )

    if attendance is None:
        raise HTTPException(
            status_code=404,
            detail="No active session found."
        )

    attendance.exit_time = datetime.now()
    attendance.status = "OUT"

    db.commit()
    db.refresh(attendance)

    return attendance


def attendance_history(student_id, db: Session):

    return (
        db.query(Attendance)
        .filter(
            Attendance.student_id == student_id
        )
        .order_by(
            Attendance.entry_time.desc()
        )
        .all()
    )


def students_inside(db: Session):

    return (
        db.query(Attendance)
        .filter(
            Attendance.exit_time == None
        )
        .all()
    )