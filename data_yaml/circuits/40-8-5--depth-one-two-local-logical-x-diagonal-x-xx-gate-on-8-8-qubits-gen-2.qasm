OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

xcx q[30], q[36];
xcx q[26], q[29];
xcx q[23], q[35];
xcx q[20], q[34];
xcx q[37], q[33];
xcx q[16], q[25];
xcx q[14], q[39];
xcx q[12], q[32];
xcx q[10], q[22];
xcx q[18], q[28];
xcx q[8], q[15];
xcx q[7], q[11];
xcx q[6], q[17];
xcx q[5], q[19];
xcx q[9], q[13];
xcx q[3], q[27];
xcx q[2], q[21];
xcx q[1], q[31];
xcx q[0], q[38];
xcx q[4], q[24];
