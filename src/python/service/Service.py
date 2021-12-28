from models import *
from sqlalchemy import exc


class AuthService():
    def login(self,username,password):
        username = username.strip()
        password = password.strip()

        u = UserLoginModel.query.filter(UserLoginModel.username==username,
            UserLoginModel.password==password).first()
        return u
    def getByID(self,userlogin_id):
        return UserLoginModel.query.get(int(userlogin_id))
    def getAll(self):
        return UserLoginModel.query.all()
    
class PictureService():
    def is_Permission(self,userlogin_id,picture_id):
        userlogin_id= int(userlogin_id)
        picture_id=int(picture_id)
        pic= PictureModel.query.filter(PictureModel.userlogin_id==userlogin_id,
                            PictureModel.id==picture_id).first()
        return not not pic

    def insert(self,userlogin_id,pic):
        picture = PictureModel(userlogin_id=userlogin_id,pic=pic)
        db.session.add(picture)
        try:
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False;
    def getByUserID(self,userlogin_id):
        # lay toan bo anh cua user
        pics= PictureModel.query.filter(PictureModel.userlogin_id==userlogin_id)
        return pics
    def searchByPicID(self,userlogin_id,picture_id):
        # lay thong tin cua anh duoc chia se toi user
        u = AuthService().getByID(userlogin_id)
        # tim trong list anh da su hu
        for pic in u.pictures:
            if(pic.id==picture_id):
                return pic
        # tim trong list share
        for sh in u.shares:
            if(sh.picture_id==picture_id):
                return sh.picture
        # ko tim thay
        return None
    def getPicByID(self,picture_id):
        return PictureModel.query.get(int(picture_id))

class ShareService():
    def getByUserID(self,userlogin_id):
        # lay picture share cho user_id
        shares = SharePictureModel.query.filter(SharePictureModel.userlogin_id==userlogin_id)
        return shares
    
    
    def searchByPicID(self,picture_id):
        shares =SharePictureModel.query.filter(SharePictureModel.picture_id==picture_id)
        return shares

    
    
    def insertMore(self,picture_id,list_user):
        for userlogin_id in list_user:
            self.insert(picture_id,userlogin_id)
        try:
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False;
        
    def insert(self,picture_id,userlogin_id):
        share = SharePictureModel(picture_id=picture_id,
                      userlogin_id=userlogin_id)
        try:  
            db.session.add(share)
            db.session.flush()
            db.session.refresh(share)
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False;
        return share
    
    def remove(self,picture_id,userlogin_id):
        share = SharePictureModel.query.filter(SharePictureModel.picture_id==picture_id,
                    SharePictureModel.userlogin_id==userlogin_id).first()
        if not share:
            return False
        db.session.delete(share)
        try:
            db.session.commit()
            return True
        except exc.SQLAlchemyError:
            db.session.rollback()
            return False;
        


    
