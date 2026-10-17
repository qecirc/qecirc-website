OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[24];

sx q[10];
sx q[6];
sx q[4];
sx q[3];
sx q[2];
sx q[23];
sx q[22];
sx q[15];
sx q[14];
sx q[12];
sx q[11];
sx q[5];
sx q[9];
sx q[13];
sx q[20];
sx q[21];
xcx q[10], q[5];
xcx q[6], q[3];
xcx q[4], q[9];
xcx q[2], q[13];
xcx q[23], q[20];
xcx q[22], q[21];
xcx q[15], q[12];
xcx q[14], q[11];
