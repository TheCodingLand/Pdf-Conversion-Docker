import math
import glob, os, random, shutil, time
from subprocess import call
import logging



class Pdffile(object):
    def __init__(self,file, folder, workingdir):
        self.name = file
        self.path = folder
        self.workingdir = workingdir
        self.tempdir = f"{self.workingdir!s}/{random.randint(0,9999999)!s}/"
        self.fullpath = f"{self.path!s}{self.name!s}"
        self.totalpages=0



class Option(object):

    def __init__(self, algo, bias, radius, method):
        self.algo = algo
        self.bias = bias
        self.radius = radius
        self.method = method

os.getenv('')
monitoringDir = "/media/docs/"
workingdir= os.getcwd()


options = []

options.append(Option(algo="localthresh",bias=5, radius=12, method=1))
options.append(Option(algo="localthresh",bias=15, radius=5, method=1))
options.append(Option(algo="localthresh",bias=3, radius=5, method=1))

def copyImage(pdf):
    if not os.path.exists(f"{pdf.tempdir!s}images/"):
        os.makedirs(f"{pdf.tempdir!s}images/")
    
    command = f'convert -density 200 "{pdf.tempdir!s}{pdf.name!s}" {pdf.tempdir!s}images/image_0000.jpg'
    logging.warning(command)
    call(command, shell=True)


def extractPages(pdf):
    if not os.path.exists(f"{pdf.tempdir!s}images/"):
        os.makedirs(f"{pdf.tempdir!s}images/")
    for i in range(0, 2000):
        command = f'convert -density 200 "{pdf.tempdir!s}{pdf.name!s}"[{i!s}] {pdf.tempdir!s}images/image_{i:04}.jpg'
        logging.warning(command)
        returncode = call(command, shell=True)
        if returncode == 1:
            break

def convertImage(pdf, option):
    if not os.path.exists(f"{pdf.tempdir!s}converted/"):
        os.makedirs(f"{pdf.tempdir!s}converted/")
    for i in range(0,pdf.totalpages):
        command = f"/usr/src/app/{option.algo!s} -b {option.bias!s} -r {option.radius!s} -m {option.method!s} -n yes {pdf.tempdir!s}border/image_{i:04}.jpg {pdf.tempdir!s}converted/image_{i:04}.gif"
        logging.warning(command)
        call(command, shell=True)

def addBorderA4(pdf):
    if not os.path.exists(f"{pdf.tempdir!s}border/"):
        os.makedirs(f"{pdf.tempdir!s}border/")
    for i in range(0,pdf.totalpages):
        command = f"convert {pdf.tempdir!s}shrink/image_{i:04}.jpg -gravity center -extent 1653x2339 {pdf.tempdir!s}border/image_{i:04}.jpg"
        logging.warning(command)
        call(command, shell=True)

def shrinkOnlyLarger(pdf):
    if not os.path.exists(f"{pdf.tempdir!s}shrink/"):
        os.makedirs(f"{pdf.tempdir!s}shrink/")
    for i in range(0,pdf.totalpages):
        
        command = f"convert {pdf.tempdir!s}images/image_{i:04}.jpg -resize 1653x2339\\> {pdf.tempdir!s}shrink/image_{i:04}.jpg"
        logging.warning(command)
        call(command, shell=True)

def buildPdf(pdf,option):
    command= f'convert -density 200 {pdf.tempdir!s}converted/image_*.gif -compress group4 "{pdf.path!s}converted/m_{option.method!s}_b_{option.bias!s}_r_{option.radius!s}{pdf.name!s}"'
    logging.warning(command)
    call(command, shell=True)

def imageToPdf(pdf,option):
    pdfname = pdf.name.replace(".jpg",".pdf")
    command= f'convert -density 200 {pdf.tempdir!s}converted/image_*.gif -compress group4 "{pdf.path!s}converted/{pdfname!s}"'
    logging.warning(command)
    call(command, shell=True)

def lookForFiles(folder):
    time.sleep(2)
    os.chdir(folder)
    for file in glob.glob(f"*.pdf"):
        #os.chdir(workingdir)
        
        
        pdf = Pdffile(file, folder, workingdir)
        if not os.path.exists(f"{pdf.tempdir!s}"):
            os.makedirs(f"{pdf.tempdir!s}")
        try:
            shutil.move(pdf.fullpath, pdf.tempdir)
        except:
            pass
        
        os.chdir(workingdir)
        extractPages(pdf)
        pdf.totalpages = len(os.listdir(f'{pdf.tempdir!s}images/'))
        logging.warning(pdf.totalpages)
        shrinkOnlyLarger(pdf) #tempdir to shrink
        addBorderA4(pdf) #shrink to border
        for option in options:
            convertImage(pdf,option) #border to converted
            buildPdf(pdf,option)
        try:
            call(f'rm -rf {pdf.tempdir!s}', shell=True)
        except:
            logging.warning("could not delete temp dir, will be cleaned up with cronjob")
    os.chdir(folder)
    for file in glob.glob(f"*.jpg"):
        #os.chdir(workingdir)
        
        
        pdf = Pdffile(file, folder, workingdir)
        if not os.path.exists(f"{pdf.tempdir!s}"):
            os.makedirs(f"{pdf.tempdir!s}")
        try:
            shutil.move(pdf.fullpath, pdf.tempdir)
        except:
            pass
        os.chdir(workingdir)
        copyImage(pdf)
        pdf.totalpages = len(os.listdir(f'{pdf.tempdir!s}images/'))
        logging.warning(pdf.totalpages)
        shrinkOnlyLarger(pdf) #tempdir to shrink
        addBorderA4(pdf) #shrink to border
        option = options[0]
       
        convertImage(pdf,option) #border to converted
        imageToPdf(pdf,option)
        try:
            call(f'rm -rf {pdf.tempdir!s}', shell=True)
        except:
            logging.warning("could not delete temp dir, will be cleaned up with cronjob")
while True:
    time.sleep(10)
    lookForFiles(monitoringDir)
