OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[24];

sx q[12];
sx q[22];
sx q[16];
sx q[18];
sx q[10];
sx q[20];
sx q[13];
sx q[23];
sx q[15];
sx q[17];
sx q[11];
sx q[21];
xcx q[14], q[1];
xcx q[9], q[0];
xcx q[19], q[2];
xcx q[7], q[4];
xcx q[6], q[3];
xcx q[8], q[5];
