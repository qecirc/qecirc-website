OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[64];

xcx q[56], q[63];
xcx q[48], q[45];
xcx q[41], q[15];
xcx q[36], q[59];
xcx q[33], q[49];
xcx q[30], q[40];
xcx q[25], q[58];
xcx q[20], q[22];
xcx q[17], q[24];
xcx q[14], q[42];
xcx q[13], q[53];
xcx q[12], q[18];
xcx q[11], q[39];
xcx q[10], q[46];
xcx q[9], q[34];
xcx q[8], q[62];
xcx q[7], q[31];
xcx q[6], q[50];
xcx q[5], q[44];
xcx q[4], q[29];
xcx q[3], q[55];
xcx q[2], q[28];
xcx q[1], q[61];
xcx q[0], q[35];
xcx q[43], q[51];
xcx q[38], q[32];
xcx q[60], q[57];
xcx q[52], q[23];
xcx q[26], q[27];
xcx q[21], q[54];
xcx q[19], q[37];
xcx q[16], q[47];
