import g4p_controls.*;
import processing.serial.*;

float q0 = 0.0F; float q1 = 0.0F; float q2 = 0.0F; float q3 = 0.0F; // Quaternions

float roll  = 0.0F;
float pitch = 0.0F;
float yaw   = 0.0F;
float temp  = 0.0F;
float alt   = 0.0F;

float indexFingerDeg = 0.0F; float indexKnuckleDeg = 0.0F;
float middleFingerDeg = 0.0F; float middleKnuckleDeg = 0.0F;
float ringFingerDeg = 0.0F; float ringKnuckleDeg = 0.0F;
float pinkieFingerDeg = 0.0F;


float xacc = 0.0F; float xvel = 0.0F; float x = 0.0F;
float yacc = 0.0F; float yvel = 0.0F; float y = 0.0F;
float zacc = 0.0F; float zvel = 0.0F; float z = 0.0F;
float thresh = 0.0F; 

// Serial port state.
Serial       port;
final String serialConfigFile = "serialconfig.txt";
boolean      printSerial = false;

void setup()
{
  size(1280, 960, P3D);
  createGUI();
  frameRate(50);
  
  // Serial port setup.
  String[] serialConfig = loadStrings(serialConfigFile);
  print(serialConfig);
  setSerialPort("COM5");
}
 
void draw()
{
  background(245,238,184);

  // Set a new co-ordinate space
  pushMatrix();
    
  // orthographic projection
  //ortho(-width/2, width/2, -height/2, height/2); 
  
  // calculate displacement
  //thresh = 0.2;
  //if (abs(yacc) > thresh) {yvel = yvel + yacc;}
  //if (abs(yvel) > thresh) {y = y + yvel;}
  
  // Move hand from 0,0 in top left to center of screen.
  translate(width/2+y,height/2,0);
  
  // Rotate shapes around the X/Y/Z axis
  rotateX(pitch);
  rotateY(yaw);
  rotateZ(roll);
  
  lbl_title.setText("Hand");
  
  //noStroke();
  drawHand();
    
  popMatrix();
  //print("draw");
}

void serialEvent(Serial p) 
{
  String incoming = p.readString();
  println(incoming);
  if ((incoming.length() > 8))
  {
    String[] list = splitTokens(incoming); //splits by whitespace characters //<>//
    if ( list.length > 1)  
    {  
      if ( list[0].equals("Alt:") ) 
      {
        alt  = float(list[1]);
      }
      if ( list[0].equals("Temp:") ) 
      {
        temp  = float(list[1]);
      }
      
      // Calibration Values
      if ( list[0].equals("System:") )
      {
        int sysCal   = int(list[1]);
        int gyroCal  = int(list[3]);
        int accelCal = int(list[5]);
        int magCal   = int(list[7]);
      }
      
      // Fingers Part 1
      if ( list[0].equals("Index:") )
      {
       indexFingerDeg  = float(list[1]);
       middleFingerDeg = float(list[3]);
       ringFingerDeg = float(list[5]);
       pinkieFingerDeg = float(list[7]);
      }
      // Fingers Part 2
      if ( list[0].equals("IndexKnuckle:") )
      {
        indexKnuckleDeg = float(list[1]);
        middleKnuckleDeg = float(list[3]);
        ringKnuckleDeg = float(list[5]);
      }
      
      // Quaternions
      if ( list[0].equals("qW:") )
      {
        q0 = float(list[1]);
        q1 = float(list[3]);
        q2 = float(list[5]);
        q3 = float(list[7]);
        
        // Angle calculation from quaternions
        if (!(abs(q1*q2+q0*q3)==0.5))
        {  
          pitch = atan2(2*q2*q0-2*q1*q3,1-2*q2*q2-2*q3*q3);
          yaw = asin(2*q1*q2+2*q3*q0);
          roll = atan2(2*q1*q0-2*q2*q3,1-2*q1*q1-2*q3*q3);
        }
        else if (q1*q2+q0*q3 > 0)
        {
          pitch = 2*atan2(q1,q0);
          roll = 0.0F;
        }
        else
        {
          pitch = -2*atan2(q1,q0);
          roll = 0.0F;
        }
      }
      
      // Linear Acceleration
      if (list[0].equals("aX:"))
      {
        xacc = float(list[1]);
        yacc = float(list[3]);
        zacc = float(list[5]);
      }
    }
  }
}

// Set serial port to desired value.
void setSerialPort(String portName) {
  // Close the port if it's currently open.
  if (port != null) {
    port.stop();
  }
  try {
    // Open port.
    port = new Serial(this, portName, 115200);
    port.bufferUntil('\n');
    // Persist port in configuration.
    // saveStrings(serialConfigFile, new String[] { portName });
  }
  catch (RuntimeException ex) {
    // Swallow error if port can't be opened, keep port closed.
    port = null; 
  }
}

void drawHand() {
  // yellow palm
  fill(246, 225, 65);
  box(200,60,150);
  
  // white fingers
  fill(255, 255, 255);
  
  // index finger
  translate(-80,0,-75);
  rotateX(radians(indexKnuckleDeg));
  translate(0,0,-60);
  box(40,60,120);
  translate(0,0,-60);
  rotateX(radians(indexFingerDeg));
  translate(0,0,-50);
  box(40,60,100);
  translate(0,0,50);
  rotateX(radians(-indexFingerDeg));
  translate(0,0,60);
  translate(0,0,60);
  rotateX(radians(-indexKnuckleDeg));
  translate(50,0,20);
    
  // middle finger
  translate(0,0,-20);
  rotateX(radians(middleKnuckleDeg));
  translate(0,0,-70);
  box(40,60,140);
  translate(0,0,-70);
  rotateX(radians(middleFingerDeg));
  translate(0,0,-60);
  box(40,60,120);
  translate(0,0,60);
  rotateX(radians(-middleFingerDeg));
  translate(0,0,70);
  translate(0,0,70);
  rotateX(radians(-middleKnuckleDeg));
  translate(50,0,70);
  
  // ring finger
  translate(0,0,-70);
  rotateX(radians(ringKnuckleDeg));
  translate(0,0,-60);
  box(40,60,120);
  translate(0,0,-60);
  rotateX(radians(ringFingerDeg));
  translate(0,0,-50);
  box(40,60,100);
  translate(0,0,50);
  rotateX(radians(-ringFingerDeg));
  translate(0,0,60);
  translate(0,0,60);
  rotateX(radians(-ringKnuckleDeg));
  translate(50,0,70);
  
  // pinkie finger
  translate(0,0,-110);
  box(40,60,80);
  translate(0,0,-40);
  rotateX(radians(pinkieFingerDeg));
  translate(0,0,-35);
  box(40,60,70);
  translate(0,0,35);
  rotateX(radians(-pinkieFingerDeg));
}

void calibrate_hand() {
  // use rotation matrices!
}