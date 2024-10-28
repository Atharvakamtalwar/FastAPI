from fastapi import Depends, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not exists!")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()
    # if vote.like == True:
    #     if found_vote:
    #         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already liked the {vote.post_id} post1")
    #     new_like = models.Vote(post_id = vote.post_id, user_id = current_user.id)
    #     db.add(new_like)
    #     db.commit()

    #     return {"Success": f"You liked the {vote.post_id} post."}
    # else:
    #     if not found_vote:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found!!")

    #     vote_query.delete(synchronize_session = False)
    #     db.commit()

    #     return {"Success": f"You removed the liked {vote.post_id} post."}

    if not found_vote:
        if vote.like == True:
            new_like = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_like)
            db.commit()

            return {"Success": f"You liked the {vote.post_id} post."}
        else:
            raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="You cannot dislike unliked post")
        
    else:
        if vote.like == True:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already liked the {vote.post_id} post1")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            
            return {"Success": f"You removed the liked {vote.post_id} post."}