OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

xcx q[26], q[28];
xcx q[24], q[16];
xcx q[21], q[38];
xcx q[17], q[36];
xcx q[14], q[32];
xcx q[13], q[25];
xcx q[12], q[20];
xcx q[11], q[35];
xcx q[10], q[30];
xcx q[39], q[23];
xcx q[8], q[18];
xcx q[7], q[37];
xcx q[6], q[33];
xcx q[5], q[27];
xcx q[4], q[15];
xcx q[3], q[34];
xcx q[2], q[29];
xcx q[1], q[19];
xcx q[0], q[22];
xcx q[9], q[31];
