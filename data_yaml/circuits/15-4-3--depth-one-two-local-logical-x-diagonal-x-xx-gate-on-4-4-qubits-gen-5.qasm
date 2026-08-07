OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[15];

sx q[10];
sx q[5];
sx q[14];
xcx q[7], q[6];
xcx q[3], q[12];
xcx q[2], q[4];
xcx q[1], q[9];
xcx q[0], q[13];
xcx q[11], q[8];
