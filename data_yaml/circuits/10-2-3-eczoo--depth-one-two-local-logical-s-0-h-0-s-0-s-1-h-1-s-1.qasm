OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[10];

sx q[8];
sx q[7];
sx q[4];
sx q[9];
sx q[6];
sx q[3];
xcx q[5], q[1];
xcx q[2], q[0];
