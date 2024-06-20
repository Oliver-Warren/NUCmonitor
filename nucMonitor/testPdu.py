from PDU import *

pdu = PDU(PDU_IP, PDU_UN, PDU_PW)
print(pdu.getOutletPower(PDU_OL))
pdu.close()
