OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[40];

sx q[12];
sx q[10];
sx q[1];
sx q[31];
sx q[0];
sx q[30];
sx q[11];
sx q[29];
id q[39];
xcx q[12], q[10];
xcx q[1], q[31];
xcx q[0], q[30];
xcx q[11], q[29];
