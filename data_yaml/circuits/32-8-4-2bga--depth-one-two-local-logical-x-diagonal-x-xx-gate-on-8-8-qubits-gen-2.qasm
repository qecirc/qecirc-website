OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[32];

xcx q[24], q[21];
xcx q[16], q[31];
xcx q[13], q[20];
xcx q[10], q[23];
xcx q[9], q[19];
xcx q[8], q[12];
xcx q[7], q[15];
xcx q[6], q[30];
xcx q[4], q[3];
xcx q[2], q[27];
xcx q[1], q[26];
xcx q[0], q[5];
xcx q[11], q[22];
xcx q[14], q[28];
xcx q[17], q[29];
xcx q[25], q[18];
