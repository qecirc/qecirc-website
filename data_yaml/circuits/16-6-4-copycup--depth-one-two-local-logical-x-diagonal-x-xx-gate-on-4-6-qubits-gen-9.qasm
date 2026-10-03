OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[16];

sx q[8];
sx q[4];
sx q[2];
sx q[1];
sx q[0];
sx q[12];
sx q[10];
sx q[9];
sx q[7];
sx q[13];
sx q[15];
sx q[5];
xcx q[8], q[5];
xcx q[4], q[12];
xcx q[2], q[7];
xcx q[1], q[9];
xcx q[0], q[13];
xcx q[10], q[15];
