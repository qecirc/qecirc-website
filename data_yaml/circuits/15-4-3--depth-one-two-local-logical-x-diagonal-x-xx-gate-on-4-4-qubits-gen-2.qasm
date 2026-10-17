OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[5];
sx q[3];
sx q[11];
sx q[13];
sx q[8];
sx q[6];
xcx q[7], q[2];
xcx q[0], q[14];
xcx q[12], q[4];
