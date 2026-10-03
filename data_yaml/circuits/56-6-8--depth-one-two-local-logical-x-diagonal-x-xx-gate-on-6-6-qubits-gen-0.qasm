OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[56];

xcx q[50], q[31];
xcx q[35], q[25];
xcx q[28], q[40];
xcx q[24], q[52];
xcx q[21], q[30];
xcx q[20], q[49];
xcx q[18], q[51];
xcx q[17], q[26];
xcx q[16], q[42];
xcx q[15], q[36];
xcx q[14], q[27];
xcx q[13], q[41];
xcx q[12], q[37];
xcx q[11], q[44];
xcx q[10], q[47];
xcx q[9], q[48];
xcx q[8], q[45];
xcx q[7], q[29];
xcx q[6], q[19];
xcx q[5], q[43];
xcx q[4], q[22];
xcx q[55], q[46];
xcx q[3], q[34];
xcx q[2], q[32];
xcx q[1], q[38];
xcx q[33], q[23];
xcx q[0], q[53];
xcx q[54], q[39];
