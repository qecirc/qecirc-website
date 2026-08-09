OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[22];

sx q[1];
sx q[8];
sx q[15];
sx q[14];
sx q[12];
sx q[11];
sx q[17];
sx q[19];
id q[21];
xcx q[1], q[8];
xcx q[15], q[12];
xcx q[14], q[11];
xcx q[17], q[19];
