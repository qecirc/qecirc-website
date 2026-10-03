OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[14];

sx q[3];
sx q[2];
sx q[1];
sx q[0];
sx q[13];
sx q[9];
sx q[12];
sx q[4];
xcx q[3], q[2];
xcx q[1], q[9];
xcx q[0], q[13];
xcx q[12], q[4];
