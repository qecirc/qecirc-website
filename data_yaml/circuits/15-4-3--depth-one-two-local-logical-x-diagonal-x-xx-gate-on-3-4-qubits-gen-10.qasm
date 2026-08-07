OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[2];
sx q[0];
sx q[14];
sx q[9];
sx q[8];
sx q[6];
sx q[4];
xcx q[2], q[0];
xcx q[14], q[8];
xcx q[9], q[4];
