

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

import subprocess
# Make sure you change this string to the last segment of your class URL.
# For example, if your URL is https://class.coursera.org/pgm-2012-001-staging, set it to "pgm-2012-001-staging".
URL = 'nlpintro-001'

# the "Identifier" you used when creating the part
#partIds = ['degree-part-1', 'degree-part-2', 'degree-part-4']
partIds = ['hw3parta', 'hw3partb']
                     
# used to generate readable run-time information for students
partFriendlyNames = ['WSD Part A', 'WSD Part B'] 


# source files to collect (just for our records)
sourceFiles = []             


def evaluate(files,test_files,baselines,references,scores):

  score_total = 0
  for i in range(len(files)):
    f = files[i]
    baseline = baselines[i]
    reference = references[i]
    test_file = test_files[i]
    score = scores[i]
    if not os.path.exists(f):
      print 'Please save your output file', f, 'under Assignment3 directory.'
      continue
      
    command = "scorer2 " + f + " " + test_file
    print command
    
    #res = subprocess.check_output(command,shell = True)
    try:
      res = subprocess.check_output(command,shell = True)
    except Exception, e:
      res = None
      print 'scorer2 failed for',f
      sys.exit()

    #print res

    acc = 0
    if res:
      try:
        acc = float(res.split('\n')[2].split(' ')[2])
      except Exception, e:
        print 'scorer2 failed for',f
        sys.exit()

    print 'accuracy',acc,
    if acc < baseline:
      score_i = 0
    elif acc >= reference:
      score_i = score
    else:
      score_i = (score - score*(reference - acc)/(reference - baseline))

    score_total += score_i
    print 'score',score_i

  return score_total

def evaluate_wsd(partIdx):

  if partIdx == 0:
    files = ['KNN-English.answer','KNN-Spanish.answer','KNN-Catalan.answer','SVM-English.answer','SVM-Spanish.answer','SVM-Catalan.answer']
    #test_files = ['data/English-dev.key data/English.sensemap','data/Spanish-dev.key','data/Catalan-dev.key'] * 2
    test_files = ['data/English-dev.key','data/Spanish-dev.key','data/Catalan-dev.key'] * 2
    baselines = [0.535,0.684,0.678] * 2
    references = [0.550,0.690,0.705,0.605,0.785,0.805]
    scores = [10] * 6
    return evaluate(files,test_files,baselines,references,scores)
  elif partIdx == 1:
    files = ['Best-English.answer','Best-Spanish.answer','Best-Catalan.answer']
    #test_files = ['data/English-dev.key data/English.sensemap','data/Spanish-dev.key','data/Catalan-dev.key']
    test_files = ['data/English-dev.key','data/Spanish-dev.key','data/Catalan-dev.key']
    baselines = [0.605,0.785,0.805]
    references = [0.650,0.810,0.820]
    scores = [20,10,10]
    return evaluate(files,test_files,baselines,references,scores)


def output(partIdx):
  """Uses the student code to compute the output for test cases."""
  outputString = 'nlpfromumich'*100
  outputString += str(int(round(evaluate_wsd(partIdx))))
  return outputString

submit()
