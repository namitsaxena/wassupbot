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

            if messageProtocolEntity.getType() == 'media':
                self.onMediaMessage(messageProtocolEntity)
                outgoingMessageProtocolEntity = TextMessageProtocolEntity("Received Media File. Thanks", "", to = messageProtocolEntity.getFrom())
            else:
                print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
                if messageProtocolEntity.getBody().lower() == "bye":
                    print "ok bye..."
                    outgoingMessageProtocolEntity = TextMessageProtocolEntity("ok bye bye..", to = messageProtocolEntity.getFrom())
                else:    
                    outgoingMessageProtocolEntity = TextMessageProtocolEntity(messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom())
            
            print "message type %s" % messageProtocolEntity.getType()           
                

            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

            # if messageProtocolEntity.getBody().lower() == "bye":
            #     sys.exit(0) 




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
