OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[56];

xcx q[38], q[39];
xcx q[31], q[53];
xcx q[27], q[25];
xcx q[24], q[29];
xcx q[22], q[34];
xcx q[21], q[43];
xcx q[55], q[48];
xcx q[19], q[46];
xcx q[18], q[44];
xcx q[17], q[47];
xcx q[16], q[42];
xcx q[15], q[50];
xcx q[14], q[35];
xcx q[20], q[45];
xcx q[12], q[28];
xcx q[11], q[33];
xcx q[10], q[41];
xcx q[9], q[51];
xcx q[8], q[32];
xcx q[7], q[40];
xcx q[13], q[52];
xcx q[5], q[54];
xcx q[4], q[23];
xcx q[3], q[26];
xcx q[2], q[30];
xcx q[1], q[36];
xcx q[0], q[49];
xcx q[6], q[37];
