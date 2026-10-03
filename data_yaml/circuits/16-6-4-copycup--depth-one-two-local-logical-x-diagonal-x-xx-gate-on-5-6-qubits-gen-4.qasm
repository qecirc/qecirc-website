OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[8];
sx q[0];
sx q[14];
sx q[3];
sx q[13];
sx q[6];
sx q[11];
sx q[5];
xcx q[8], q[6];
xcx q[0], q[14];
xcx q[3], q[5];
xcx q[13], q[11];
