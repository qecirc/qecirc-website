OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[14];

sx q[10];
sx q[3];
sx q[2];
sx q[0];
sx q[11];
sx q[13];
sx q[6];
id q[4];
xcx q[3], q[2];
xcx q[0], q[13];
xcx q[11], q[6];
