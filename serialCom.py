import serial
import time

CMD_LINEBREAK = b'\r\n'

# Serial port config
PORT = "COM3"
BAUD = 115200

# Serial functions
def send(data):
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        ser.write(data)

def send_cmd(cmd):
    send(cmd.encode('utf-8') + CMD_LINEBREAK)

def watch(timeout=10, success=None, failure=None, echo_cmd=None):
    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        t_start = time.time()
        reply = list()
        while True:
            if ser.in_waiting:
                line = ser.readline()
                echo = False
                if echo_cmd:
                    echo = line.decode('utf-8').strip().endswith(echo_cmd)
                if line != CMD_LINEBREAK and not echo:
                    line = line.decode('utf-8').strip()
                    reply.append('\t' + line)
                    if success and line.startswith(success):
                        return ("Success", reply, time.time()-t_start)
                    if failure and line.startswith(failure):
                        return ("Error", reply, time.time()-t_start)
            if (time.time()-t_start) > timeout:
                return ("Timeout", reply, time.time()-t_start)
            time.sleep(0.02)

def AT(cmd="", timeout=10, success="OK", failure="+CME ERROR"):
    cmd = 'AT' + cmd
    print("----------- ", cmd, " -----------")
    send_cmd(cmd)
    reply = watch(echo_cmd=cmd, timeout=timeout, success=success, failure=failure)
    print("{0} ({1:.2f}secs):".format(reply[0], reply[2]))
    print(*reply[1], sep='\n')
    print('')
    return reply