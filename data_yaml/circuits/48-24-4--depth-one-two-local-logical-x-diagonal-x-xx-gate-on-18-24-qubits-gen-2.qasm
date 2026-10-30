OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[48];

sx q[12];
sx q[10];
sx q[9];
sx q[8];
sx q[7];
sx q[6];
sx q[5];
sx q[4];
sx q[3];
sx q[41];
sx q[36];
sx q[32];
sx q[28];
sx q[24];
sx q[20];
sx q[16];
id q[47];
xcx q[12], q[3];
xcx q[10], q[41];
xcx q[9], q[36];
xcx q[8], q[32];
xcx q[7], q[28];
xcx q[6], q[24];
xcx q[5], q[20];
xcx q[4], q[16];
