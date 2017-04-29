from yowsup.stacks import  YowStackBuilder
from layer_send import SendLayer
from layer_bot import EchoLayer
from layer_bot_witai import WitaiLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
import ConfigParser
import sys
import getopt
import os

#####################################
#  Load Configuration Data
#####################################
cfgFile = './wassupbot.cfg'
print "Loading configuration from: %s" % cfgFile
config = ConfigParser.ConfigParser()
config.read(cfgFile)
phone = config.get('user', 'phone')
password = config.get('user', 'password')
chatbot_access_key = config.get('chatbot', 'witai_access_key')

credentials = (phone, password) 
stackBuilder = YowStackBuilder()

#####################################
#  Send a message
#####################################
def send(number, message):
    print ("Sending Message: number={}, message={}".format(number, message))    
    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(SendLayer)\
        .build()

    messages =  [([number, message])]    
    stack.setProp(SendLayer.PROP_MESSAGES, messages)
    stack.setCredentials(credentials)

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        stack.loop()
    except AuthError as e:
        print("Authentication Error: %s" % e.message) 
    except KeyboardInterrupt:
        print("\nMessage Sent")     

#####################################
#  Start the bot
#####################################
def startBot():
    print("\nStarting Up Chat Bot.") 
    stackBuilder = YowStackBuilder()

    # initialize wit.ai client
    witai = WitaiLayer()
    witai.setup(chatbot_access_key)

    #.push(EchoLayer)
    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(witai)\
        .build()

    print("Listening for messages using phone:{}".format(credentials[0]))    
    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal

    try:
        stack.loop(timeout = 0.5, discrete = 0.5)
    except AuthError as e:
        print("Auth Error, reason %s" % e)
    except KeyboardInterrupt:
        print("\nBot down now")   


#####################################
#             MAIN method
#####################################
def printUsage():
    print 'Usage:-'
    print ' run.py -c <command=send|bot> -n <number> -m <message> -u <user phone number> -p <password> -k <chat api access key>'
    print ' user phone number, password and key are required if not provided in the configuration file or as environment variables'
    print ' Environment variables supported: WA_PHONE, WA_PASSWORD, CHAT_ENGINE_KEY'
    print ' Example: run.py -c bot'
    sys.exit(2)

def main(argv):
    command=''
    number=''
    message=''
    global phone
    global password
    global chatbot_access_key
    global credentials

    #print("ENV: {}".format(os.environ))
    
    # Check environment variables for credentials first
    # these can override configuration file but
    # the command line can override these 
    if os.environ.get('WA_PHONE') != None:
        phone = os.environ.get('WA_PHONE')
    if os.environ.get('WA_PASSWORD') != None:
        password = os.environ.get('WA_PASSWORD')
    if os.environ.get('CHAT_ENGINE_KEY') != None:
        chatbot_access_key = os.environ.get('CHAT_ENGINE_KEY')

    try:
        opts, args = getopt.getopt(argv,"c:n:m:u:p:k:",["command=","number=","message="])
    except getopt.GetoptError:
        printUsage()

    for opt, arg in opts:
        if opt == '-h':
            printUsage()
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-n", "--number"):
            number = arg
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-u", "--userphone"):
            phone = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-k", "--key"):
            chatbot_access_key = arg

    print ("command={}, number={}, message={}".format(command, number, message))    

    credentials = (phone, password) 
    
    if command == 'send':
        if number == '' or message == '':
            print "Missing arguments"
            sys.exit(3)
        send(number, message)      
    elif command == 'bot':
        startBot()
    else:
        print ("Unknown command specified '{}'".format(command)) 
        printUsage()   

if __name__==  "__main__": 
    main(sys.argv[1:])
