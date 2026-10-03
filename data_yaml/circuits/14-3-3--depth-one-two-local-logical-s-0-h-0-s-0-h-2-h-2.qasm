OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[12];

sx q[3];
sx q[2];
sx q[1];
xcx q[10], q[9];
id q[8];
xcx q[3], q[2];
xcx q[11], q[1];
