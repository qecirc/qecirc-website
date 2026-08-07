OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[31];

sx q[24];
sx q[16];
sx q[10];
sx q[26];
sx q[6];
sx q[3];
sx q[1];
sx q[7];
sx q[20];
sx q[14];
sx q[9];
sx q[22];
sx q[28];
sx q[30];
sx q[23];
sx q[15];
xcx q[24], q[22];
xcx q[16], q[20];
xcx q[10], q[14];
xcx q[26], q[9];
xcx q[6], q[15];
xcx q[3], q[28];
xcx q[1], q[30];
xcx q[7], q[23];
