OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

sx q[12];
sx q[10];
sx q[3];
sx q[41];
sx q[2];
sx q[40];
sx q[1];
sx q[39];
sx q[0];
sx q[38];
sx q[11];
sx q[37];
id q[47];
xcx q[12], q[10];
xcx q[3], q[41];
xcx q[2], q[40];
xcx q[1], q[39];
xcx q[0], q[38];
xcx q[11], q[37];
