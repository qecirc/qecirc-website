OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[21];

sx q[12];
sx q[9];
sx q[5];
sx q[4];
sx q[3];
sx q[2];
sx q[1];
sx q[13];
sx q[10];
sx q[20];
sx q[15];
sx q[11];
sx q[6];
sx q[18];
id q[14];
xcx q[12], q[11];
xcx q[9], q[1];
xcx q[5], q[13];
xcx q[4], q[2];
xcx q[3], q[15];
xcx q[10], q[6];
xcx q[20], q[18];
