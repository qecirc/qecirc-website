OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[22];

sx q[6];
sx q[4];
sx q[3];
sx q[2];
sx q[1];
sx q[8];
sx q[15];
sx q[14];
sx q[12];
sx q[11];
sx q[5];
sx q[9];
sx q[17];
sx q[19];
sx q[20];
sx q[21];
xcx q[6], q[4];
xcx q[3], q[9];
xcx q[2], q[20];
xcx q[1], q[19];
xcx q[8], q[17];
xcx q[15], q[11];
xcx q[14], q[12];
xcx q[5], q[21];
