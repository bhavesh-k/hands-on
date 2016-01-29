
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/* This driver uses the Adafruit unified sensor library (Adafruit_Sensor),
   which provides a common 'type' for sensor data and some helper functions.

   To use this driver you will also need to download the Adafruit_Sensor
   library and include it in your libraries folder.

   You should also assign a unique ID to this sensor for use with
   the Adafruit Sensor API so that you can identify this particular
   sensor in any data logs, etc.  To assign a unique ID, simply
   provide an appropriate value in the constructor below (12345
   is used by default in this example).

   Connections
   ===========
   Connect SCL to analog 5
   Connect SDA to analog 4
   Connect VDD to 3.3-5V DC
   Connect GROUND to common ground

   History
   =======
   2015/MAR/03  - First release (KTOWN)
*/

/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (20)

Adafruit_BNO055 bno = Adafruit_BNO055(55);

/**************************************************************************/
/*
    Displays some basic information on this sensor from the unified
    sensor API sensor_t type (see Adafruit_Sensor for more information)
*/
/**************************************************************************/
void displaySensorDetails(void)
{
  sensor_t sensor;
  bno.getSensor(&sensor);
  Serial.println("------------------------------------");
  Serial.print  ("Sensor:       "); Serial.println(sensor.name);
  Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
  Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
  Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
  Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
  Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
  Serial.println("------------------------------------");
  Serial.println("");
  delay(500);
}

/**************************************************************************/
/*
    Arduino setup function (automatically called at startup)
*/
/**************************************************************************/
void setup(void)
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin(bno.OPERATION_MODE_IMUPLUS))
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display some basic information on this sensor */
  displaySensorDetails();

  uint16_t modeRead = bno.readMode();
  Serial.print("Mode:  ");
  Serial.println(modeRead);
  
}

/**************************************************************************/
/*
    Arduino loop function, called once 'setup' is complete (your own code
    should go here)
*/
/**************************************************************************/
void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Board layout:
         +----------+
         |         *| RST   PITCH  ROLL  HEADING
     ADR |*        *| SCL
     INT |*        *| SDA     ^            /->
     PS1 |*        *| GND     |            |
     PS0 |*        *| 3VO     Y    Z-->    \-X
         |         *| VIN
         +----------+
  */

  /* The processing sketch expects data as roll, pitch, yaw */
  Serial.print(F("Orientation: "));
  Serial.print((float)event.orientation.x); // yaw
  Serial.print(F(" "));
  Serial.print((float)event.orientation.y); // pitch
  Serial.print(F(" "));
  Serial.print((float)event.orientation.z); // roll
  Serial.println(F(""));

  /* Quaternions */
  imu::Quaternion quat = bno.getQuat();
  Serial.print(F("Quaternions: "));
  Serial.print(quat.w(),4);
  Serial.print(F(" "));
  Serial.print(quat.x(),4);
  Serial.print(F(" "));
  Serial.print(quat.y(),4);
  Serial.print(F(" "));
  Serial.println(quat.z(),4);

  /* Also send calibration data for each sensor. */
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.print(F("Calibration: "));
  Serial.print(sys, DEC);
  Serial.print(F(" "));
  Serial.print(gyro, DEC);
  Serial.print(F(" "));
  Serial.print(accel, DEC);
  Serial.print(F(" "));
  Serial.println(mag, DEC);
  
  ////// Flex Sensor Degrees
  int sensor[8];
  int degrees[8];
  int pins[8];

  // analog pins on teensy
  pins[0] = 14; pins[1] = 15; pins[2] = 16; pins[3] = 17;
  pins[4] = 20; pins[5] = 21; pins[6] = 22; pins[7] = 23;
  
  for (int i = 0; i < 8; i++){
    sensor[i] = analogRead(pins[i]); //A1 Input: 26.1 kOhm Series Resistor
    degrees[i] = map(sensor[i], 700, 900, 0, 120);
  }

  //Serial.print("26.1kOhm resistor analog input: ");
  //Serial.print(sensor[0],DEC);
  Serial.print("Fingers: ");
  Serial.print(degrees[1],DEC);
  Serial.print(F(" "));
  Serial.print(degrees[4],DEC);
  Serial.print(F(" "));
  Serial.print(degrees[7],DEC);
  Serial.print(F(" "));
  Serial.print(degrees[5],DEC);
  Serial.print(F(" "));
  Serial.print(degrees[2],DEC);
  Serial.print(F(" "));
  Serial.print(degrees[0],DEC);
  Serial.print(F(" "));
  Serial.println(degrees[3],DEC);
  ////// Flex Sensor Degrees

  /*Get acceleration information*/
  imu::Vector<3> linearAccel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  Serial.print("Acceleration: ");
  Serial.print(linearAccel[0],DEC);
  Serial.print(F(" "));
  Serial.print(linearAccel[1],DEC);
  Serial.print(F(" "));
  Serial.println(linearAccel[2],DEC);
  
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
