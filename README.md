# Pdf-Conversion-Docker
This is a minimal first version to solve complex image compression using local thresholding algorythms.
The goal is to produce 200DPI Black and white only, CCITT FAX compressed, A4 documents, no matter the input resolution.

This is very much a draft, and the code is really horrible for now, but as it was requested I have decided to release it.

Please be aware that this Dockerfile downloads a shell script for imagemagick from fred's webpage and sets its rights to execute when building the container.

Maybe you will like to download it and store it for security reasons.
Just place it in the same folder as the dockerfile and remove the wget command.

"http://www.fmwconcepts.com/imagemagick/downloadcounter.php?scriptname=localthresh&dirname=localthresh"

On the docker host, mount a network share where PDF files are stored to be converted.
Mount it with a RW permission.

example : 
mkdir /media/docs
and in /etc/fstab
//fileserver/docs /media/docs cifs rw,username=user,password=password,guest,uid=root,iocharset=utf8,file_mode=0666,dir_mode=0666,noperm 0 0

to run : 

clone this repo,
docker build .
docker up -e "PDFPATHORIGIN=/media/docs"

Be careful, each files are deleted and moved to a subfolder named "converted"
Currently it produces 3 different versions, with different settings for bias and radius.

This is to accomodate differences in input quality.

This is meant to become a web platform but I have no time currently to do it.

