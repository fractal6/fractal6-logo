version := v1
logo := fractale_inv

path = img/$(version)

default: logo

logo:
	#svgexport $(path)/$(logo).svg $(path)/$(logo).png 1024:1024
	#convert -resize x16 -gravity center -crop 16x16+0+0 $(path)/$(logo).png -flatten -colors 256 $(path)/favicon-16.png
	#convert -resize x32 -gravity center -crop 32x32+0+0 $(path)/$(logo).png -flatten -colors 256 $(path)/favicon-32.png
	#convert -resize x64 -gravity center -crop 64x64+0+0 $(path)/$(logo).png -flatten -colors 256 $(path)/favicon-64.png
	#icotool -c -o $(path)/favicon.ico $(path)/favicon-16.png $(path)/favicon-32.png $(path)/favicon-64.png
	#rm $(path)/favicon-16.png $(path)/favicon-32.png $(path)/favicon-64.png
	ffmpeg -y -i $(path)/$(logo).svg -vf scale=64:64 $(path)/favicon.ico
	ffmpeg -y -i $(path)/$(logo).svg -vf scale=32:32 $(path)/favicon-32.png
	ffmpeg -y -i $(path)/$(logo).svg -vf scale=64:64 $(path)/favicon-64.png
	ffmpeg -y -i $(path)/$(logo).svg -vf scale=180:180 $(path)/favicon-180.png
	ffmpeg -y -i $(path)/$(logo).svg -vf scale=196:196 $(path)/favicon-196.png
	#svgexport $(path)/$(logo).svg $(path)/favicon-32.png 32:32
	#svgexport $(path)/$(logo).svg $(path)/favicon-64.png 64:64
	#svgexport $(path)/$(logo).svg $(path)/favicon-180.png 180:180
	#svgexport $(path)/$(logo).svg $(path)/favicon-196.png 196:196



install:
	sudo apt install icoutils ffmpeg
	npm install svgexport
