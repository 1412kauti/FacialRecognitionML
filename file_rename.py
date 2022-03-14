import os

FList = os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR,"images")

image_dir = os.path.join(image_dir,"oszkar")

os.chdir(image_dir)

Flist  = os.listdir(os.getcwd())
FlistC = Flist[1:]

m = 0
for i in FlistC:
    fileExtension = os.path.splitext(i)[1]
    os.rename(i,str(m)+fileExtension)
    m=m+1