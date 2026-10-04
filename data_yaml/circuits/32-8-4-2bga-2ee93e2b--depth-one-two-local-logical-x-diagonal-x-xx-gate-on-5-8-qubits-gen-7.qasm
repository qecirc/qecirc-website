OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[31];

sx q[24];
sx q[19];
sx q[16];
sx q[13];
sx q[10];
sx q[8];
sx q[26];
sx q[21];
sx q[4];
sx q[2];
sx q[0];
sx q[5];
sx q[28];
sx q[30];
sx q[23];
sx q[15];
xcx q[24], q[30];
xcx q[19], q[0];
xcx q[16], q[23];
xcx q[13], q[5];
xcx q[10], q[15];
xcx q[8], q[4];
xcx q[26], q[28];
xcx q[21], q[2];
