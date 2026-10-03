OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

sx q[12];
sx q[6];
sx q[3];
sx q[24];
sx q[2];
sx q[23];
sx q[1];
sx q[22];
sx q[0];
sx q[21];
sx q[11];
sx q[45];
id q[47];
xcx q[12], q[6];
xcx q[3], q[24];
xcx q[2], q[23];
xcx q[1], q[22];
xcx q[0], q[21];
xcx q[11], q[45];
