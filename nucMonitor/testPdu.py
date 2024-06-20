from pduSsh import PDU

pdu = PDU("10.68.17.123", "apc", "apc")
print(pdu.getOutletPower(6))
pdu.close()
