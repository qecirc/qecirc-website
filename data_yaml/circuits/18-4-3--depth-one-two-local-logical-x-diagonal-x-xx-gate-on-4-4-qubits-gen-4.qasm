OPENQASM 2.0;
include "qelib1.inc";
gate xcx q0, q1 { h q0; cx q0, q1; h q0; }

qreg q[18];

xcx q[11], q[14];
xcx q[6], q[15];
xcx q[4], q[16];
xcx q[3], q[2];
xcx q[10], q[0];
xcx q[13], q[1];
xcx q[12], q[8];
xcx q[5], q[9];
xcx q[17], q[7];
