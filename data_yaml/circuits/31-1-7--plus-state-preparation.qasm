OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

reset q[23];
reset q[21];
reset q[17];
reset q[12];
reset q[11];
reset q[10];
reset q[8];
reset q[6];
reset q[3];
reset q[2];
reset q[13];
reset q[20];
reset q[28];
reset q[0];
reset q[27];
reset q[7]; h q[7]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[18]; h q[18]; // decomposed RX
reset q[14]; h q[14]; // decomposed RX
reset q[22]; h q[22]; // decomposed RX
reset q[15]; h q[15]; // decomposed RX
reset q[16]; h q[16]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
cx q[14], q[2];
cx q[26], q[6];
cx q[18], q[10];
cx q[29], q[11];
cx q[22], q[12];
cx q[1], q[21];
cx q[25], q[23];
cx q[15], q[0];
cx q[7], q[8];
cx q[19], q[17];
cx q[16], q[22];
cx q[25], q[18];
cx q[14], q[28];
cx q[24], q[26];
cx q[11], q[1];
cx q[29], q[13];
cx q[21], q[6];
cx q[2], q[10];
cx q[4], q[12];
cx q[9], q[23];
cx q[17], q[20];
cx q[10], q[19];
cx q[28], q[27];
cx q[18], q[0];
cx q[9], q[26];
cx q[13], q[3];
cx q[30], q[4];
cx q[5], q[6];
cx q[1], q[7];
cx q[23], q[12];
cx q[8], q[25];
cx q[22], q[21];
cx q[24], q[14];
cx q[16], q[11];
cx q[15], q[17];
cx q[5], q[27];
cx q[0], q[20];
cx q[12], q[3];
cx q[9], q[8];
cx q[26], q[2];
cx q[30], q[29];
cx q[6], q[28];
cx q[7], q[23];
cx q[19], q[18];
cx q[1], q[22];
cx q[4], q[13];
