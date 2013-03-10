class score(object):
    def __init__(self):
        self.score = 0
        self.scoreString = "0"
        
    def incScore(self,gain):
        self.score = self.score + gain
        self.scoreString = "%d" % self.score
#        print(self.scoreString)
        
    def resetScore(self):
        self.score = 0
        self.scoreString = "0"
        
    def getScore(self):
        return self.scoreString
                
#Create singleton accessible through score.get()
__instance = score()
def get(): return __instance