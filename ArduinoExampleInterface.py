import pyfirmata
import time

class MotorController():
  def __init__(self):
    self.arduinoPort = '/dev/cu.usbmodem141101'
    self.arduinoBoard = pyfirmata.Arduino(self.arduinoPort)
    self.leftEyeTheta = 0
    self.leftEyePhi = 0
    self.rightEyeTheta = 0
    self.rightEyePhi = 0
    self.maxDegree = 180
    it = pyfirmata.util.Iterator(self.arduinoBoard)
    it.start()
    self.leftEyeThetaServo = self.arduinoBoard.get_pin('d:5:s')
    self.leftEyePhiServo = self.arduinoBoard.get_pin('d:6:s')
    self.rightEyeThetaServo = self.arduinoBoard.get_pin('d:10:s')
    self.rightEyePhiServo = self.arduinoBoard.get_pin('d:11:s')
    

  def test(self):
   
    while True:
      self.leftEyePhiServo.write(0)
      time.sleep(2)
      self.leftEyePhiServo.write(180)
      time.sleep(2)
      # self.arduinoBoard.digital[13].write(1)
      # time.sleep(2)
      # self.arduinoBoard.digital[13].write(0)
      # time.sleep(2)

  def LeftEyeThetaController(self, theta):
    self.leftEyeThetaServo.write(theta)
    pass

  def LeftEyePhiController(self, phi):
    self.leftEyePhiServo.write(phi)
  
  def RightEyeThetaController(self):
    pass
  
  def RightEyePhiController(self):
    pass

if __name__ == '__main__':
  Motor = MotorController()
  #Motor.test()

  