import os

loc = '../lib/images'


for i in os.listdir(loc):
	if '.png.jpg' in i:
		fp = os.path.join(loc, i)
		os.rename(fp, fp.replace('.png.jpg', '.jpg'))