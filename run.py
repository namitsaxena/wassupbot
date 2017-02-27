from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv
import ConfigParser


# load the configuration file
cfgFile = './wassupbot.cfg'
print "Loading configuration from: %s" % cfgFile
config = ConfigParser.ConfigParser()
config.read(cfgFile)
phone = config.get('user', 'phone')
password = config.get('user', 'password')
print "User Phone: %s" % phone

credentials = (phone, password) 

if __name__==  "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
    stack.loop() #this is the program mainloop