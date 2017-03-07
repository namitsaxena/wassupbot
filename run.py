from yowsup.stacks import  YowStackBuilder
from layer_send import SendLayer
from layer_bot import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
import ConfigParser
import sys
import getopt

#####################################
#  Load Configuration Data
#####################################
cfgFile = './wassupbot.cfg'
print "Loading configuration from: %s" % cfgFile
config = ConfigParser.ConfigParser()
config.read(cfgFile)
phone = config.get('user', 'phone')
password = config.get('user', 'password')
print "Starting up using user phone: %s" % phone

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
    print("\nStarting Up Echo Bot. \nListening for incoming messages.... ") 
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

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

def main(argv):
    command=''
    number=''
    message=''

    try:
        opts, args = getopt.getopt(argv,"c:n:m:",["command=","number=","message="])
    except getopt.GetoptError:
        print 'run.py -c <command=send|bot> -n <number> -m <message>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'run.py -c <command> -n <number> -m <message>'
            sys.exit()
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-n", "--number"):
            number = arg
        elif opt in ("-m", "--message"):
            message = arg

    print ("command={}, number={}, message={}".format(command, number, message))    
    
    if command == 'send':
        if number == '' or message == '':
            print "Missing arguments"
            sys.exit(3)
        send(number, message)      
    elif command == 'bot':
        startBot()
    else:
        print ("Unknown command specified '{}'".format(command))    

if __name__==  "__main__": 
    main(sys.argv[1:])
