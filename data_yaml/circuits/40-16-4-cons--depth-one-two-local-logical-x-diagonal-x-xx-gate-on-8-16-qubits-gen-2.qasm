OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

sx q[12];
sx q[10];
sx q[9];
sx q[8];
sx q[7];
sx q[6];
sx q[5];
sx q[4];
sx q[3];
sx q[2];
sx q[1];
sx q[31];
sx q[28];
sx q[26];
sx q[24];
sx q[22];
sx q[20];
sx q[18];
sx q[16];
sx q[14];
id q[39];
xcx q[12], q[1];
xcx q[10], q[31];
xcx q[9], q[28];
xcx q[8], q[26];
xcx q[7], q[24];
xcx q[6], q[22];
xcx q[5], q[20];
xcx q[4], q[18];
xcx q[3], q[16];
xcx q[2], q[14];
