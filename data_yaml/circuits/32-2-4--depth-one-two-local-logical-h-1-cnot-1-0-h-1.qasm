OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[32];

xcx q[28], q[24];
xcx q[25], q[27];
xcx q[22], q[31];
xcx q[20], q[30];
xcx q[15], q[11];
xcx q[12], q[14];
xcx q[9], q[19];
xcx q[8], q[17];
xcx q[7], q[10];
xcx q[6], q[13];
xcx q[5], q[18];
xcx q[4], q[16];
xcx q[29], q[0];
xcx q[26], q[1];
xcx q[23], q[2];
xcx q[21], q[3];
