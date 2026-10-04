OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[47];

sx q[40];
sx q[36];
sx q[32];
sx q[44];
sx q[10];
sx q[9];
sx q[8];
sx q[11];
sx q[42];
sx q[38];
sx q[34];
sx q[46];
sx q[13];
sx q[19];
sx q[17];
sx q[15];
xcx q[40], q[42];
xcx q[36], q[38];
xcx q[32], q[34];
xcx q[44], q[46];
xcx q[10], q[13];
xcx q[9], q[19];
xcx q[8], q[17];
xcx q[11], q[15];
