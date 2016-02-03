
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
*/

/* Set the delay between fresh samples in ms */
#define BNO055_SAMPLERATE_DELAY_MS (50)

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

void displaySensorStatus(void)
{
  /* Get the system status values (mostly for debugging purposes) */
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);

  /* Display the results in the Serial Monitor */
  Serial.println("");
  Serial.print("System Status: 0x");
  Serial.println(system_status, HEX);
  /* System Status (see section 4.3.58)
     ---------------------------------
     0 = Idle
     1 = System Error
     2 = Initializing Peripherals
     3 = System Iniitalization
     4 = Executing Self-Test
     5 = Sensor fusio algorithm running
     6 = System running without fusion algorithms */
  
  Serial.print("Self Test:     0x");
  Serial.println(self_test_results, HEX);
  /* Self Test Results (see section )
     --------------------------------
     1 = test passed, 0 = test failed

     Bit 0 = Accelerometer self test
     Bit 1 = Magnetometer self test
     Bit 2 = Gyroscope self test
     Bit 3 = MCU self test

     0x0F = all good! */
  
  Serial.print("System Error:  0x");
  Serial.println(system_error, HEX);
  /* System Error (see section 4.3.59)
     ---------------------------------
     0 = No error
     1 = Peripheral initialization error
     2 = System initialization error
     3 = Self test result failed
     4 = Register map value out of range
     5 = Register map address out of range
     6 = Register map write error
     7 = BNO low power mode not available for selected operat ion mode
     8 = Accelerometer power mode not available
     9 = Fusion algorithm configuration error
     A = Sensor configuration error */
  
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
  /* Automatically uses maximum USB data rate? */
  Serial.begin(115200); 
  Serial.println("Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor
      Operation mode settings
      OPERATION_MODE_CONFIG                                   = 0X00,
      OPERATION_MODE_ACCONLY                                  = 0X01,
      OPERATION_MODE_MAGONLY                                  = 0X02,
      OPERATION_MODE_GYRONLY                                  = 0X03,
      OPERATION_MODE_ACCMAG                                   = 0X04,
      OPERATION_MODE_ACCGYRO                                  = 0X05,
      OPERATION_MODE_MAGGYRO                                  = 0X06,
      OPERATION_MODE_AMG                                      = 0X07,
      OPERATION_MODE_IMUPLUS                                  = 0X08,
      OPERATION_MODE_COMPASS                                  = 0X09,
      OPERATION_MODE_M4G                                      = 0X0A,
      OPERATION_MODE_NDOF_FMC_OFF                             = 0X0B,
      OPERATION_MODE_NDOF                                     = 0X0C
 */
  if(!bno.begin(bno.OPERATION_MODE_IMUPLUS))
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.println("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display some basic information on this sensor */
  displaySensorDetails();
  displaySensorStatus();

  uint16_t modeRead = bno.readMode();
  Serial.print("Operation Mode:  ");
  Serial.println(modeRead);
  Serial.println(F(""));
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
  Serial.println(F("Orientation(degrees)"));
  Serial.print(F("   Yaw: "));
  Serial.print((float)event.orientation.x); // yaw
  Serial.print(F(" Pitch: "));
  Serial.print((float)event.orientation.y); // roll
  Serial.print(F(" Roll: "));
  Serial.println((float)event.orientation.z); // pitch

  /* Quaternions */
  imu::Quaternion quat = bno.getQuat();
  Serial.println(F("Quaternions"));
  Serial.print(F("   qW: "));
  Serial.print(quat.w(),4);
  Serial.print(F(" qX: "));
  Serial.print(quat.x(),4);
  Serial.print(F(" qY: "));
  Serial.print(quat.y(),4);
  Serial.print(F(" qZ: "));
  Serial.println(quat.z(),4);

  /* Also send calibration data for each sensor. */
  uint8_t sys, gyro, accel, mag = 0;
  bno.getCalibration(&sys, &gyro, &accel, &mag);
  Serial.println(F("Calibration"));
  Serial.print(F("   System: ")); 
  Serial.print(sys, DEC);
  Serial.print(F(" Gyro: "));
  Serial.print(gyro, DEC);
  Serial.print(F(" Accel: "));
  Serial.print(accel, DEC);
  Serial.print(F(" Mag: "));
  Serial.println(mag, DEC);
   
  /*Get acceleration information*/
  imu::Vector<3> linearAccel = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
  Serial.println("Acceleration");
  Serial.print("   aX: ");
  Serial.print(linearAccel[0],DEC); // X
  Serial.print(" aY: ");
  Serial.print(linearAccel[1],DEC); // Y
  Serial.print(" aZ: ");
  Serial.print(linearAccel[2],DEC); // Z
  Serial.println(F(""));

  /* Flex Sensors use simple voltage divider circuit:
   * VCC (3.3V) --> R=26.1kOhms ---> VOUT
   *                             ^
   *                             |
   *                    Flex Sensor Resistance (10kOhms - 50kOhms)
   *                             |
   *                            GND
   */
  
  /* Flex Sensor Degrees */
  int flexRaw[8];
  int flexDegrees[8];
  int flexPinMap[8];
  /* Mapping to Analog pins on teensy 
    from flexPinMap[0] to flexPinMap[7]
    Index, IndexKnuckle, Middle, MiddleKnuckle
    Ring, Ring Knuckle, Pinky, -
  */
  flexPinMap[0] = 15; flexPinMap[1] = 20; flexPinMap[2] = 23; flexPinMap[3] = 21;
  flexPinMap[4] = 16; flexPinMap[5] = 14; flexPinMap[6] = 17; flexPinMap[7] = 22;
  
  for (int i = 0; i < 8; i++){
    flexRaw[i] = analogRead(flexPinMap[i]);
    flexDegrees[i] = map(flexRaw[i], 700, 900, 0, 120);
  }

  Serial.println("FlexSensorBending(degrees)");
  Serial.print("   Index: ");
  Serial.print(flexDegrees[0],DEC);
  Serial.print(F(" "));
  Serial.print("Middle: ");
  Serial.print(flexDegrees[2],DEC);
  Serial.print(F(" "));
  Serial.print("Ring: ");
  Serial.print(flexDegrees[4],DEC);
  Serial.print(F(" "));
  Serial.print("Pinky: ");
  Serial.println(flexDegrees[6],DEC);
  Serial.print("   IndexKnuckle: ");
  Serial.print(flexDegrees[1],DEC);
  Serial.print(F(" "));
  Serial.print("MiddleKnuckle: ");
  Serial.print(flexDegrees[3],DEC);
  Serial.print(F(" "));
  Serial.print("RingKnuckle: ");
  Serial.println(flexDegrees[5],DEC);
  Serial.println(F(""));
  Serial.println(F(""));
  
  delay(BNO055_SAMPLERATE_DELAY_MS);
}
