OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

sx q[12];
sx q[7];
sx q[3];
sx q[28];
sx q[2];
sx q[27];
sx q[1];
sx q[26];
sx q[0];
sx q[25];
sx q[11];
sx q[44];
id q[47];
xcx q[12], q[7];
xcx q[3], q[28];
xcx q[2], q[27];
xcx q[1], q[26];
xcx q[0], q[25];
xcx q[11], q[44];
