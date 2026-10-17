OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

sx q[26];
sx q[23];
sx q[20];
sx q[29];
sx q[16];
sx q[14];
sx q[12];
sx q[18];
sx q[2];
sx q[1];
sx q[0];
sx q[3];
sx q[43];
sx q[39];
sx q[35];
sx q[47];
id q[15];
xcx q[26], q[16];
xcx q[23], q[14];
xcx q[20], q[12];
xcx q[29], q[18];
xcx q[2], q[35];
xcx q[1], q[47];
xcx q[0], q[43];
xcx q[3], q[39];
