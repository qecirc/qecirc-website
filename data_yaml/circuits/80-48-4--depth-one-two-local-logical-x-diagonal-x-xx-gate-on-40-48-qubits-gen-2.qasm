OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[80];

sx q[16];
sx q[14];
sx q[13];
sx q[12];
sx q[11];
sx q[10];
sx q[9];
sx q[8];
sx q[7];
sx q[6];
sx q[5];
sx q[71];
sx q[64];
sx q[58];
sx q[52];
sx q[46];
sx q[40];
sx q[34];
sx q[28];
sx q[22];
id q[79];
xcx q[16], q[5];
xcx q[14], q[71];
xcx q[13], q[64];
xcx q[12], q[58];
xcx q[11], q[52];
xcx q[10], q[46];
xcx q[9], q[40];
xcx q[8], q[34];
xcx q[7], q[28];
xcx q[6], q[22];
