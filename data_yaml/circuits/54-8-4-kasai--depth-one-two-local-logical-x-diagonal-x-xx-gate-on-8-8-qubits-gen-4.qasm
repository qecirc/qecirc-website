OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[54];

sx q[36];
sx q[10];
sx q[33];
sx q[1];
sx q[20];
sx q[49];
xcx q[29], q[14];
xcx q[25], q[15];
xcx q[24], q[16];
xcx q[18], q[17];
xcx q[13], q[28];
xcx q[12], q[8];
xcx q[11], q[9];
xcx q[46], q[34];
xcx q[7], q[4];
xcx q[6], q[5];
xcx q[3], q[44];
xcx q[2], q[26];
xcx q[0], q[41];
xcx q[31], q[22];
xcx q[53], q[39];
xcx q[48], q[51];
xcx q[19], q[47];
xcx q[42], q[35];
xcx q[37], q[30];
xcx q[52], q[40];
xcx q[32], q[43];
xcx q[50], q[23];
xcx q[38], q[45];
xcx q[21], q[27];
