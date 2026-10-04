OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[24];

xcx q[16], q[18];
xcx q[12], q[20];
xcx q[10], q[19];
xcx q[8], q[21];
xcx q[6], q[14];
xcx q[22], q[15];
xcx q[4], q[23];
xcx q[3], q[7];
xcx q[2], q[9];
xcx q[1], q[11];
xcx q[0], q[13];
xcx q[5], q[17];
