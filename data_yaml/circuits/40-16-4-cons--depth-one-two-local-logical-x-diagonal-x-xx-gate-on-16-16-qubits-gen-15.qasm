OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

sx q[28];
sx q[26];
sx q[24];
sx q[22];
sx q[20];
sx q[18];
sx q[16];
sx q[14];
sx q[27];
sx q[25];
sx q[23];
sx q[21];
sx q[19];
sx q[17];
sx q[15];
sx q[13];
xcx q[12], q[29];
xcx q[10], q[11];
xcx q[9], q[32];
xcx q[8], q[33];
xcx q[7], q[34];
xcx q[6], q[35];
xcx q[5], q[36];
xcx q[4], q[37];
xcx q[3], q[38];
xcx q[2], q[39];
xcx q[1], q[31];
xcx q[0], q[30];
