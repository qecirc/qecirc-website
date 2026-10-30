OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

xcx q[12], q[35];
xcx q[10], q[36];
xcx q[9], q[37];
xcx q[8], q[38];
xcx q[7], q[39];
xcx q[6], q[11];
xcx q[5], q[29];
xcx q[4], q[32];
xcx q[3], q[33];
xcx q[2], q[34];
xcx q[1], q[22];
xcx q[31], q[20];
xcx q[28], q[18];
xcx q[26], q[16];
xcx q[24], q[14];
xcx q[0], q[21];
xcx q[30], q[19];
xcx q[27], q[17];
xcx q[25], q[15];
xcx q[23], q[13];
