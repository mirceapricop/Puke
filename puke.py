#!/usr/bin/python
import random
import cgi
import cgitb
cgitb.enable()

def generate_model(cfdist, word, min_count, num=50):
  origword = word
  for i in range(num):
    pos = [s for s in cfdist.filter(word) if cfdist.count(word,s) > min_count and s != word ]
    if i==0:
      print word.capitalize()
    else:
      print word
    try:
      word = random.choice(pos)
    except IndexError:
      word = origword
 
def bigrams(words):
  result = []
  for i, w in enumerate(words[:-1]):
    result.append((w, words[i+1]))
  return result
 
class FreqDist:
  def __init__ (self, bigram):
    self.hash = dict()
    for b in bigram:
      if b in self.hash:
        self.hash[b]=self.hash[b]+1
      else:
        self.hash[b]=1
    
  def filter(self, w):
    result = []
    for item in self.hash:
      if item[0] == w:
        result.append(item[1])
    return result
  
  def count(self, w, s):
    return self.hash[(w,s)]

  def __str__(self):
    return self.hash.__str__()
 
def main():
  print "Content-type: text/html\n"
  form = cgi.FieldStorage();
  if form.has_key('source'):
    text = form['source'].value
    bigs = bigrams(text.split())
    # print bigs
    cfd = FreqDist(bigs)
    # print cfd
    count = 0
    if form.has_key('count'):
      count = int(form['count'].value)
    coverage = 0
    if form.has_key('coverage'):
      coverage = int(form['coverage'].value)
    generate_model(cfd, random.choice(text.split()), coverage, count)
  print(".\n")

main()

