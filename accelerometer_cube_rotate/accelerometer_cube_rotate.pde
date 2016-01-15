import g4p_controls.*;
import processing.serial.*;

float q0 = 0.0F; float q1 = 0.0F; float q2 = 0.0F; float q3 = 0.0F; // Quaternions

float roll  = 0.0F; float rollOffset = 0.0F;
float pitch = 0.0F; float pitchOffset = 0.0F;
float yaw   = 0.0F; float yawOffset = 0.0F;
float temp  = 0.0F;
float alt   = 0.0F;

float indexFingerDeg = 0.0F;
float middleFingerDeg = 0.0F;
float ringFingerDeg = 0.0F;


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
  setSerialPort(serialConfig[0]);
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
  
  // Rotate shapes around the X/Y/Z axis (values in radians, 0..Pi*2)
  rotateX(-pitch + pitchOffset);
  rotateY(yaw - yawOffset);
  rotateZ(-roll + rollOffset);
  
  lbl_title.setText(str((pitch)));
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
    String[] list = split(incoming, " ");
    //if ( (list.length > 0) && (list[0].equals("Orientation:")) ) 
    //{
    //  roll  = float(list[3]); // Roll = Z
    //  pitch = float(list[2]); // Pitch = Y 
    //  yaw   = float(list[1]); // Yaw/Heading = X
    //}
    if ( (list.length > 0) && (list[0].equals("Alt:")) ) 
    {
      alt  = float(list[1]);
    }
    if ( (list.length > 0) && (list[0].equals("Temp:")) ) 
    {
      temp  = float(list[1]);
    }
    if ( (list.length > 0) && (list[0].equals("Calibration:")) )
    {
      int sysCal   = int(list[1]);
      int gyroCal  = int(list[2]);
      int accelCal = int(list[3]);
      int magCal   = int(list[4]);
    }
    if ( (list.length > 0) && (list[0].equals("Fingers:")) )
    {
     indexFingerDeg  = float(list[1]);
     middleFingerDeg = float(list[2]);
     ringFingerDeg = float(list[3]);
    }
    if ( (list.length > 0) && (list[0].equals("Quaternions:")) )
    {
      q0 = float(list[1]);
      q1 = float(list[2]);
      q2 = float(list[3]);
      q3 = float(list[4]);
      
      //roll = atan2(2*(q0*q1+q2*q3), 1-2*(q1*q1+q2*q2));
      //pitch = asin(2*(q0*q2-q3*q1));
      //yaw = atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2+q3*q3));
      
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
    
    if ( (list.length > 0) && (list[0].equals("Acceleration:")) )
    {
      xacc = float(list[1]);
      yacc = float(list[2]);
      zacc = float(list[3]);
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
  translate(80,0,135); box(40,60,120);
  translate(0,0,100); rotateX(radians(-indexFingerDeg)); box(40,60,100);
  rotateX(radians(indexFingerDeg));
  // middle finger
  translate(-60,0,-90); box(40,60,140);
  translate(0,0,130); rotateX(radians(-middleFingerDeg)); box(40,60,120);
  rotateX(radians(middleFingerDeg));
  // ring finger
  translate(-60,0,-140); box(40,60,120);
  translate(0,0,110); rotateX(radians(-ringFingerDeg)); box(40,60,100);
  rotateX(radians(ringFingerDeg));
}

void calibrate_hand() {
  rollOffset = roll;
  pitchOffset = pitch;
  yawOffset = yaw + PI;  
}

//void signTranslate