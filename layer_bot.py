from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity
# import sys

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        #send receipt otherwise we keep receiving the same message over and over

        if True:
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom(), 'read', messageProtocolEntity.getParticipant())

            #print ("Message received of type: %s" % messageProtocolEntity.getType()) 

            if messageProtocolEntity.getType() == 'text':
                print("'%s' <-- %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

                msg = messageProtocolEntity.getBody()
                reply = self.getReply(msg)

                print("  > '%s' --> %s" % (reply, messageProtocolEntity.getFrom(False)))

                outgoingMessageProtocolEntity = TextMessageProtocolEntity(reply, to = messageProtocolEntity.getFrom())                       
            elif messageProtocolEntity.getType() == 'media':
                self.onMediaMessage(messageProtocolEntity)
                outgoingMessageProtocolEntity = TextMessageProtocolEntity("Received Media File. Thanks", "", to = messageProtocolEntity.getFrom())
            else:
                outgoingMessageProtocolEntity = TextMessageProtocolEntity("I couldn't understand.", to = messageProtocolEntity.getFrom())
                

            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

            # if messageProtocolEntity.getBody().lower() == "bye":
            #     sys.exit(0) 

    def getReply(self, message):
        msg = message.lower()
        reply = ""

        if msg == "hi":
            reply = "Hi, How are you"
        elif msg == "hello":
            reply = "Hello, How are you"
        elif msg == "bye":
            reply = "ok bye, ttyl"
        elif msg == "shutup":
            reply = "You shutup!!!" + '\U0001F600'.decode('unicode-escape') 
        elif '\U0001F600'.decode('unicode-escape') in msg \
            or '\U0001F601'.decode('unicode-escape') in msg \
            or '\U0001F602'.decode('unicode-escape') in msg \
            or '\U0001F603'.decode('unicode-escape') in msg \
            or '\U0001F604'.decode('unicode-escape') in msg \
            or '\U0001F605'.decode('unicode-escape') in msg \
            or '\U0001F606'.decode('unicode-escape') in msg \
            or '\U0001F923'.decode('unicode-escape') in msg:
            reply = '\U0001F600'.decode('unicode-escape')  + '\U0001F601'.decode('unicode-escape') 
        else:
            reply = message       
        return reply   


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)


    # this can handle only simple ascii it seems and not emoji/unicode    
    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))  
        if messageProtocolEntity.getBody().__str__() == "bye":
            print "ok bye......"
            outgoingMessageProtocolEntity = TextMessageProtocolEntity("ok bye..", messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom())

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
