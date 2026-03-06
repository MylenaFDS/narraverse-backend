from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


class PostService:

    @staticmethod
    def create(db: Session, post_data: PostCreate, owner_id: int):
        post = Post(**post_data.dict(), owner_id=owner_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_all(db: Session):
        return db.query(Post).all()

    @staticmethod
    def get_by_id(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def update(db: Session, post_id: int, post_data: PostUpdate):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None

        for key, value in post_data.dict().items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete(db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return False

        db.delete(post)
        db.commit()
        return True