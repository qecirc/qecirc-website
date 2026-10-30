OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[16];

sx q[2];
sx q[1];
sx q[10];
sx q[9];
sx q[14];
sx q[13];
sx q[6];
sx q[5];
xcx q[8], q[15];
xcx q[4], q[11];
xcx q[0], q[7];
xcx q[12], q[3];
