OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[32];

sx q[19];
sx q[13];
sx q[8];
sx q[21];
sx q[4];
sx q[2];
sx q[0];
sx q[5];
sx q[25];
sx q[17];
sx q[11];
sx q[27];
sx q[12];
sx q[31];
sx q[29];
sx q[18];
id q[15];
xcx q[19], q[0];
xcx q[13], q[5];
xcx q[8], q[4];
xcx q[21], q[2];
xcx q[25], q[29];
xcx q[17], q[18];
xcx q[11], q[12];
xcx q[27], q[31];
