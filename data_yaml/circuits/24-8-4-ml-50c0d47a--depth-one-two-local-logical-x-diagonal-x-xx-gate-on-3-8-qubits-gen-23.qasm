OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[22];

sx q[6];
sx q[4];
sx q[3];
sx q[15];
sx q[14];
sx q[12];
sx q[11];
sx q[9];
id q[21];
xcx q[6], q[9];
xcx q[4], q[3];
xcx q[15], q[14];
xcx q[12], q[11];
