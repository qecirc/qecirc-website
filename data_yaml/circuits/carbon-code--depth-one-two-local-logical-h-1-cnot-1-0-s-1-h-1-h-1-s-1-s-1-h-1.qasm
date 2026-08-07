OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[12];

sx q[1];
sx q[7];
sx q[9];
sx q[8];
sx q[10];
sx q[5];
xcx q[0], q[6];
xcx q[2], q[3];
xcx q[4], q[11];
