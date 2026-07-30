OPENQASM 2.0;
include "qelib1.inc";

qreg q[49];
creg rec[24];

reset q[25]; h q[25]; // decomposed RX
reset q[26]; h q[26]; // decomposed RX
reset q[27]; h q[27]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[30]; h q[30]; // decomposed RX
reset q[31]; h q[31]; // decomposed RX
reset q[32]; h q[32]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[34]; h q[34]; // decomposed RX
reset q[35]; h q[35]; // decomposed RX
reset q[36]; h q[36]; // decomposed RX
reset q[37]; h q[37]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[39]; h q[39]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[42]; h q[42]; // decomposed RX
reset q[43]; h q[43]; // decomposed RX
reset q[44]; h q[44]; // decomposed RX
reset q[45]; h q[45]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[48]; h q[48]; // decomposed RX
barrier q;

cx q[25], q[7];
cx q[26], q[6];
cx q[27], q[14];
cx q[28], q[5];
cx q[29], q[9];
cx q[30], q[23];
cx q[31], q[1];
cx q[32], q[4];
cx q[33], q[24];
cx q[34], q[2];
cx q[35], q[10];
cx q[36], q[0];
barrier q;

cx q[25], q[16];
cx q[26], q[22];
cx q[27], q[11];
cx q[28], q[8];
cx q[29], q[4];
cx q[30], q[6];
cx q[31], q[9];
cx q[32], q[23];
cx q[33], q[3];
cx q[34], q[21];
cx q[35], q[1];
cx q[36], q[18];
barrier q;

cx q[25], q[8];
cx q[26], q[12];
cx q[29], q[7];
cx q[30], q[3];
cx q[31], q[5];
cx q[32], q[0];
cx q[35], q[20];
cx q[36], q[24];
barrier q;

cx q[25], q[15];
cx q[26], q[13];
cx q[29], q[22];
cx q[30], q[14];
cx q[31], q[2];
cx q[32], q[10];
cx q[35], q[19];
cx q[36], q[17];
barrier q;

barrier q;

cz q[37], q[16];
cz q[38], q[13];
cz q[39], q[22];
cz q[40], q[6];
cz q[41], q[7];
cz q[42], q[23];
cz q[43], q[9];
cz q[44], q[3];
cz q[45], q[1];
cz q[46], q[10];
cz q[47], q[19];
cz q[48], q[17];
barrier q;

cz q[37], q[15];
cz q[38], q[12];
cz q[39], q[7];
cz q[40], q[11];
cz q[41], q[9];
cz q[42], q[6];
cz q[43], q[4];
cz q[44], q[23];
cz q[45], q[21];
cz q[46], q[0];
cz q[47], q[20];
cz q[48], q[18];
barrier q;

cz q[39], q[16];
cz q[40], q[13];
cz q[41], q[8];
cz q[42], q[4];
cz q[43], q[10];
cz q[44], q[0];
cz q[45], q[2];
cz q[46], q[19];
barrier q;

cz q[39], q[12];
cz q[40], q[14];
cz q[41], q[5];
cz q[42], q[22];
cz q[43], q[1];
cz q[44], q[24];
cz q[45], q[20];
cz q[46], q[17];
barrier q;

h q[25]; measure q[25] -> rec[0]; h q[25]; // decomposed MX
h q[26]; measure q[26] -> rec[1]; h q[26]; // decomposed MX
h q[27]; measure q[27] -> rec[2]; h q[27]; // decomposed MX
h q[28]; measure q[28] -> rec[3]; h q[28]; // decomposed MX
h q[29]; measure q[29] -> rec[4]; h q[29]; // decomposed MX
h q[30]; measure q[30] -> rec[5]; h q[30]; // decomposed MX
h q[31]; measure q[31] -> rec[6]; h q[31]; // decomposed MX
h q[32]; measure q[32] -> rec[7]; h q[32]; // decomposed MX
h q[33]; measure q[33] -> rec[8]; h q[33]; // decomposed MX
h q[34]; measure q[34] -> rec[9]; h q[34]; // decomposed MX
h q[35]; measure q[35] -> rec[10]; h q[35]; // decomposed MX
h q[36]; measure q[36] -> rec[11]; h q[36]; // decomposed MX
h q[37]; measure q[37] -> rec[12]; h q[37]; // decomposed MX
h q[38]; measure q[38] -> rec[13]; h q[38]; // decomposed MX
h q[39]; measure q[39] -> rec[14]; h q[39]; // decomposed MX
h q[40]; measure q[40] -> rec[15]; h q[40]; // decomposed MX
h q[41]; measure q[41] -> rec[16]; h q[41]; // decomposed MX
h q[42]; measure q[42] -> rec[17]; h q[42]; // decomposed MX
h q[43]; measure q[43] -> rec[18]; h q[43]; // decomposed MX
h q[44]; measure q[44] -> rec[19]; h q[44]; // decomposed MX
h q[45]; measure q[45] -> rec[20]; h q[45]; // decomposed MX
h q[46]; measure q[46] -> rec[21]; h q[46]; // decomposed MX
h q[47]; measure q[47] -> rec[22]; h q[47]; // decomposed MX
h q[48]; measure q[48] -> rec[23]; h q[48]; // decomposed MX
