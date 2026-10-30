OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[22];

sx q[14];
sx q[10];
sx q[8];
sx q[6];
sx q[5];
sx q[4];
sx q[3];
sx q[2];
sx q[1];
sx q[0];
sx q[7];
sx q[20];
sx q[15];
sx q[12];
sx q[13];
sx q[11];
sx q[16];
sx q[17];
sx q[19];
sx q[18];
sx q[9];
sx q[21];
xcx q[14], q[2];
xcx q[10], q[8];
xcx q[6], q[19];
xcx q[5], q[16];
xcx q[4], q[21];
xcx q[3], q[17];
xcx q[1], q[18];
xcx q[0], q[7];
xcx q[20], q[13];
xcx q[15], q[12];
xcx q[11], q[9];
