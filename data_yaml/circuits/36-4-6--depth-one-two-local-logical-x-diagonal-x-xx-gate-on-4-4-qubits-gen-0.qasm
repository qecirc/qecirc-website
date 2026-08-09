OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[36];

xcx q[24], q[31];
xcx q[19], q[14];
xcx q[15], q[29];
xcx q[12], q[16];
xcx q[11], q[23];
xcx q[10], q[33];
xcx q[9], q[27];
xcx q[8], q[21];
xcx q[7], q[13];
xcx q[6], q[20];
xcx q[5], q[18];
xcx q[4], q[26];
xcx q[3], q[28];
xcx q[2], q[17];
xcx q[1], q[22];
xcx q[0], q[25];
xcx q[35], q[30];
xcx q[32], q[34];
