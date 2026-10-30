OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

xcx q[26], q[42];
xcx q[19], q[35];
xcx q[18], q[23];
xcx q[16], q[28];
xcx q[15], q[30];
xcx q[14], q[17];
xcx q[13], q[40];
xcx q[12], q[31];
xcx q[11], q[38];
xcx q[10], q[46];
xcx q[9], q[45];
xcx q[8], q[20];
xcx q[7], q[24];
xcx q[6], q[39];
xcx q[5], q[25];
xcx q[4], q[36];
xcx q[3], q[22];
xcx q[2], q[34];
xcx q[1], q[37];
xcx q[0], q[21];
xcx q[27], q[32];
xcx q[47], q[44];
xcx q[41], q[29];
xcx q[33], q[43];
