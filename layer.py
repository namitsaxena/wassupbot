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

            # if messageProtocolEntity.getType() == 'text':
            #     self.onTextMessage(messageProtocolEntity)
            
            outgoingMessageProtocolEntity = TextMessageProtocolEntity(messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom())

            print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
            if messageProtocolEntity.getBody().lower() == "bye":
                print "ok bye..."
                outgoingMessageProtocolEntity = TextMessageProtocolEntity("ok bye bye..", messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom())


            self.toLower(receipt)
            self.toLower(outgoingMessageProtocolEntity)

            # if messageProtocolEntity.getBody().lower() == "bye":
            #     sys.exit(0) 




    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", entity.getType(), entity.getFrom())
        self.toLower(ack)


    # def onTextMessage(self,messageProtocolEntity):
    #     # just print info
    #     print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))  
    #     if messageProtocolEntity.getBody().__str__() == "bye":
    #         print "ok bye......"
    #         outgoingMessageProtocolEntity = TextMessageProtocolEntity("ok bye..", messageProtocolEntity.getBody(), to = messageProtocolEntity.getFrom())
