from .. import utils, schemas, models, oauth2
from ..database import get_db
from fastapi import Depends, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

# @router.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts

@router.get("/", response_model=List[schemas.Post_Vote])
def post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int=10, skip: int=0, search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    posts = db.query(models.Post).filter(models.Post.content.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("Votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True
    ).group_by(models.Post.id).all()

    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_dict = post.model_dump()
    # new_dict["id"] = randrange(0, 100000)
    # my_posts.append(new_dict)

    
    # cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES({post.title, post.content, post.published}) RETURNING *""")
    # We can use the above query but its prone to SQL Injection

    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(user_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_one_post(id:int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} post not found!")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index = find_post_index(int(id))

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    # post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} post not found!")
    # conn.commit()

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")

    post_query.delete(synchronize_session=False)
    # db.delete(post)
    db.commit()

    # del my_posts[index]
    # return {"message":"post deleted successfully"}
    return post

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, new_post:schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # index = find_post_index(int(id))

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id).first()

    post = post_query

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"{id} post not found!")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform for this action")
    
    post_query.update(new_post.model_dump(), synchronize_session=False)
    db.commit()

    # conn.commit()

    # new_post = post.model_dump()
    # new_post["id"] = int(id)
    # my_posts[index] = new_post
    return new_post