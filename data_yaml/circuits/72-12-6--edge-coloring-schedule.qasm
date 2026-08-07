OPENQASM 2.0;
include "qelib1.inc";

qreg q[144];
creg rec[72];

reset q[72]; h q[72]; // decomposed RX
reset q[73]; h q[73]; // decomposed RX
reset q[74]; h q[74]; // decomposed RX
reset q[75]; h q[75]; // decomposed RX
reset q[76]; h q[76]; // decomposed RX
reset q[77]; h q[77]; // decomposed RX
reset q[78]; h q[78]; // decomposed RX
reset q[79]; h q[79]; // decomposed RX
reset q[80]; h q[80]; // decomposed RX
reset q[81]; h q[81]; // decomposed RX
reset q[82]; h q[82]; // decomposed RX
reset q[83]; h q[83]; // decomposed RX
reset q[84]; h q[84]; // decomposed RX
reset q[85]; h q[85]; // decomposed RX
reset q[86]; h q[86]; // decomposed RX
reset q[87]; h q[87]; // decomposed RX
reset q[88]; h q[88]; // decomposed RX
reset q[89]; h q[89]; // decomposed RX
reset q[90]; h q[90]; // decomposed RX
reset q[91]; h q[91]; // decomposed RX
reset q[92]; h q[92]; // decomposed RX
reset q[93]; h q[93]; // decomposed RX
reset q[94]; h q[94]; // decomposed RX
reset q[95]; h q[95]; // decomposed RX
reset q[96]; h q[96]; // decomposed RX
reset q[97]; h q[97]; // decomposed RX
reset q[98]; h q[98]; // decomposed RX
reset q[99]; h q[99]; // decomposed RX
reset q[100]; h q[100]; // decomposed RX
reset q[101]; h q[101]; // decomposed RX
reset q[102]; h q[102]; // decomposed RX
reset q[103]; h q[103]; // decomposed RX
reset q[104]; h q[104]; // decomposed RX
reset q[105]; h q[105]; // decomposed RX
reset q[106]; h q[106]; // decomposed RX
reset q[107]; h q[107]; // decomposed RX
reset q[108]; h q[108]; // decomposed RX
reset q[109]; h q[109]; // decomposed RX
reset q[110]; h q[110]; // decomposed RX
reset q[111]; h q[111]; // decomposed RX
reset q[112]; h q[112]; // decomposed RX
reset q[113]; h q[113]; // decomposed RX
reset q[114]; h q[114]; // decomposed RX
reset q[115]; h q[115]; // decomposed RX
reset q[116]; h q[116]; // decomposed RX
reset q[117]; h q[117]; // decomposed RX
reset q[118]; h q[118]; // decomposed RX
reset q[119]; h q[119]; // decomposed RX
reset q[120]; h q[120]; // decomposed RX
reset q[121]; h q[121]; // decomposed RX
reset q[122]; h q[122]; // decomposed RX
reset q[123]; h q[123]; // decomposed RX
reset q[124]; h q[124]; // decomposed RX
reset q[125]; h q[125]; // decomposed RX
reset q[126]; h q[126]; // decomposed RX
reset q[127]; h q[127]; // decomposed RX
reset q[128]; h q[128]; // decomposed RX
reset q[129]; h q[129]; // decomposed RX
reset q[130]; h q[130]; // decomposed RX
reset q[131]; h q[131]; // decomposed RX
reset q[132]; h q[132]; // decomposed RX
reset q[133]; h q[133]; // decomposed RX
reset q[134]; h q[134]; // decomposed RX
reset q[135]; h q[135]; // decomposed RX
reset q[136]; h q[136]; // decomposed RX
reset q[137]; h q[137]; // decomposed RX
reset q[138]; h q[138]; // decomposed RX
reset q[139]; h q[139]; // decomposed RX
reset q[140]; h q[140]; // decomposed RX
reset q[141]; h q[141]; // decomposed RX
reset q[142]; h q[142]; // decomposed RX
reset q[143]; h q[143]; // decomposed RX
barrier q;

cz q[108], q[40];
cz q[109], q[5];
cz q[110], q[4];
cz q[111], q[3];
cz q[112], q[2];
cz q[113], q[57];
cz q[114], q[56];
cz q[115], q[1];
cz q[116], q[0];
cz q[117], q[63];
cz q[118], q[25];
cz q[119], q[62];
cz q[120], q[61];
cz q[121], q[58];
cz q[122], q[59];
cz q[123], q[64];
cz q[124], q[60];
cz q[125], q[32];
cz q[126], q[68];
cz q[127], q[66];
cz q[128], q[38];
cz q[129], q[36];
cz q[130], q[54];
cz q[131], q[48];
cz q[132], q[52];
cz q[133], q[55];
cz q[134], q[69];
cz q[135], q[44];
cz q[136], q[65];
cz q[137], q[51];
cz q[138], q[53];
cz q[139], q[37];
cz q[140], q[49];
cz q[141], q[45];
cz q[142], q[42];
cz q[143], q[35];
barrier q;

barrier q;

cz q[108], q[57];
cz q[109], q[40];
cz q[110], q[5];
cz q[111], q[4];
cz q[112], q[3];
cz q[113], q[2];
cz q[114], q[62];
cz q[115], q[56];
cz q[116], q[1];
cz q[117], q[0];
cz q[118], q[63];
cz q[119], q[25];
cz q[120], q[32];
cz q[121], q[61];
cz q[122], q[58];
cz q[123], q[59];
cz q[124], q[64];
cz q[125], q[60];
cz q[126], q[48];
cz q[127], q[68];
cz q[128], q[66];
cz q[129], q[38];
cz q[130], q[36];
cz q[131], q[54];
cz q[132], q[51];
cz q[133], q[52];
cz q[134], q[55];
cz q[135], q[69];
cz q[136], q[44];
cz q[137], q[65];
cz q[138], q[35];
cz q[139], q[53];
cz q[140], q[37];
cz q[141], q[49];
cz q[142], q[45];
cz q[143], q[42];
barrier q;

barrier q;

cx q[72], q[11];
cx q[73], q[10];
cx q[74], q[70];
cx q[75], q[71];
cx q[76], q[46];
cx q[77], q[67];
cx q[78], q[9];
cx q[79], q[8];
cx q[80], q[31];
cx q[81], q[33];
cx q[82], q[27];
cx q[83], q[30];
cx q[84], q[7];
cx q[85], q[6];
cx q[86], q[20];
cx q[87], q[21];
cx q[88], q[16];
cx q[89], q[19];
cx q[90], q[50];
cx q[91], q[47];
cx q[92], q[43];
cx q[93], q[41];
cx q[94], q[39];
cx q[95], q[34];
cx q[96], q[29];
cx q[97], q[28];
cx q[98], q[26];
cx q[99], q[24];
cx q[100], q[23];
cx q[101], q[22];
cx q[102], q[18];
cx q[103], q[17];
cx q[104], q[15];
cx q[105], q[14];
cx q[106], q[13];
cx q[107], q[12];
barrier q;

barrier q;

cx q[72], q[1];
cx q[73], q[0];
cx q[74], q[63];
cx q[75], q[25];
cx q[76], q[62];
cx q[77], q[56];
cx q[78], q[58];
cx q[79], q[59];
cx q[80], q[64];
cx q[81], q[60];
cx q[82], q[32];
cx q[83], q[61];
cx q[84], q[66];
cx q[85], q[38];
cx q[86], q[36];
cx q[87], q[54];
cx q[88], q[48];
cx q[89], q[68];
cx q[90], q[55];
cx q[91], q[69];
cx q[92], q[44];
cx q[93], q[65];
cx q[94], q[51];
cx q[95], q[52];
cx q[96], q[37];
cx q[97], q[49];
cx q[98], q[45];
cx q[99], q[42];
cx q[100], q[35];
cx q[101], q[53];
cx q[102], q[5];
cx q[103], q[4];
cx q[104], q[3];
cx q[105], q[2];
cx q[106], q[57];
cx q[107], q[40];
barrier q;

barrier q;

cx q[72], q[58];
cx q[73], q[59];
cx q[74], q[64];
cx q[75], q[60];
cx q[76], q[32];
cx q[77], q[61];
cx q[78], q[66];
cx q[79], q[38];
cx q[80], q[36];
cx q[81], q[54];
cx q[82], q[48];
cx q[83], q[68];
cx q[84], q[55];
cx q[85], q[69];
cx q[86], q[44];
cx q[87], q[65];
cx q[88], q[51];
cx q[89], q[52];
cx q[90], q[37];
cx q[91], q[49];
cx q[92], q[45];
cx q[93], q[42];
cx q[94], q[35];
cx q[95], q[53];
cx q[96], q[5];
cx q[97], q[4];
cx q[98], q[3];
cx q[99], q[2];
cx q[100], q[57];
cx q[101], q[40];
cx q[102], q[1];
cx q[103], q[0];
cx q[104], q[63];
cx q[105], q[25];
cx q[106], q[62];
cx q[107], q[56];
barrier q;

barrier q;

cx q[72], q[2];
cx q[73], q[57];
cx q[74], q[40];
cx q[75], q[5];
cx q[76], q[4];
cx q[77], q[3];
cx q[78], q[25];
cx q[79], q[62];
cx q[80], q[56];
cx q[81], q[1];
cx q[82], q[0];
cx q[83], q[63];
cx q[84], q[60];
cx q[85], q[32];
cx q[86], q[61];
cx q[87], q[58];
cx q[88], q[59];
cx q[89], q[64];
cx q[90], q[54];
cx q[91], q[48];
cx q[92], q[68];
cx q[93], q[66];
cx q[94], q[38];
cx q[95], q[36];
cx q[96], q[65];
cx q[97], q[51];
cx q[98], q[52];
cx q[99], q[55];
cx q[100], q[69];
cx q[101], q[44];
cx q[102], q[42];
cx q[103], q[35];
cx q[104], q[53];
cx q[105], q[37];
cx q[106], q[49];
cx q[107], q[45];
barrier q;

barrier q;

cz q[108], q[7];
cz q[109], q[6];
cz q[110], q[20];
cz q[111], q[21];
cz q[112], q[16];
cz q[113], q[19];
cz q[114], q[50];
cz q[115], q[47];
cz q[116], q[43];
cz q[117], q[41];
cz q[118], q[39];
cz q[119], q[34];
cz q[120], q[29];
cz q[121], q[28];
cz q[122], q[26];
cz q[123], q[24];
cz q[124], q[23];
cz q[125], q[22];
cz q[126], q[18];
cz q[127], q[17];
cz q[128], q[15];
cz q[129], q[14];
cz q[130], q[13];
cz q[131], q[12];
cz q[132], q[11];
cz q[133], q[10];
cz q[134], q[70];
cz q[135], q[71];
cz q[136], q[46];
cz q[137], q[67];
cz q[138], q[9];
cz q[139], q[8];
cz q[140], q[31];
cz q[141], q[33];
cz q[142], q[27];
cz q[143], q[30];
barrier q;

barrier q;

cz q[108], q[9];
cz q[109], q[8];
cz q[110], q[31];
cz q[111], q[33];
cz q[112], q[27];
cz q[113], q[30];
cz q[114], q[7];
cz q[115], q[6];
cz q[116], q[20];
cz q[117], q[21];
cz q[118], q[16];
cz q[119], q[19];
cz q[120], q[50];
cz q[121], q[47];
cz q[122], q[43];
cz q[123], q[41];
cz q[124], q[39];
cz q[125], q[34];
cz q[126], q[29];
cz q[127], q[28];
cz q[128], q[26];
cz q[129], q[24];
cz q[130], q[23];
cz q[131], q[22];
cz q[132], q[18];
cz q[133], q[17];
cz q[134], q[15];
cz q[135], q[14];
cz q[136], q[13];
cz q[137], q[12];
cz q[138], q[11];
cz q[139], q[10];
cz q[140], q[70];
cz q[141], q[71];
cz q[142], q[46];
cz q[143], q[67];
barrier q;

barrier q;

cz q[108], q[41];
cz q[109], q[39];
cz q[110], q[34];
cz q[111], q[50];
cz q[112], q[47];
cz q[113], q[43];
cz q[114], q[24];
cz q[115], q[23];
cz q[116], q[22];
cz q[117], q[29];
cz q[118], q[28];
cz q[119], q[26];
cz q[120], q[14];
cz q[121], q[13];
cz q[122], q[12];
cz q[123], q[18];
cz q[124], q[17];
cz q[125], q[15];
cz q[126], q[71];
cz q[127], q[46];
cz q[128], q[67];
cz q[129], q[11];
cz q[130], q[10];
cz q[131], q[70];
cz q[132], q[33];
cz q[133], q[27];
cz q[134], q[30];
cz q[135], q[9];
cz q[136], q[8];
cz q[137], q[31];
cz q[138], q[21];
cz q[139], q[16];
cz q[140], q[19];
cz q[141], q[7];
cz q[142], q[6];
cz q[143], q[20];
barrier q;

barrier q;

cz q[108], q[66];
cz q[109], q[38];
cz q[110], q[36];
cz q[111], q[54];
cz q[112], q[48];
cz q[113], q[68];
cz q[114], q[55];
cz q[115], q[69];
cz q[116], q[44];
cz q[117], q[65];
cz q[118], q[51];
cz q[119], q[52];
cz q[120], q[37];
cz q[121], q[49];
cz q[122], q[45];
cz q[123], q[42];
cz q[124], q[35];
cz q[125], q[53];
cz q[126], q[5];
cz q[127], q[4];
cz q[128], q[3];
cz q[129], q[2];
cz q[130], q[57];
cz q[131], q[40];
cz q[132], q[1];
cz q[133], q[0];
cz q[134], q[63];
cz q[135], q[25];
cz q[136], q[62];
cz q[137], q[56];
cz q[138], q[58];
cz q[139], q[59];
cz q[140], q[64];
cz q[141], q[60];
cz q[142], q[32];
cz q[143], q[61];
barrier q;

barrier q;

cx q[72], q[47];
cx q[73], q[43];
cx q[74], q[41];
cx q[75], q[39];
cx q[76], q[34];
cx q[77], q[50];
cx q[78], q[28];
cx q[79], q[26];
cx q[80], q[24];
cx q[81], q[23];
cx q[82], q[22];
cx q[83], q[29];
cx q[84], q[17];
cx q[85], q[15];
cx q[86], q[14];
cx q[87], q[13];
cx q[88], q[12];
cx q[89], q[18];
cx q[90], q[10];
cx q[91], q[70];
cx q[92], q[71];
cx q[93], q[46];
cx q[94], q[67];
cx q[95], q[11];
cx q[96], q[8];
cx q[97], q[31];
cx q[98], q[33];
cx q[99], q[27];
cx q[100], q[30];
cx q[101], q[9];
cx q[102], q[6];
cx q[103], q[20];
cx q[104], q[21];
cx q[105], q[16];
cx q[106], q[19];
cx q[107], q[7];
barrier q;

barrier q;

cx q[72], q[43];
cx q[73], q[41];
cx q[74], q[39];
cx q[75], q[34];
cx q[76], q[50];
cx q[77], q[47];
cx q[78], q[26];
cx q[79], q[24];
cx q[80], q[23];
cx q[81], q[22];
cx q[82], q[29];
cx q[83], q[28];
cx q[84], q[15];
cx q[85], q[14];
cx q[86], q[13];
cx q[87], q[12];
cx q[88], q[18];
cx q[89], q[17];
cx q[90], q[70];
cx q[91], q[71];
cx q[92], q[46];
cx q[93], q[67];
cx q[94], q[11];
cx q[95], q[10];
cx q[96], q[31];
cx q[97], q[33];
cx q[98], q[27];
cx q[99], q[30];
cx q[100], q[9];
cx q[101], q[8];
cx q[102], q[20];
cx q[103], q[21];
cx q[104], q[16];
cx q[105], q[19];
cx q[106], q[7];
cx q[107], q[6];
barrier q;

h q[72]; measure q[72] -> rec[0]; h q[72]; // decomposed MX
h q[73]; measure q[73] -> rec[1]; h q[73]; // decomposed MX
h q[74]; measure q[74] -> rec[2]; h q[74]; // decomposed MX
h q[75]; measure q[75] -> rec[3]; h q[75]; // decomposed MX
h q[76]; measure q[76] -> rec[4]; h q[76]; // decomposed MX
h q[77]; measure q[77] -> rec[5]; h q[77]; // decomposed MX
h q[78]; measure q[78] -> rec[6]; h q[78]; // decomposed MX
h q[79]; measure q[79] -> rec[7]; h q[79]; // decomposed MX
h q[80]; measure q[80] -> rec[8]; h q[80]; // decomposed MX
h q[81]; measure q[81] -> rec[9]; h q[81]; // decomposed MX
h q[82]; measure q[82] -> rec[10]; h q[82]; // decomposed MX
h q[83]; measure q[83] -> rec[11]; h q[83]; // decomposed MX
h q[84]; measure q[84] -> rec[12]; h q[84]; // decomposed MX
h q[85]; measure q[85] -> rec[13]; h q[85]; // decomposed MX
h q[86]; measure q[86] -> rec[14]; h q[86]; // decomposed MX
h q[87]; measure q[87] -> rec[15]; h q[87]; // decomposed MX
h q[88]; measure q[88] -> rec[16]; h q[88]; // decomposed MX
h q[89]; measure q[89] -> rec[17]; h q[89]; // decomposed MX
h q[90]; measure q[90] -> rec[18]; h q[90]; // decomposed MX
h q[91]; measure q[91] -> rec[19]; h q[91]; // decomposed MX
h q[92]; measure q[92] -> rec[20]; h q[92]; // decomposed MX
h q[93]; measure q[93] -> rec[21]; h q[93]; // decomposed MX
h q[94]; measure q[94] -> rec[22]; h q[94]; // decomposed MX
h q[95]; measure q[95] -> rec[23]; h q[95]; // decomposed MX
h q[96]; measure q[96] -> rec[24]; h q[96]; // decomposed MX
h q[97]; measure q[97] -> rec[25]; h q[97]; // decomposed MX
h q[98]; measure q[98] -> rec[26]; h q[98]; // decomposed MX
h q[99]; measure q[99] -> rec[27]; h q[99]; // decomposed MX
h q[100]; measure q[100] -> rec[28]; h q[100]; // decomposed MX
h q[101]; measure q[101] -> rec[29]; h q[101]; // decomposed MX
h q[102]; measure q[102] -> rec[30]; h q[102]; // decomposed MX
h q[103]; measure q[103] -> rec[31]; h q[103]; // decomposed MX
h q[104]; measure q[104] -> rec[32]; h q[104]; // decomposed MX
h q[105]; measure q[105] -> rec[33]; h q[105]; // decomposed MX
h q[106]; measure q[106] -> rec[34]; h q[106]; // decomposed MX
h q[107]; measure q[107] -> rec[35]; h q[107]; // decomposed MX
h q[108]; measure q[108] -> rec[36]; h q[108]; // decomposed MX
h q[109]; measure q[109] -> rec[37]; h q[109]; // decomposed MX
h q[110]; measure q[110] -> rec[38]; h q[110]; // decomposed MX
h q[111]; measure q[111] -> rec[39]; h q[111]; // decomposed MX
h q[112]; measure q[112] -> rec[40]; h q[112]; // decomposed MX
h q[113]; measure q[113] -> rec[41]; h q[113]; // decomposed MX
h q[114]; measure q[114] -> rec[42]; h q[114]; // decomposed MX
h q[115]; measure q[115] -> rec[43]; h q[115]; // decomposed MX
h q[116]; measure q[116] -> rec[44]; h q[116]; // decomposed MX
h q[117]; measure q[117] -> rec[45]; h q[117]; // decomposed MX
h q[118]; measure q[118] -> rec[46]; h q[118]; // decomposed MX
h q[119]; measure q[119] -> rec[47]; h q[119]; // decomposed MX
h q[120]; measure q[120] -> rec[48]; h q[120]; // decomposed MX
h q[121]; measure q[121] -> rec[49]; h q[121]; // decomposed MX
h q[122]; measure q[122] -> rec[50]; h q[122]; // decomposed MX
h q[123]; measure q[123] -> rec[51]; h q[123]; // decomposed MX
h q[124]; measure q[124] -> rec[52]; h q[124]; // decomposed MX
h q[125]; measure q[125] -> rec[53]; h q[125]; // decomposed MX
h q[126]; measure q[126] -> rec[54]; h q[126]; // decomposed MX
h q[127]; measure q[127] -> rec[55]; h q[127]; // decomposed MX
h q[128]; measure q[128] -> rec[56]; h q[128]; // decomposed MX
h q[129]; measure q[129] -> rec[57]; h q[129]; // decomposed MX
h q[130]; measure q[130] -> rec[58]; h q[130]; // decomposed MX
h q[131]; measure q[131] -> rec[59]; h q[131]; // decomposed MX
h q[132]; measure q[132] -> rec[60]; h q[132]; // decomposed MX
h q[133]; measure q[133] -> rec[61]; h q[133]; // decomposed MX
h q[134]; measure q[134] -> rec[62]; h q[134]; // decomposed MX
h q[135]; measure q[135] -> rec[63]; h q[135]; // decomposed MX
h q[136]; measure q[136] -> rec[64]; h q[136]; // decomposed MX
h q[137]; measure q[137] -> rec[65]; h q[137]; // decomposed MX
h q[138]; measure q[138] -> rec[66]; h q[138]; // decomposed MX
h q[139]; measure q[139] -> rec[67]; h q[139]; // decomposed MX
h q[140]; measure q[140] -> rec[68]; h q[140]; // decomposed MX
h q[141]; measure q[141] -> rec[69]; h q[141]; // decomposed MX
h q[142]; measure q[142] -> rec[70]; h q[142]; // decomposed MX
h q[143]; measure q[143] -> rec[71]; h q[143]; // decomposed MX
