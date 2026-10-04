OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[23];

sx q[7];
sx q[6];
sx q[8];
sx q[4];
sx q[3];
sx q[5];
sx q[12];
sx q[22];
sx q[16];
sx q[17];
sx q[11];
sx q[21];
xcx q[7], q[16];
xcx q[6], q[12];
xcx q[8], q[22];
xcx q[4], q[17];
xcx q[3], q[11];
xcx q[5], q[21];
