import math, operator
import os
import shutil
from functools import reduce

from PIL.Image import Resampling
from PIL import ImageTk, Image
from os import listdir
from os.path import isfile, join

dirs = [f for f in listdir("groups") if not isfile(join("groups", f))]

for dir in dirs:
    image = [Image.open(join("groups", dir, f)) for f in listdir(join("groups", dir))[:1] if
              isfile(join("groups", dir, f))][0]

    shutil.copy(image.filename.replace("\\", '/'), f"cimages/" + image.filename.replace("\\", '/').split('/')[-1])