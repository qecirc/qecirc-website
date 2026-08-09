OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[42];

xcx q[28], q[15];
xcx q[22], q[30];
xcx q[16], q[39];
xcx q[14], q[25];
xcx q[13], q[38];
xcx q[11], q[24];
xcx q[10], q[36];
xcx q[9], q[26];
xcx q[8], q[27];
xcx q[7], q[37];
xcx q[6], q[34];
xcx q[5], q[29];
xcx q[40], q[32];
xcx q[4], q[21];
xcx q[3], q[18];
xcx q[19], q[23];
xcx q[2], q[17];
xcx q[1], q[33];
xcx q[41], q[12];
xcx q[0], q[31];
xcx q[35], q[20];
