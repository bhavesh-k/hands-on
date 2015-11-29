import processing.serial.*;

float roll  = 0.0F;
float pitch = 0.0F;
float yaw   = 0.0F;
float temp  = 0.0F;
float alt   = 0.0F;

float middleFingerDeg = 0.0F;
float indexFingerDeg = 0.0F;

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
  size(640, 480, P3D);
  frameRate(25);
  
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

  // Simple 3 point lighting for dramatic effect.
  // Slightly red light in upper right, slightly blue light in upper left, and white light from behind.
  //pointLight(255, 200, 200,  400, 400,  500);
  //pointLight(200, 200, 255, -400, 400,  500);
  //pointLight(255, 255, 255,    0,   0, -500);
  
  // Instead rotating each shape, rotate the camera angle #mindblown
  // camera((height/2)*sin(radians(yaw)),(height/2)*sin(radians(pitch)),(height/2),width/2,height/2,0,0,1,0);
  
  // orthographic projection
  //ortho(0, width/2, 0, height/2); 
  
  // calculate displacement
  thresh = 0.2;
  if (abs(yacc) > thresh) {yvel = yvel + yacc;}
  if (abs(yvel) > thresh) {y = y + yvel;}
  
  // Move hand from 0,0 in top left to center of screen.
  translate(width/2+y,height/2,0);
  
  // Rotate shapes around the X/Y/Z axis (values in radians, 0..Pi*2)
  rotateZ(radians(roll));
  rotateX(radians(pitch));
  rotateY(radians(-yaw));
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
    if ( (list.length > 0) && (list[0].equals("Orientation:")) ) 
    {
      roll  = float(list[3]); // Roll = Z
      pitch = float(list[2]); // Pitch = Y 
      yaw   = float(list[1]); // Yaw/Heading = X
    }
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
      middleFingerDeg  = float(list[1]);
      indexFingerDeg = float(list[2]);      
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
  box(100,30,75);
  
  // white fingers
  fill(255, 255, 255);
  // index finger
  translate(-40,0,-57.5); box(20,30,40);
  translate(0,0,-40); rotateX(radians(indexFingerDeg)); box(20,30,40);
  rotateX(radians(-indexFingerDeg));
  // middle finger
  translate(30,0,40); box(20,30,40);
  translate(0,0,-45); rotateX(radians(middleFingerDeg)); box(20,30,50);
}