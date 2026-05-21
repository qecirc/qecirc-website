OPENQASM 2.0;
include "qelib1.inc";

qreg q[144];

reset q[104];
reset q[92];
reset q[82];
reset q[126];
reset q[78];
reset q[75];
reset q[74];
reset q[73];
reset q[72];
reset q[71];
reset q[69];
reset q[64];
reset q[59];
reset q[58];
reset q[56];
reset q[97];
reset q[86];
reset q[81];
reset q[54];
reset q[50];
reset q[53];
reset q[48];
reset q[47];
reset q[76];
reset q[46];
reset q[52];
reset q[39];
reset q[51];
reset q[49];
reset q[41];
reset q[37];
reset q[34];
reset q[36];
reset q[32];
reset q[31];
reset q[30];
reset q[27];
reset q[26];
reset q[23];
reset q[22];
reset q[135];
reset q[139];
reset q[91];
reset q[127];
reset q[20];
reset q[18];
reset q[17];
reset q[16];
reset q[15];
reset q[14];
reset q[61];
reset q[62];
reset q[60];
reset q[8];
reset q[6];
reset q[44];
reset q[45];
reset q[43];
reset q[85];
reset q[80];
reset q[111];
reset q[141];
reset q[131];
reset q[124];
reset q[118];
reset q[87];
reset q[42]; h q[42]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[35]; h q[35]; // decomposed RX
reset q[33]; h q[33]; // decomposed RX
reset q[29]; h q[29]; // decomposed RX
reset q[28]; h q[28]; // decomposed RX
reset q[25]; h q[25]; // decomposed RX
reset q[24]; h q[24]; // decomposed RX
reset q[21]; h q[21]; // decomposed RX
reset q[19]; h q[19]; // decomposed RX
reset q[57]; h q[57]; // decomposed RX
reset q[13]; h q[13]; // decomposed RX
reset q[12]; h q[12]; // decomposed RX
reset q[11]; h q[11]; // decomposed RX
reset q[10]; h q[10]; // decomposed RX
reset q[9]; h q[9]; // decomposed RX
reset q[7]; h q[7]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[5]; h q[5]; // decomposed RX
reset q[4]; h q[4]; // decomposed RX
reset q[3]; h q[3]; // decomposed RX
reset q[2]; h q[2]; // decomposed RX
reset q[110]; h q[110]; // decomposed RX
reset q[132]; h q[132]; // decomposed RX
reset q[137]; h q[137]; // decomposed RX
reset q[140]; h q[140]; // decomposed RX
reset q[103]; h q[103]; // decomposed RX
reset q[89]; h q[89]; // decomposed RX
reset q[123]; h q[123]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[1]; h q[1]; // decomposed RX
reset q[0]; h q[0]; // decomposed RX
reset q[95]; h q[95]; // decomposed RX
reset q[138]; h q[138]; // decomposed RX
reset q[102]; h q[102]; // decomposed RX
reset q[142]; h q[142]; // decomposed RX
reset q[90]; h q[90]; // decomposed RX
reset q[117]; h q[117]; // decomposed RX
reset q[63]; h q[63]; // decomposed RX
reset q[116]; h q[116]; // decomposed RX
reset q[113]; h q[113]; // decomposed RX
reset q[115]; h q[115]; // decomposed RX
reset q[96]; h q[96]; // decomposed RX
reset q[101]; h q[101]; // decomposed RX
reset q[143]; h q[143]; // decomposed RX
reset q[114]; h q[114]; // decomposed RX
reset q[55]; h q[55]; // decomposed RX
reset q[112]; h q[112]; // decomposed RX
reset q[125]; h q[125]; // decomposed RX
reset q[66]; h q[66]; // decomposed RX
reset q[65]; h q[65]; // decomposed RX
reset q[105]; h q[105]; // decomposed RX
reset q[93]; h q[93]; // decomposed RX
reset q[128]; h q[128]; // decomposed RX
reset q[99]; h q[99]; // decomposed RX
reset q[79]; h q[79]; // decomposed RX
reset q[120]; h q[120]; // decomposed RX
reset q[98]; h q[98]; // decomposed RX
reset q[129]; h q[129]; // decomposed RX
reset q[107]; h q[107]; // decomposed RX
reset q[133]; h q[133]; // decomposed RX
reset q[83]; h q[83]; // decomposed RX
reset q[100]; h q[100]; // decomposed RX
reset q[130]; h q[130]; // decomposed RX
reset q[121]; h q[121]; // decomposed RX
reset q[119]; h q[119]; // decomposed RX
reset q[134]; h q[134]; // decomposed RX
reset q[109]; h q[109]; // decomposed RX
reset q[106]; h q[106]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[94]; h q[94]; // decomposed RX
reset q[84]; h q[84]; // decomposed RX
reset q[136]; h q[136]; // decomposed RX
reset q[88]; h q[88]; // decomposed RX
reset q[122]; h q[122]; // decomposed RX
reset q[77]; h q[77]; // decomposed RX
reset q[68]; h q[68]; // decomposed RX
reset q[108]; h q[108]; // decomposed RX
cx q[88], q[16];
cx q[84], q[18];
cx q[67], q[20];
cx q[83], q[26];
cx q[100], q[37];
cx q[105], q[53];
cx q[65], q[54];
cx q[136], q[78];
cx q[103], q[45];
cx q[134], q[6];
cx q[109], q[62];
cx q[107], q[41];
cx q[99], q[49];
cx q[95], q[59];
cx q[4], q[64];
cx q[98], q[73];
cx q[93], q[92];
cx q[3], q[104];
cx q[79], q[87];
cx q[77], q[141];
cx q[116], q[43];
cx q[121], q[23];
cx q[137], q[51];
cx q[130], q[58];
cx q[142], q[74];
cx q[132], q[15];
cx q[113], q[48];
cx q[70], q[69];
cx q[122], q[124];
cx q[129], q[139];
cx q[125], q[71];
cx q[108], q[67];
cx q[136], q[17];
cx q[94], q[18];
cx q[115], q[20];
cx q[138], q[26];
cx q[102], q[37];
cx q[110], q[53];
cx q[29], q[54];
cx q[88], q[76];
cx q[96], q[78];
cx q[106], q[109];
cx q[105], q[3];
cx q[120], q[45];
cx q[1], q[62];
cx q[134], q[135];
cx q[0], q[41];
cx q[103], q[49];
cx q[10], q[59];
cx q[65], q[64];
cx q[89], q[73];
cx q[2], q[92];
cx q[4], q[104];
cx q[130], q[121];
cx q[87], q[99];
cx q[143], q[141];
cx q[100], q[95];
cx q[128], q[137];
cx q[63], q[43];
cx q[90], q[6];
cx q[98], q[30];
cx q[7], q[74];
cx q[116], q[48];
cx q[122], q[131];
cx q[125], q[127];
cx q[115], q[96];
cx q[108], q[111];
cx q[83], q[102];
cx q[133], q[138];
cx q[136], q[16];
cx q[84], q[17];
cx q[13], q[18];
cx q[40], q[20];
cx q[21], q[26];
cx q[94], q[27];
cx q[66], q[29];
cx q[67], q[32];
cx q[25], q[37];
cx q[28], q[53];
cx q[38], q[54];
cx q[101], q[76];
cx q[42], q[78];
cx q[106], q[107];
cx q[65], q[110];
cx q[140], q[45];
cx q[119], q[135];
cx q[57], q[41];
cx q[24], q[49];
cx q[109], q[50];
cx q[0], q[59];
cx q[5], q[64];
cx q[103], q[73];
cx q[3], q[92];
cx q[10], q[104];
cx q[89], q[79];
cx q[93], q[137];
cx q[128], q[8];
cx q[87], q[14];
cx q[120], q[30];
cx q[99], q[34];
cx q[130], q[36];
cx q[134], q[85];
cx q[98], q[139];
cx q[88], q[131];
cx q[122], q[39];
cx q[2], q[66];
cx q[68], q[111];
cx q[29], q[1];
cx q[28], q[40];
cx q[101], q[13];
cx q[42], q[62];
cx q[11], q[16];
cx q[12], q[17];
cx q[38], q[21];
cx q[18], q[23];
cx q[20], q[25];
cx q[94], q[31];
cx q[112], q[32];
cx q[108], q[46];
cx q[133], q[47];
cx q[26], q[51];
cx q[37], q[53];
cx q[138], q[58];
cx q[96], q[76];
cx q[54], q[78];
cx q[83], q[82];
cx q[107], q[113];
cx q[119], q[142];
cx q[106], q[43];
cx q[102], q[7];
cx q[110], q[15];
cx q[117], q[135];
cx q[67], q[27];
cx q[33], q[49];
cx q[63], q[50];
cx q[19], q[64];
cx q[5], q[69];
cx q[9], q[92];
cx q[99], q[132];
cx q[137], q[14];
cx q[128], q[34];
cx q[100], q[36];
cx q[93], q[52];
cx q[84], q[56];
cx q[120], q[22];
cx q[10], q[131];
cx q[45], q[68];
cx q[38], q[77];
cx q[21], q[111];
cx q[66], q[70];
cx q[62], q[140];
cx q[53], q[6];
cx q[143], q[11];
cx q[141], q[12];
cx q[26], q[13];
cx q[28], q[57];
cx q[24], q[16];
cx q[25], q[17];
cx q[90], q[23];
cx q[112], q[31];
cx q[55], q[32];
cx q[114], q[46];
cx q[1], q[47];
cx q[35], q[51];
cx q[95], q[58];
cx q[78], q[59];
cx q[40], q[73];
cx q[54], q[74];
cx q[41], q[76];
cx q[0], q[82];
cx q[18], q[104];
cx q[49], q[43];
cx q[110], q[8];
cx q[7], q[15];
cx q[96], q[27];
cx q[117], q[50];
cx q[63], q[85];
cx q[119], q[80];
cx q[132], q[14];
cx q[105], q[52];
cx q[115], q[56];
cx q[5], q[129];
cx q[42], q[139];
cx q[123], q[22];
cx q[133], q[60];
cx q[29], q[68];
cx q[51], q[77];
cx q[35], q[121];
cx q[23], q[79];
cx q[59], q[55];
cx q[33], q[114];
cx q[74], q[140];
cx q[142], q[6];
cx q[11], q[19];
cx q[16], q[135];
cx q[70], q[30];
cx q[111], q[31];
cx q[104], q[32];
cx q[64], q[46];
cx q[113], q[47];
cx q[13], q[48];
cx q[9], q[58];
cx q[12], q[69];
cx q[57], q[73];
cx q[53], q[76];
cx q[1], q[82];
cx q[17], q[92];
cx q[2], q[8];
cx q[78], q[15];
cx q[40], q[50];
cx q[132], q[52];
cx q[141], q[39];
cx q[107], q[60];
cx q[117], q[126];
cx q[66], q[127];
cx q[74], q[77];
cx q[32], q[79];
cx q[55], q[114];
cx q[68], q[118];
cx q[64], q[43];
cx q[73], q[6];
cx q[33], q[135];
cx q[19], q[27];
cx q[46], q[30];
cx q[92], q[31];
cx q[140], q[34];
cx q[142], q[36];
cx q[12], q[47];
cx q[104], q[48];
cx q[76], q[58];
cx q[20], q[69];
cx q[121], q[75];
cx q[11], q[82];
cx q[15], q[85];
cx q[16], q[8];
cx q[111], q[56];
cx q[59], q[129];
cx q[101], q[39];
cx q[95], q[60];
cx q[70], q[71];
cx q[3], q[127];
cx q[48], q[79];
cx q[114], q[118];
cx q[77], q[124];
cx q[121], q[80];
cx q[6], q[14];
cx q[43], q[27];
cx q[135], q[30];
cx q[58], q[31];
cx q[25], q[34];
cx q[19], q[36];
cx q[92], q[47];
cx q[69], q[50];
cx q[102], q[75];
cx q[46], q[82];
cx q[139], q[85];
cx q[15], q[131];
cx q[129], q[72];
cx q[47], q[118];
cx q[9], q[124];
cx q[17], q[80];
cx q[79], q[123];
cx q[82], q[8];
cx q[76], q[14];
cx q[31], q[22];
cx q[50], q[34];
cx q[24], q[36];
cx q[27], q[52];
cx q[30], q[56];
cx q[138], q[75];
cx q[32], q[85];
cx q[23], q[131];
cx q[129], q[91];
cx q[34], q[118];
cx q[14], q[124];
cx q[22], q[80];
cx q[47], q[123];
cx q[36], q[52];
cx q[82], q[56];
cx q[8], q[75];
cx q[85], q[44];
cx q[131], q[97];
cx q[27], q[60];
cx q[79], q[61];
cx q[125], q[91];
cx q[69], q[118];
cx q[22], q[124];
cx q[34], q[80];
cx q[52], q[39];
cx q[123], q[72];
cx q[56], q[75];
cx q[143], q[97];
cx q[140], q[61];
cx q[4], q[91];
cx q[118], q[81];
cx q[124], q[86];
cx q[80], q[44];
cx q[75], q[39];
cx q[123], q[71];
cx q[89], q[72];
cx q[37], q[97];
cx q[137], q[61];
cx q[41], q[91];
cx q[124], q[81];
cx q[131], q[86];
cx q[80], q[126];
cx q[90], q[44];
cx q[39], q[60];
cx q[13], q[71];
cx q[43], q[72];
cx q[50], q[97];
cx q[75], q[61];
cx q[58], q[91];
cx q[35], q[81];
cx q[36], q[86];
cx q[45], q[126];
cx q[52], q[44];
cx q[21], q[71];
cx q[60], q[72];
cx q[39], q[127];
cx q[73], q[97];
cx q[71], q[81];
cx q[49], q[86];
cx q[51], q[126];
cx q[72], q[44];
cx q[56], q[127];
cx q[48], q[81];
cx q[72], q[86];
cx q[71], q[126];
cx q[44], q[61];
