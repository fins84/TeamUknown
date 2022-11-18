int x;

void setup() 
{
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(115200);
  Serial.setTimeout(1);
}


void loop() 
{
  while (!Serial.available());
  x = Serial.readString().toInt();

  if(x == 1)
  {
    digitalWrite(LED_BUILTIN, HIGH);
  }
  else
  {
     digitalWrite(LED_BUILTIN, LOW);
  }
}
