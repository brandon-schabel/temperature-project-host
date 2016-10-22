import sys
import glob
import serial

def connect_to_arduino():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    serialPorts = result
    print(serialPorts)
    checkUserInput = False
    chosenPort = ''
    choosePortNum = ''
    
    while checkUserInput == False:
        print(str(len(serialPorts)) + " found")
        
        for i in range(0,len(serialPorts)):
            print("[" + str(i) + "] "  + serialPorts[i])
            
        if(len(serialPorts) == 1):
            chosenPort = serialPorts[0]
            checkUserInput = True
            print(chosenPort + " Found")
        else:
            choosePortNum = input("Choose Port Number using indexes above.")
            if(int(choosePortNum) <= (len(serialPorts) - 1)):
                chosenPort = serialPorts[int(choosePortNum)]
                checkUserInput = True
                print(chosenPort + " Found")
            else:
                print("That port didn't work, please try again.")

    return chosenPort
