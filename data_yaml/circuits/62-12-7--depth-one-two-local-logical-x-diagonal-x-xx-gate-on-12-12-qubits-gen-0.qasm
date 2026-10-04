OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[62];

xcx q[54], q[16];
xcx q[49], q[18];
xcx q[44], q[21];
xcx q[39], q[24];
xcx q[35], q[27];
xcx q[32], q[30];
xcx q[29], q[33];
xcx q[26], q[36];
xcx q[23], q[40];
xcx q[20], q[45];
xcx q[17], q[50];
xcx q[15], q[56];
xcx q[13], q[60];
xcx q[11], q[19];
xcx q[10], q[22];
xcx q[9], q[25];
xcx q[8], q[28];
xcx q[7], q[31];
xcx q[6], q[34];
xcx q[5], q[38];
xcx q[4], q[43];
xcx q[3], q[48];
xcx q[2], q[53];
xcx q[1], q[61];
xcx q[0], q[37];
xcx q[58], q[42];
xcx q[51], q[47];
xcx q[46], q[52];
xcx q[41], q[59];
xcx q[57], q[12];
xcx q[55], q[14];
