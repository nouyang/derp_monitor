void setup() {
  Serial.begin(115200);
}

// the loop routine runs over and over again forever:
void loop() {
  Serial.println("A,I_HV:-67.26,I_LV:-131.68,V_HV:678.59,V_LV:71.21,T1:433.74,T2:433.74,T3:433.74,T4:433.74,MOD1:0,MOD2:0,MOD3:0,MOD4:0");
  delay(100);        // delay in between reads for stability
  Serial.println("A,I_HV:nnn,I_LV:-131.68,V_HV:678.59,V_LV:71.21,T1:433.74,T2:433.74,T3:433.74,T4:433.74,MOD1:0,MOD2:0,MOD3:0,MOD4:nnn");
  delay(100);        // delay in between reads for stability
  Serial.println("B,I_HV:-67.26,I_LV:-131.68,V_HV:678.59,V_LV:71.21,T1:433.74,T2:433.74,T3:433.74,T4:433.74,MOD1:0,MOD2:0,MOD3:0,MOD4:0");
  delay(100);        // delay in between reads for stability
  Serial.println("B,I_HV:nnn,I_LV:-131.68,V_HV:678.59,V_LV:71.21,T1:433.74,T2:433.74,T3:433.74,T4:433.74,MOD1:0,MOD2:0,MOD3:0,MOD4:nnn");
  delay(100);        // delay in between reads for stability
}
