OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[0];
sx q[12];
sx q[13];
sx q[1];
sx q[11];
sx q[9];
sx q[8];
sx q[5];
sx q[7];
sx q[14];
sx q[4];
sx q[10];
xcx q[0], q[14];
xcx q[12], q[11];
xcx q[13], q[8];
xcx q[1], q[5];
xcx q[9], q[4];
xcx q[7], q[10];
