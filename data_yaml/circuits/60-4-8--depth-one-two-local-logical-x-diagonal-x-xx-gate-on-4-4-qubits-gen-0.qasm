OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[60];

xcx q[42], q[0];
xcx q[36], q[28];
xcx q[31], q[30];
xcx q[29], q[35];
xcx q[26], q[32];
xcx q[23], q[27];
xcx q[22], q[37];
xcx q[21], q[44];
xcx q[20], q[33];
xcx q[18], q[24];
xcx q[17], q[1];
xcx q[16], q[47];
xcx q[15], q[55];
xcx q[14], q[43];
xcx q[13], q[54];
xcx q[12], q[56];
xcx q[11], q[25];
xcx q[10], q[51];
xcx q[50], q[59];
xcx q[40], q[38];
xcx q[9], q[58];
xcx q[8], q[41];
xcx q[7], q[34];
xcx q[6], q[48];
xcx q[5], q[53];
xcx q[4], q[45];
xcx q[3], q[57];
xcx q[2], q[19];
xcx q[49], q[52];
xcx q[39], q[46];
