from passlib.apache import HtpasswdFile
import jwt

class Auth:
    def __init__(self,user=None,passwd=None):
        self.db = './user.db'
        self.ht = HtpasswdFile(self.db)
        self.user = user 
        self.passwd = passwd
        self.token = None
        self.jwt_conf = {}
        self.jwt_conf['iss'] = 'MDI emo'
        self.jwt_conf['algorithm'] = 'HS256'
        self.jwt_conf['secret_key'] = '0lantern4baneEnable6shrimpPrevious9humilityrigin57celerylabor2neatable7DeckerUpstairsflocapricornWhip'
    def UserAdd(self,user,passwd):
        if user not in self.ht.users():
            self.ht.set_password(user,passwd)
            self.ht.save()
            return True
        return False
        
    def ChangePasswd(self,user,passwd):
        if user in self.ht.users() :
            self.ht.set_password(user,passwd)
            self.ht.save()
            return True
        return False
    
    def Login(self):
        if self.ht.check_password(self.user, self.passwd):
            self.token = self.__Token(self.user)
            return True
        return False

    def Chk_Token(self,token):
            try:
                jwt.decode(token,self.jwt_conf['secret_key'],self.jwt_conf['algorithm'])
                self.token = token
                return True
            except:
                return False
    
    def __Token(self,userdata):
        payload = {}
        payload['iss'] = self.jwt_conf['iss']
        payload['uid'] = f"{userdata}"
        return jwt.encode(payload,self.jwt_conf['secret_key'],self.jwt_conf['algorithm'])