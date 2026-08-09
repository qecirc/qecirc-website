OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[14];

sx q[8];
sx q[4];
sx q[2];
sx q[1];
sx q[12];
sx q[13];
sx q[7];
sx q[10];
id q[9];
xcx q[8], q[13];
xcx q[4], q[2];
xcx q[1], q[7];
xcx q[12], q[10];
