OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[8];
sx q[4];
sx q[2];
sx q[1];
sx q[12];
sx q[6];
sx q[13];
sx q[7];
sx q[11];
sx q[10];
sx q[5];
sx q[14];
id q[9];
xcx q[8], q[10];
xcx q[4], q[12];
xcx q[2], q[1];
xcx q[6], q[11];
xcx q[13], q[7];
xcx q[5], q[14];
