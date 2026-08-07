OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[10];

xcx q[4], q[0];
xcx q[2], q[9];
xcx q[6], q[5];
xcx q[1], q[3];
xcx q[8], q[7];
