OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

xcx q[30], q[27];
xcx q[26], q[31];
xcx q[23], q[38];
xcx q[20], q[21];
xcx q[37], q[24];
xcx q[14], q[28];
xcx q[12], q[32];
xcx q[11], q[39];
xcx q[10], q[22];
xcx q[19], q[25];
xcx q[8], q[17];
xcx q[7], q[15];
xcx q[6], q[18];
xcx q[5], q[13];
xcx q[9], q[16];
xcx q[3], q[35];
xcx q[2], q[33];
xcx q[1], q[36];
xcx q[0], q[29];
xcx q[4], q[34];
