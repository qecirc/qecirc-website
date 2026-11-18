OPENQASM 2.0;
include "qelib1.inc";

qreg q[29];
creg rec[12];

h q[28];
h q[9];
h q[11];
h q[1];
h q[6];
h q[13];
h q[16];
h q[4];
h q[12];
h q[19];
h q[21];
h q[24];
cx q[16], q[0];
cx q[9], q[7];
cx q[12], q[15];
cx q[6], q[14];
cx q[1], q[10];
cx q[4], q[8];
cx q[28], q[20];
cx q[19], q[22];
cx q[21], q[17];
cx q[24], q[26];
cx q[0], q[5];
cx q[7], q[3];
cx q[4], q[9];
cx q[16], q[2];
cx q[13], q[6];
cx q[19], q[1];
cx q[24], q[23];
cx q[26], q[25];
cx q[15], q[5];
cx q[0], q[1];
cx q[3], q[28];
cx q[14], q[16];
cx q[2], q[8];
cx q[11], q[9];
cx q[10], q[7];
cx q[6], q[12];
cx q[4], q[18];
cx q[23], q[27];
cx q[13], q[15];
cx q[1], q[3];
cx q[11], q[2];
cx q[9], q[0];
cx q[5], q[14];
cx q[22], q[6];
cx q[19], q[8];
cx q[7], q[17];
cx q[26], q[27];
measure q[27] -> rec[0];
cx q[22], q[15];
cx q[19], q[14];
cx q[11], q[28];
cx q[3], q[21];
cx q[7], q[18];
cx q[8], q[20];
cx q[6], q[17];
cx q[23], q[2];
h q[23]; measure q[23] -> rec[1]; h q[23]; // decomposed MX
cx q[22], q[0];
cx q[15], q[21];
cx q[3], q[18];
cx q[19], q[2];
cx q[28], q[20];
cx q[14], q[17];
cx q[25], q[7];
cx q[26], q[11];
h q[25]; measure q[25] -> rec[2]; h q[25]; // decomposed MX
h q[26]; measure q[26] -> rec[3]; h q[26]; // decomposed MX
h q[28]; measure q[28] -> rec[4]; h q[28]; // decomposed MX
cx q[19], q[22];
cx q[0], q[20];
cx q[21], q[17];
cx q[8], q[18];
cx q[24], q[3];
h q[19]; measure q[19] -> rec[5]; h q[19]; // decomposed MX
measure q[22] -> rec[6];
measure q[20] -> rec[7];
measure q[17] -> rec[8];
h q[21]; measure q[21] -> rec[9]; h q[21]; // decomposed MX
measure q[18] -> rec[10];
h q[24]; measure q[24] -> rec[11]; h q[24]; // decomposed MX
