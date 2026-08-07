OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[80];

sx q[16];
sx q[9];
sx q[5];
sx q[40];
sx q[4];
sx q[39];
sx q[3];
sx q[38];
sx q[2];
sx q[37];
sx q[1];
sx q[36];
sx q[0];
sx q[35];
sx q[15];
sx q[76];
id q[79];
xcx q[16], q[9];
xcx q[5], q[40];
xcx q[4], q[39];
xcx q[3], q[38];
xcx q[2], q[37];
xcx q[1], q[36];
xcx q[0], q[35];
xcx q[15], q[76];
