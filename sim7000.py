import sys
import os
from serialCom import *
from datetime import datetime


# If there is no CAT-M and NB-Iot avaliable GPRS is used
# There is no way to get the APN using GPRS
APN = "internet.movistar.com.co" 
# Deppending on the carrier 

# Mosquitto.org Settings
MQTT_URL="test.mosquitto.org"
CERTS_FOLDER = 'certs'
CA_NAME = 'mosquitto-ca.crt'
CERT_NAME = "mosquitto.crt"
KEY_NAME = "mosquitto.key"





###### STATUS

# AT+CBC



# Restart board
if "--reboot" in sys.argv:
    AT('+CFUN=1,1', timeout=30, success="*PSUTTZ") 

# # GLOSSARY
# ME, MS, TA, DCE -> GSM modem
# TE, DTE -> Controller


########################### HARDWARE FEATURES ###########################

# # Check module is responding
# AT()  

# # Check if SIM card is present and active
# # If SIM card is not present on start up URC +CPIN: NOT INSERTED
# # ERROR -> SIM not present or error in SIM
# # READY -> Not pending for any password
# # SIM PIN -> Waiting SIM PIN to be given
# # SIM PUK -> Waiting SIM PUK to be given
# AT('+CPIN?')

# # Enter a solicited PIN or PUK
# AT('+CPIN=<pin>')  

## Set VBAT checking feature ON/OFF
# AT('+CBATCHK?') # Check VBAT ON/OFF
# AT('+CBATCHK=1') # VBAT OFF
# AT('+CBATCHK?') # VBAT ON

# # Set DCD (circuit 109) Function Mode
# AT('&C0')  # DCD line is always ON
# AT('&C1')  # DCD line is ON only if data carrier present (Default)


########################### GENERAL INFORMATION ###########################
# Get IMEI
# AT('+GSN') 

# # Request ME model identification 
# AT('+CGMM') 

# # Request ME firmware version
# AT('+CGMR')

# # Request ME serial number identification
# AT('+CGSN')


########################### USART CONFIGURATION ###########################
# # TE-TA Framing 
# AT('+ICF=3,3')  # 8 data 0 parity 1 stop (Default)

# # TE-TA Data flow control
# - AT('+IFC=<dce_by_dte>,<dte_by_dce>')

# # TE-TA baud rate (Auto_Save)
# AT('+IPR=115200')  # (Default)   

###### INDEX ######
# # <dce_by_dte> Specifies the method will be used by TE at receive of data from TA
# # 0 No flow control (Default)
# # 1 Software flow control
# # 2 Hardware flow control

# # <dte_by_dce> Specifies the method will be used by TA at receive of data from TE
# # 0 No flow control (Default)
# # 1 Software flow control
# # 2 Hardware flow control

########################### RESPONCE FORMAT ###########################

# # Set command Echo mode
# AT('E0')  # Turn off
# AT('E1')  # Turn on (Default)

# # Result code presentation mode
# AT('Q0')  # Show result codes (Default)
# AT('Q1')  # Do not show result codes

# # Select TE character set
# # (Default) "IRA" International reference alphabet (ITU-T T.50)
# AT('+CSCS="IRA"') 

# # Define report mobile equipment error
# AT('+CMEE=0') # Just report ERROR 
# AT('+CMEE=1') # Report the numeric error
# AT('+CMEE=2') # Report the numeric error and verbose description

########################### SIGNAL INFORMATION ###########################

# # Signal level, range: -53 dbm (Exelent) to -109 dbm (Marginal)
# AT("+CSQ") # Get signal strength

# # Get detailed signal info
# AT('+CPSI?') 
# # If camping on a gsm cell: +CPSI: <System Mode>,<Operation Mode>,<MCC>-<MNC>,<LAC>,<Cell ID>,<Absolute RF Ch Num>,<RxLev>,<Track LO Adjust>,<C1-C2>
# # If camping on a CAT-M or NB-IOT cell: +CPSI: <System Mode>,<Operation Mode>,<MCC>-<MNC>,<TAC>,<SCellID>,<PCellID>,<Frequency Band>,<earfcn>,<dlbw>,<ulbw>,<RSRQ>,<RSRP>,<RSSI>,<RSSNR> 

########################### NETWORK PREFERENCES ###########################

# # Preferred Mode Selection (Auto_Save)
# AT('+CNMP=2')   # Automatic
# AT('+CNMP=13')  # GSM only
# AT('+CNMP=38')  # LTE only
# AT('+CNMP=51')  # GSM and LTE only 

# # Set preference for nb-iot between CAT-M and NB-Iot (Auto_Save)
# AT('+CMNB=1')  # CAT-M
# AT('+CMNB=2')  # NB-Iot  
# AT('+CMNB=3')  # CAT-M and NB-Iot

########################### NETWORK CONFIGURATION ###########################

# # Preferred operator list
# # Response:
# # +CPOL: <index1>,<format>,<oper1>[,<GSM>,<GSM_compact>,<UTRAN>,<E-UTRAN>]
# # [<CR><LF>+CPOL:<index2>,<format>,<oper2>[,<GSM,<GSM_compact>,<UTRAN>,<E-UTRAN>][…]]
# AT('+CPOL?')

# # Operator Selection
# # TA returns the current mode and the currently selected operator. If no operator is selected,<format> and <oper> are omitted. +COPS: <mode>[,<format>,<oper>,<netact>]
# AT('+COPS?')

# # Force opperator selection (Auto_Save)
# # TA forces an attempt to select and register the GSM network operator. If the selected operator is not available, no other operator shall be selected (except <mode>=4).
# - AT('+COPS=<mode>,<format>,<oper>')

# # Network registration
# # TA returns the status of result code presentation and an integer <stat> which shows whether the network has currently indicated the registration of the ME. Location information elements <lac> and <ci> are returned only when <n>=2 and ME is registered in the network.+CREG: <n>,<stat>[,<lac>,<ci>,<netact>]
# AT("+CGREG?")

# # Network registration URC
# TA controls the presentation of an unsolicited result code when there is a change in the ME network registration status.
# - AT('+CREG=<n>')


###### INDEX ######
# # <mode> 
# # 0 Automatic mode; <oper> field is ignored (Default)
# # 1 Manual (<oper> field shall be present, and <AcT> optionally)
# # 2 manual deregister from network
# # 3 set only <format> (for read Command +COPS?) - not shown in Read Command response
# # 4 Manual/automatic (<oper> field shall be present); if manual selection fails, automatic mode (<mode>=0) is entered

# # <format> 
# # 0 Long format alphanumeric <oper> (Default)
# # 1 Short format alphanumeric <oper>
# # 2 Numeric <oper>;

# # <oper> 
# # Refer to [27.007] operator in format as per <format>

# # <index> 
# # Integer type: order number of operator in SIM preferred operator list

# # <GSM> GSM access technology
# # 0 Access technology is not selected
# # 1 Access technology is selected

# # <GSM_compact> GSM compact access technology
# # 0 Access technology is not selected
# # 1 Access technology is selected

# # <UTRAN> UTRAN access technology
# # 0 Access technology is not selected
# # 1 Access technology is selected

# # <E-UTRAN> E-UTRAN access technology
# # 0 Access technology is not selected
# # 1 Access technology is selected

# # <n> 
# # 0 Disable network registration unsolicited result code (Default)
# # 1 Enable network registration unsolicited result code +CREG: <stat>
# # 2 Enable network registration unsolicited result code with location information (2 is only for 7000 series module which support GPRS.) CREG: <stat>[,<lac>,<ci>,<netact>]

# # <stat> 
# # 0 Not registered, MT is not currently searching a new operator to register to
# # 1 Registered, home network
# # 2 Not registered, but MT is currently searching a new operator to register to
# # 3 Registration denied
# # 4 Unknown
# # 5 Registered, roaming

# # <netact> 
# # 0 User-specified GSM access technology
# # 1 GSM compact
# # 3 GSM EGPRS
# # 7 User-specified LTE M1 A GB access technology
# # 9 User-specified LTE NB S1 access technology

# # <lac> String type (string should be included in quotation marks); two byte location area code in hexadecimal format

# # <ci> String type (string should be included in quotation marks); two byte cell ID in hexadecimal format

########################### LOCAL TIME ###########################

# # Get system time
# AT('+CCLK?') 

# # Set system time (Auto_Save)
# - AT('+CCLK=<time>')

###### INDEX ######
# <time> 
# String type(string should be included in quotation marks) value;
# format is "yy/MM/dd,hh:mm:ss±zz", where characters indicate year (two last
# digits),month, day, hour, minutes, seconds and time zone (indicates the
# difference, expressed in quarters of an hour, between the local time and
# GMT; range -47...+48). E.g. 6th of May 2010, 00:01:52 GMT+2 hours
# equals to "10/05/06,00:01:52+08".


########################### PHONE ###########################

# # Check phone activity status
# AT("+CPAS") 
# # 0 -> Ready
# # 3 -> Ringing
# # 4 -> Call in progress

# # Set Cellular Result Codes for Incoming Call Indication
# AT('+CRC=0')  # Disable extended format
# AT('+CRC=1')  # Enable extended format






# AT("+CGACT?") # Show PDP context state

# AT('+CGPADDR') # Show PDP address

# cgcontrdp = AT("+CGCONTRDP") # Get APN and IP address
# Check nb-iot Status
# AT('+CGNAPN')

# AT('+CBAND?') # Get band





############################### PING/NTP ##################################

# Ping - works :-)
if sys.argv[1] == "ping":
    print("++++++++++++++++++++ PING +++++++++++++++++++++\n")
    AT('+CSTT="{}"'.format(APN))
    AT('+CIICR')
    AT('+CIFSR')
    AT('+CIPPING="www.google.com"')

# Get NTP time - working :-)
if sys.argv[1] == "ntp":
    print("++++++++++++++++++++ NTP +++++++++++++++++++++\n")
    AT('+SAPBR=3,1,"APN","{}"'.format(APN))
    AT('+SAPBR=1,1')
    AT('+SAPBR=2,1')
    AT('+CNTP="pool.ntp.org",0,1,1')
    AT('+CNTP', timeout=3, success="+CNTP")
    AT('+SAPBR=0,1')

############################### HTTP/MQTT ##################################

# HTTP Get example - working :-)
if sys.argv[1] == "http1":
    print("++++++++++++++++++++ HTTP1 +++++++++++++++++++++\n")
    AT('+SAPBR=3,1,"APN","{}"'.format(APN))
    AT('+SAPBR=1,1')
    AT('+SAPBR=2,1')
    AT('+HTTPINIT')
    AT('+HTTPPARA="CID",1')
    AT('+HTTPPARA="URL","http://minimi.ukfit.webfactional.com"')
    AT('+HTTPACTION=0', timeout=30, success="+HTTPACTION: 0,200")
    AT('+HTTPREAD')
    AT('+HTTPTERM')
    AT('+SAPBR=0,1')

# HTTP Get example - Working :-)
if sys.argv[1] == "http2":
    print("++++++++++++++++++++ HTTP2 +++++++++++++++++++++\n")
    AT('+CNACT=1')
    AT("+CNACT?")
    AT('+SHCONF="URL","http://minimi.ukfit.webfactional.com"')
    AT('+SHCONF="BODYLEN",350')
    AT('+SHCONF="HEADERLEN",350')
    AT('+SHCONN',timeout=30, success="OK")
    AT('+SHSTATE?')
    AT('+SHREQ="http://minimi.ukfit.webfactional.com",1', timeout=30, success="+SHREQ:")
    AT('+SHREAD=0,1199', timeout=30, success="</html>")
    AT('+SHDISC')

# MQTT (No SSL) - Working :-)
if sys.argv[1] == "mqtt-nossl":
    print("++++++++++++++++++++ MQTT - NO SSL +++++++++++++++++++++\n")
    AT("+CNACT=1") # Open wireless connection
    AT("+CNACT?") # Check connection open and have IP
    AT('+SMCONF="CLIENTID",1233')
    AT('+SMCONF="KEEPTIME",60') # Set the MQTT connection time (timeout?)
    AT('+SMCONF="CLEANSS",1')
    AT('+SMCONF="URL","{}","1883"'.format(MQTT_URL)) # Set MQTT address
    smstate = AT('+SMSTATE?') # Check MQTT connection state
    if smstate[1][0].split(":")[1].strip() == "0":
        AT('+SMCONN', timeout=30) # Connect to MQTT
    msg = "Hello Moto {}".format(datetime.now())
    AT('+SMPUB="test001","{}",1,1'.format(len(msg)), timeout=30, success=">") # Publish command
    send(msg.encode('utf-8'))
    watch(timeout=10)
    #AT('+SMSUB="test1234",1')
    AT('+SMDISC') # Disconnect MQTT
    AT("+CNACT=0") # Close wireless connection

############################### SSL/TLS ##################################

# Check certs on device - working :-)
if sys.argv[1] == "certs-check":
    print("++++++++++++++++++++ CERTS - CHECK +++++++++++++++++++++\n")
    AT('+CFSINIT')
    AT('+CFSGFIS=3,"{}"'.format(CA_NAME))
    AT('+CFSGFIS=3,"{}"'.format(CERT_NAME))
    AT('+CFSGFIS=3,"{}"'.format(KEY_NAME))
    AT('+CFSTERM')

# Delete certs on device - working :-)
if sys.argv[1] == "certs-delete":
    print("++++++++++++++++++++ CERTS - DELETE +++++++++++++++++++++\n")
    AT('+CFSINIT')
    AT('+CFSDFILE=3,"{}"'.format(CA_NAME))
    AT('+CFSDFILE=3,"{}"'.format(CERT_NAME))
    AT('+CFSDFILE=3,"{}"'.format(KEY_NAME))
    AT('+CFSTERM')

# Load a cert from a file on computer - working :-)
if sys.argv[1] == "certs-load":
    print("++++++++++++++++++++ CERTS - LOAD +++++++++++++++++++++\n")
    AT('+CFSINIT')
    with open(os.path.join(CERTS_FOLDER, CA_NAME),'rb') as f:
        data = f.read()
        AT('+CFSWFILE=3,"{}",0,{},5000'.format(CA_NAME, len(data)), success="DOWNLOAD")
        send(data)
    with open(os.path.join(CERTS_FOLDER, CERT_NAME),'rb') as f:
        data = f.read()
        AT('+CFSWFILE=3,"{}",0,{},5000'.format(CERT_NAME, len(data)), success="DOWNLOAD")
        send(data)
    with open(os.path.join(CERTS_FOLDER, KEY_NAME),'rb') as f:
        data = f.read()
        AT('+CFSWFILE=3,"{}",0,{},5000'.format(KEY_NAME, len(data)), success="DOWNLOAD")
        send(data)
    AT('+CFSTERM')

# MQTT (SSL) - No client cert, working for Mosquitto.org :-(
if sys.argv[1] == "mqtt-cacert":
    print("++++++++++++++++++++ MQTT - CA Cert Only +++++++++++++++++++++\n")
    AT("+CNACT=1") # Open wireless connection
    AT("+CNACT?") # Check connection open and have IP
    AT('+SMCONF="CLIENTID", "TOMTEST01"')
    AT('+SMCONF="KEEPTIME",60') # Set the MQTT connection time (timeout?)
    AT('+SMCONF="CLEANSS",1')
    AT('+SMCONF="URL","{}","8883"'.format(MQTT_URL)) # Set MQTT address
    AT('+CSSLCFG="ctxindex", 0') # Use index 1
    AT('+CSSLCFG="sslversion",0,3') # TLS 1.2
    AT('+CSSLCFG="convert",2,"{}"'.format(CA_NAME))
    AT('+SMSSL=0, {}'.format(CA_NAME))
    AT('+SMSSL?')
    AT('+SMSTATE?') # Check MQTT connection state
    AT('+SMCONN', timeout=60, success="OK") # Connect to MQTT
    AT('+SMSTATE?', timeout=5) # Check MQTT connection state
    msg = "Hello Moto {}".format(datetime.now())
    AT('+SMPUB="test002","{}",1,1'.format(len(msg))) # Publish command
    send(msg.encode('utf-8'))
    #AT('+SMSUB="test1234",1')
    AT('+SMDISC') # Connect to MQTT

# MQTT (SSL) - CA and client certs, working for Mosquitto.org :-(
if sys.argv[1] == "mqtt-bothcerts":
    print("++++++++++++++++++++ MQTT - CA and Client Cert +++++++++++++++++++++\n")
    AT("+CNACT=1") # Open wireless connection
    AT("+CNACT?") # Check connection open and have IP
    AT('+SMCONF="CLIENTID", "TOMTEST01"')
    AT('+SMCONF="KEEPTIME",60') # Set the MQTT connection time (timeout?)
    AT('+SMCONF="CLEANSS",1')
    AT('+SMCONF="URL","{}","8884"'.format(MQTT_URL)) # Set MQTT address
    AT('+CSSLCFG="ctxindex", 0') # Use index 1
    AT('+CSSLCFG="sslversion",0,3') # TLS 1.2
    AT('+CSSLCFG="convert",2,"{}"'.format(CA_NAME))
    AT('+CSSLCFG="convert",1,"{}","{}"'.format(CERT_NAME, KEY_NAME))
    AT('+SMSSL=1, {}, {}'.format(CA_NAME, CERT_NAME))
    AT('+SMSSL?')
    AT('+SMSTATE?') # Check MQTT connection state
    AT('+SMCONN', timeout=60, success="OK") # Connect to MQTT, this can take a while
    AT('+SMSTATE?', timeout=5) # Check MQTT connection state
    msg = "Hello Moto {}".format(datetime.now())
    AT('+SMPUB="test001","{}",1,1'.format(len(msg)), success=">") # Publish command
    send(msg.encode('utf-8'))
    watch(timeout=10)
    #AT('+SMSUB="test1234",1')
    AT('+SMDISC') # Connect to MQTT

