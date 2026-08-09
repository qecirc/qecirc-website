OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[56];

xcx q[36], q[22];
xcx q[27], q[45];
xcx q[23], q[39];
xcx q[18], q[46];
xcx q[15], q[41];
xcx q[14], q[42];
xcx q[12], q[32];
xcx q[11], q[31];
xcx q[10], q[40];
xcx q[9], q[29];
xcx q[8], q[34];
xcx q[7], q[50];
xcx q[6], q[49];
xcx q[55], q[26];
xcx q[5], q[48];
xcx q[4], q[28];
xcx q[3], q[37];
xcx q[2], q[13];
xcx q[1], q[51];
xcx q[0], q[16];
xcx q[54], q[19];
xcx q[25], q[52];
xcx q[38], q[17];
xcx q[30], q[20];
xcx q[47], q[24];
xcx q[21], q[44];
xcx q[33], q[35];
xcx q[43], q[53];
