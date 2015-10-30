

### The only things you'll have to edit (unless you're porting this script over to a different language) 
### are at the bottom of this file.

import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys
import os

""""""""""""""""""""
""""""""""""""""""""

class NullDevice:
  def write(self, s):
    pass

def submit():   
  print '==\n== [sandbox] Submitting Solutions \n=='
  
  (login, password) = loginPrompt()
  if not login:
    print '!! Submission Cancelled'
    return
  
  print '\n== Connecting to Coursera ... '

  # Part Identifier
  (partIdx, sid) = partPrompt()

  # Get Challenge
  (login, ch, state, ch_aux) = getChallenge(login, sid) #sid is the "part identifier"
  if((not login) or (not ch) or (not state)):
    # Some error occured, error string in first return element.
    print '\n!! Error: %s\n' % login
    return

  # Attempt Submission with Challenge
  ch_resp = challengeResponse(login, password, ch)
  #try:
  (result, string) = submitSolution(login, ch_resp, sid, output(partIdx), \
                                  source(partIdx), state, ch_aux)
  
  print '== %s' % string.strip()
  #except:
    #print
    #print 'Submission Failure from error',str(sys.exc_info()[0])
    #print 'The error can be caused by a too large output file, or some unexpected output preventing the submission.'

# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  (login, password) = basicPrompt()
  return login, password


def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, password)."""
  login = raw_input('Login (Email address): ')
  password = raw_input('One-time Password (from the assignment page. This is NOT your own account\'s password): ')
  return login, password

def partPrompt():
  print 'Hello! These are the assignment parts that you can submit:'
  counter = 0
  for part in partFriendlyNames:
    counter += 1
    print str(counter) + ') ' + partFriendlyNames[counter - 1]
  partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
  return (partIdx, partIds[partIdx])

def getChallenge(email, sid):
  """Gets the challenge salt from the server. Returns (email,ch,state,ch_aux)."""
  url = challenge_url()
  values = {'email_address' : email, 'assignment_part_sid' : sid, 'response_encoding' : 'delim'}
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  text = response.read().strip()

  # text is of the form email|ch|signature
  splits = text.split('|')
  if(len(splits) != 9):
    print 'Badly formatted challenge response: %s' % text
    return None
  return (splits[2], splits[4], splits[6], splits[8])

def challengeResponse(email, passwd, challenge):
  sha1 = hashlib.sha1()
  sha1.update("".join([challenge, passwd])) # hash the first elements
  digest = sha1.hexdigest()
  strAnswer = ''
  for i in range(0, len(digest)):
    strAnswer = strAnswer + digest[i]
  return strAnswer 
  
def challenge_url():
  """Returns the challenge url."""
  return "https://class.coursera.org/" + URL + "/assignment/challenge"

def submit_url():
  """Returns the submission url."""
  return "https://class.coursera.org/" + URL + "/assignment/submit"

def submitSolution(email_address, ch_resp, sid, output, source, state, ch_aux):
  #print output
  #print source
  """Submits a solution to the server. Returns (result, string)."""
  source_64_msg = email.message.Message()
  source_64_msg.set_payload(source)
  email.encoders.encode_base64(source_64_msg)

  output_64_msg = email.message.Message()
  output_64_msg.set_payload(output)
  email.encoders.encode_base64(output_64_msg)
  values = { 'assignment_part_sid' : sid, \
             'email_address' : email_address, \
             'submission' : output_64_msg.get_payload(), \
             'submission_aux' : source_64_msg.get_payload(), \
             'challenge_response' : ch_resp, \
             'state' : state \
           }
  url = submit_url()  
  data = urllib.urlencode(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  string = response.read().strip()
  result = 0
  return result, string

## This collects the source code (just for logging purposes) 
def source(partIdx):
  # open the file, get all lines
  #f = open(sourceFiles[partIdx])
  #src = f.read() 
  #f.close()
  #return src
  return ''



############ BEGIN ASSIGNMENT SPECIFIC CODE - YOU'LL HAVE TO EDIT THIS ##############

import random
from providedcode import dataset
from providedcode.transitionparser import TransitionParser
from providedcode.evaluate import DependencyEvaluator
from featureextractor import FeatureExtractor
from transition import Transition

# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'nlpintro-001'

# the "Identifier" you used when creating the part
#partIds = ['degree-part-1', 'degree-part-2', 'degree-part-4']
partIds = ['hw2english', 'hw2danish','hw2swedish']
                     
# used to generate readable run-time information for students
partFriendlyNames = ['English Parser', 'Danish Parser', 'Swedish Parser'] 


# source files to collect (just for our records)
#sourceFiles = ['sampleStudentAnswer.py', 'sampleStudentAnswer.py', 'sampleStudentAnswer.py']
# what is purpose of this?                          
sourceFiles = []             

def evaluate_parse(partIdx):
  print 'Evaluating your model ... '
  if partIdx == 2:
    testdata = dataset.get_swedish_test_corpus().parsed_sents()
    if not os.path.exists('./swedish.model'):
      print 'No model. Please save your model as swedish.model at current directory before submission.'
      sys.exit(0)
    tp = TransitionParser.load('swedish.model')
    parsed = tp.parse(testdata)
    ev = DependencyEvaluator(testdata, parsed)
    uas, las = ev.eval()
    print 'UAS:',uas
    print 'LAS:',las
    swed_score = (min(las, 0.7) / 0.7) ** 2 * 25
    return swed_score
  
  if partIdx == 0:
    testdata = dataset.get_english_test_corpus().parsed_sents()
    if not os.path.exists('./english.model'):
      print 'No model. Please save your model as english.model at current directory before submission.'
      sys.exit(0)
    tp = TransitionParser.load('english.model')
    parsed = tp.parse(testdata)
    ev = DependencyEvaluator(testdata, parsed)
    uas, las = ev.eval()
    print 'UAS:',uas
    print 'LAS:',las
    eng_score = (min(las, 0.7) / 0.7) ** 2 * 50
    return eng_score
  
  if partIdx == 1:
    testdata = dataset.get_danish_test_corpus().parsed_sents()
    if not os.path.exists('./danish.model'):
      print 'No model. Please save your model danish.model at current directory before submission.'
      sys.exit(0)
    tp = TransitionParser.load('danish.model')
    parsed = tp.parse(testdata)
    ev = DependencyEvaluator(testdata, parsed)
    uas, las = ev.eval()
    print 'UAS:',uas
    print 'LAS:',las
    dan_score = (min(las, 0.7) / 0.7) ** 2 * 25
    return dan_score
 


def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = 'nlpfromumich'*100
  #outputString = ''
  outputString += str(int(round(evaluate_parse(partIdx))))
  #print outputString
  return outputString

submit()
