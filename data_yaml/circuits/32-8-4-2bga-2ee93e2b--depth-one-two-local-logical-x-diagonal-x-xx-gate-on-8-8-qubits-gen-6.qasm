OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[32];

sx q[6];
sx q[4];
sx q[3];
sx q[2];
sx q[1];
sx q[0];
sx q[7];
sx q[5];
sx q[12];
sx q[28];
sx q[31];
sx q[30];
sx q[29];
sx q[23];
sx q[18];
sx q[15];
xcx q[24], q[22];
xcx q[19], q[25];
xcx q[16], q[20];
xcx q[13], q[17];
xcx q[10], q[14];
xcx q[8], q[11];
xcx q[26], q[9];
xcx q[21], q[27];
