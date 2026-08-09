OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[80];

sx q[16];
sx q[10];
sx q[5];
sx q[46];
sx q[4];
sx q[45];
sx q[3];
sx q[44];
sx q[2];
sx q[43];
sx q[1];
sx q[42];
sx q[0];
sx q[41];
sx q[15];
sx q[75];
id q[79];
xcx q[16], q[10];
xcx q[5], q[46];
xcx q[4], q[45];
xcx q[3], q[44];
xcx q[2], q[43];
xcx q[1], q[42];
xcx q[0], q[41];
xcx q[15], q[75];
