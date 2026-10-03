OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[42];

xcx q[29], q[10];
xcx q[26], q[38];
xcx q[20], q[16];
xcx q[17], q[8];
xcx q[15], q[39];
xcx q[12], q[27];
xcx q[11], q[13];
xcx q[9], q[30];
xcx q[7], q[36];
xcx q[6], q[23];
xcx q[5], q[24];
xcx q[4], q[37];
xcx q[3], q[35];
xcx q[2], q[32];
xcx q[1], q[40];
xcx q[41], q[18];
xcx q[0], q[14];
xcx q[28], q[31];
xcx q[22], q[21];
xcx q[33], q[25];
xcx q[19], q[34];
