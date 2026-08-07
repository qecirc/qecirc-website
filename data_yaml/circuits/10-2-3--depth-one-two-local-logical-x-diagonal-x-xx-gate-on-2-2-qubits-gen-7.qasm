OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[10];

sx q[1];
sx q[8];
sx q[9];
sx q[3];
sx q[7];
xcx q[0], q[5];
xcx q[1], q[8];
xcx q[3], q[7];
