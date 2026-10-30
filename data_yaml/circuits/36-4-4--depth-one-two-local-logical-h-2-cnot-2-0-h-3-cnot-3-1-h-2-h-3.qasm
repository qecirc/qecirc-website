OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[36];

xcx q[19], q[21];
xcx q[17], q[22];
xcx q[15], q[29];
xcx q[13], q[10];
xcx q[12], q[30];
xcx q[11], q[34];
xcx q[9], q[0];
xcx q[8], q[31];
xcx q[7], q[35];
xcx q[6], q[14];
xcx q[5], q[32];
xcx q[4], q[33];
xcx q[3], q[25];
xcx q[2], q[27];
xcx q[1], q[26];
xcx q[16], q[28];
xcx q[20], q[24];
xcx q[18], q[23];
