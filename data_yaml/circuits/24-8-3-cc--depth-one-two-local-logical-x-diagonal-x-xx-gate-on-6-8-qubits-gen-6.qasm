OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[24];

sx q[14];
sx q[9];
sx q[19];
sx q[1];
sx q[0];
sx q[2];
sx q[18];
sx q[10];
sx q[20];
sx q[13];
sx q[23];
sx q[15];
id q[21];
xcx q[14], q[1];
xcx q[9], q[0];
xcx q[19], q[2];
xcx q[18], q[13];
xcx q[10], q[23];
xcx q[20], q[15];
