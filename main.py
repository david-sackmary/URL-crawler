import sys, os, csv, re, shutil
from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from collections import *
#from nltk.corpus import stopwords

if len(sys.argv) != 4:
    sys.exit("usage:  python main.py input.csv output.csv stop_words.csv")
ifile = open(sys.argv[1],'r')
ofile = open(sys.argv[2],'wb')
sfile = open(sys.argv[3],'r')   #stop words file

try:
  rows = csv.reader(ifile) #create reader object
  orows = csv.writer(ofile,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
  srows = csv.reader(sfile)

  ifile.seek(0)
  stopwords = sfile.read().split()

  for row in rows:
    try:

      url = row[0]
      print url
      ofile.write(url)

      #This retrieves the webpage content
      br = Browser()
      br.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept', '*/*')]
      res = br.open(url)
      data = res.get_data() 

      #This parses the content
      soup = BeautifulSoup(data)

      title = soup.find('title')
      ofile.write( "," + title.renderContents() + ",")
    
      description = soup.findAll(attrs={"name":"Description"})
      keywords = soup.findAll("Meta", attrs={"name":"Keywords"})

      #finds all p elements without links
      paras = soup.fetch('p')
      text = ""
      for p in paras:
        text = text + " " + p.text.encode('utf-8')

      # remove stop words
      pattern = re.compile(r'\b(' + r'|'.join(stopwords) + r')\b\s*')
      t = pattern.sub('', text)

      # word counts
      wordCount = Counter(re.findall(r"[\w']+", t.lower()))
      i = 0
      for key, count in wordCount.iteritems():
        if (i < 20):
          i = i + 1
          ofile.write(key + "," + str(count) + ",")
      ofile.write("\n")

      # keywords
      if keywords != []:
         mk = meta[0]['content'].encode('utf-8')
         print keywords

    except: # catch *all* exceptions
      e = sys.exc_info()[0]
      print ("error on URL" + url + "error is %s</p>" % e )

finally:

    ifile.close()
    ofile.close()

#Study materials which help understand this project:
# http://programming-review.com/beautifulsoasome-interesting-python-functions/
# hhtp://stackoverflow.com/questions/11300383/how-to-find-the-count-of-a-word-in-a-string
# http://stackoverflow.com/questions/16922214/reading-a-text-file-and-splitting-it-into-single-words-in-python
