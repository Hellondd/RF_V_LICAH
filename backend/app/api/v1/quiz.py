from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.deps import get_current_user
from app.models import QuizQuestion, QuizAnswer, QuizResult, User
from app.schemas.quiz import QuestionOut, QuizSubmit, QuizResultOut, LeaderboardEntry

router = APIRouter(prefix="/quiz", tags=["quiz"])


def _level_for(score: int, max_score: int) -> str:
    if max_score == 0:
        return "Новичок"
    ratio = score / max_score
    if ratio >= 0.9:
        return "Эксперт"
    if ratio >= 0.6:
        return "Знаток"
    if ratio >= 0.3:
        return "Любитель"
    return "Новичок"


@router.get("/questions", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    return db.query(QuizQuestion).all()


@router.post("/submit", response_model=QuizResultOut)
def submit(payload: QuizSubmit, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    score = 0
    max_score = 0
    selected_map = {item.question_id: set(item.selected_answer_ids) for item in payload.answers}

    questions = db.query(QuizQuestion).all()
    for question in questions:
        correct_ids = {a.id for a in question.answers if a.is_correct}
        if not correct_ids:
            continue
        max_score += 1
        if selected_map.get(question.id, set()) == correct_ids:
            score += 1

    level = _level_for(score, max_score)
    result = QuizResult(user_id=current_user.id, score=score, max_score=max_score, level=level)
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@router.get("/results", response_model=list[QuizResultOut])
def my_results(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return (
        db.query(QuizResult)
        .filter(QuizResult.user_id == current_user.id)
        .order_by(QuizResult.completed_at.desc())
        .all()
    )


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def leaderboard(db: Session = Depends(get_db)):
    rows = (
        db.query(QuizResult, User)
        .join(User, User.id == QuizResult.user_id)
        .order_by(QuizResult.score.desc(), QuizResult.completed_at.asc())
        .limit(10)
        .all()
    )
    return [
        LeaderboardEntry(
            user_name=user.name,
            score=res.score,
            max_score=res.max_score,
            level=res.level,
            completed_at=res.completed_at,
        )
        for res, user in rows
    ]
