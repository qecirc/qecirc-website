OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[16];

sx q[0];
sx q[12];
sx q[1];
sx q[6];
sx q[8];
sx q[3];
sx q[14];
sx q[10];
xcx q[2], q[11];
xcx q[13], q[9];
xcx q[15], q[7];
xcx q[5], q[4];
