from pygmyhdl import *
from math import ceil, log2

initialize()

NUM_OF_BITS = 16  # 16
FRAC_BITS = 9  # 9

FILTER_ROWS = 3
FILTER_COLS = 3

INPUT_ROWS = 4
INPUT_COLS = 6

OUTPUT_ROWS = INPUT_ROWS - FILTER_ROWS + 1
OUTPUT_COLS = INPUT_COLS - FILTER_COLS + 1

ADD_COUNT = 10
MULT_COUNT = 10

Input_mat = [[0.3, 0.2, 0.0, 0.5, 0.6, 0.1], [0.1, 0.3, 0.2, 0.5, 0.2, 0.1],
                [0.8, 0.2, 0.3, 0.5, 00.4, 0.2], [0.1, 0.3, 0.0, 0.2, 0.3, 0.4]]

Filter_mat = [[0.1, 0.2, 0.4], [0.2, 0.0, 0.3], [0.2, 0.5, 0.1], [0.0, 0.0, 0.0]]



Output_mat = [[0 for x in range(OUTPUT_COLS)] for y in range(OUTPUT_ROWS)]

Outputt = [0.0 for s in range(OUTPUT_COLS * OUTPUT_ROWS)]


print(Input_mat)
print(Filter_mat)
print(Output_mat)

def to_float(x, Fshift):
    return int(x) / float(1 << Fshift)

def to_fixed(x, Fshift):
    return int(x * (1 << Fshift))


for x in range(FILTER_ROWS):
    for m in range(FILTER_COLS):
        print("i: ", x, "m: ", m, " ", (to_fixed(Filter_mat[x][m], FRAC_BITS)))



@chunk
def adder(A, B, Out):

    @always_comb
    def sum():
        Out.next = A + B

@chunk
def multer(A, B, Out):

    multer_out = Bus(len(A) + len(B), name='multer_out')

    @always_comb
    def mul1():
        multer_out.next = A * B

    @always_comb
    def mul():
        Out.next = multer_out[25:9]



@chunk
def filter_ram(clk_i, en_i, wr_i, row_i, col_i, data_i, data_o):

    addr_len = FILTER_ROWS * FILTER_COLS

    addr = Bus(int(ceil(log2(addr_len))), name='addr')

    mem = [Bus(len(data_i)) for _ in range(2 ** len(addr))]

    @always_comb
    def decoder():
        addr.next = row_i * FILTER_COLS + col_i
    @seq_logic(clk_i.posedge)
    def logic():
        if en_i:
            if wr_i:
                mem[addr.val].next = data_i
            else:
                data_o.next = mem[addr.val]


@chunk
def input_ram(clk_i, en_i, wr_i, row_i, col_i, data_i, data_o):

    addr_len = INPUT_ROWS * INPUT_COLS

    addr = Bus(int(ceil(log2(addr_len))),name='addr')

    mem = [Bus(len(data_i)) for _ in range(2 ** len(addr))]

    @always_comb
    def decoder():
        addr.next = row_i * INPUT_COLS + col_i

    @seq_logic(clk_i.posedge)
    def logic():
        if en_i:
            if wr_i:
                mem[addr.val].next = data_i
            else:
                data_o.next = mem[addr.val]


@chunk
def output_ram(clk_i, en_i, wr_i, row_i, col_i, data_i, data_o):

    addr_len = OUTPUT_ROWS * OUTPUT_COLS

    addr = Bus(int(ceil(log2(addr_len))),name='addr')

    mem = [Bus(len(data_i)) for _ in range(2 ** len(addr))]

    @always_comb
    def decoder():
        addr.next = row_i * OUTPUT_COLS + col_i

    @seq_logic(clk_i.posedge)
    def logic():
        if en_i:
            if wr_i:
                mem[addr.val].next = data_i
            else:
                data_o.next = mem[addr.val]


@chunk
def CNN_Controler(clk_i, fill_req, out_valid, data_i, data_o):

    state = State('INPUT_INIT', 'FILTER_INIT', 'CALCULATE', 'BEFORE_FIN', 'FINISH', 'IDLE', name='state')

    reset_cnt = Bus(2, name='reset_cnt')

    mult_a = Bus(NUM_OF_BITS, name='mult_a')
    mult_b = Bus(NUM_OF_BITS, name='mult_b')
    mult_out = Bus(NUM_OF_BITS, name='mult_out')

    multer(mult_a, mult_b, mult_out)

    add_a = Bus(NUM_OF_BITS, name='add_a')
    add_b = Bus(NUM_OF_BITS, name='add_b')
    add_out = Bus(NUM_OF_BITS, name='add_out')

    adder(add_a, add_b, add_out)

    input_ram_en = Wire(name='input_ram_en')
    input_ram_wr = Wire(name='input_ram_wr')
    input_ram_row = Bus(int(ceil(log2(INPUT_ROWS))), name='input_ram_row')
    input_ram_col = Bus(int(ceil(log2(INPUT_COLS))), name='input_ram_col')
    input_ram_data_in = Bus(NUM_OF_BITS, name='input_ram_data_in')
    input_ram_data_out = Bus(NUM_OF_BITS, name='input_ram_data_out')

    input_ram(clk_i, input_ram_en, input_ram_wr, input_ram_row, input_ram_col, input_ram_data_in, input_ram_data_out)

    filter_ram_en = Wire(name='filter_ram_en')
    filter_ram_wr = Wire(name='filter_ram_wr')
    filter_ram_row = Bus(int(ceil(log2(FILTER_ROWS))), name='filter_ram_row')
    filter_ram_col = Bus(int(ceil(log2(FILTER_COLS))), name='filter_ram_col')
    filter_ram_data_in = Bus(NUM_OF_BITS, name='filter_ram_data_in')
    filter_ram_data_out = Bus(NUM_OF_BITS, name='filter_ram_data_out')

    filter_ram(clk_i, filter_ram_en, filter_ram_wr, filter_ram_row, filter_ram_col, filter_ram_data_in, filter_ram_data_out)

    output_ram_en = Wire(name='output_ram_en')
    output_ram_wr = Wire(name='output_ram_wr')
    output_ram_row = Bus(int(ceil(log2(OUTPUT_ROWS))), name='output_ram_row')
    output_ram_col = Bus(int(ceil(log2(OUTPUT_COLS))), name='output_ram_col')
    output_ram_data_in = Bus(NUM_OF_BITS, name='output_ram_data_in')
    output_ram_data_out = Bus(NUM_OF_BITS, name='output_ram_data_out')

    output_ram(clk_i, output_ram_en, output_ram_wr, output_ram_row, output_ram_col, output_ram_data_in, output_ram_data_out)

    in_row_cnt = Bus(int(ceil(log2(INPUT_ROWS))), name='in_row_cnt')
    in_col_cnt = Bus(int(ceil(log2(INPUT_COLS))), name='in_col_cnt')

    fil_row_cnt = Bus(int(ceil(log2(FILTER_ROWS))), name='fil_row_cnt')
    fil_col_cnt = Bus(int(ceil(log2(FILTER_COLS))), name='fil_col_cnt')

    out_row_cnt = Bus(int(ceil(log2(OUTPUT_ROWS))), name='out_row_cnt')
    out_col_cnt = Bus(int(ceil(log2(OUTPUT_COLS))), name='out_col_cnt')

    acc_cnt = Bus(int(ceil(log2(OUTPUT_COLS * OUTPUT_ROWS)))+1, name= 'out_cnt')
    add_cnt = Bus(int(ceil(log2(ADD_COUNT))), name='add_cnt')
    mult_cnt = Bus(int(ceil(log2(MULT_COUNT))), name='mult_cnt')

    bus0 = Bus(NUM_OF_BITS)
    bus1 = Bus(NUM_OF_BITS)
    bus2 = Bus(NUM_OF_BITS)
    bus3 = Bus(NUM_OF_BITS)
    bus4 = Bus(NUM_OF_BITS)
    bus5 = Bus(NUM_OF_BITS)
    bus6 = Bus(NUM_OF_BITS)
    bus7 = Bus(NUM_OF_BITS)
    bus8 = Bus(NUM_OF_BITS)
    bus9 = Bus(NUM_OF_BITS)
    bus10 = Bus(NUM_OF_BITS)
    bus11 = Bus(NUM_OF_BITS)

    sum = Bus(NUM_OF_BITS, name='sum')

    sum_is_zero = Wire(name='sum_is_zero')
    mult_is_zero = Wire(name='mult_is_zero')
    result_out = Wire(name='result_out')

    buff = Bus(10, name='buff')
    sum_ready = Wire(name='sum_ready')

    finished = Wire(name='finished')

    buffer = Bus(NUM_OF_BITS)
    mat_cnt = Bus(10)

    @comb_logic
    def to_out():
        if result_out:
            data_o.next = output_ram_data_out
        else:
            data_o.next = 0

    @comb_logic
    def in_logic():
        input_ram_col.next = in_col_cnt
        input_ram_row.next = in_row_cnt
        input_ram_data_in.next = data_i

    @comb_logic
    def fil_logic():
        filter_ram_col.next = fil_col_cnt
        filter_ram_row.next = fil_row_cnt
        filter_ram_data_in.next = buffer#Filter_mat[fil_row_cnt.val * FILTER_COLS + fil_col_cnt.val]

    @comb_logic
    def out_logic():
        output_ram_col.next = out_col_cnt
        output_ram_row.next = out_row_cnt
        output_ram_data_in.next = sum

    @comb_logic
    def sum_reset():
        if sum_is_zero == 1:
            sum.next = 0
        else:
            sum.next = add_out

    @comb_logic
    def mul_logic():
        if mult_is_zero:
            mult_a.next = 0
            mult_b.next = 0
        else:
            mult_a.next = input_ram_data_out
            mult_b.next = filter_ram_data_out

    @seq_logic(clk_i.posedge)
    def fsm_logic():
        if reset_cnt < reset_cnt.max-1:
            in_row_cnt.next = 0
            in_col_cnt.next = 0
            fil_row_cnt.next = 0
            fill_req.next = 0
            fil_col_cnt.next = 0
            bus0.next = 51
            bus1.next = 102
            bus2.next = 204
            bus3.next = 102
            bus4.next = 0
            bus5.next = 153
            bus6.next = 102
            bus7.next = 256
            bus8.next = 51
            bus9.next = 0
            bus10.next = 0
            bus11.next = 0
            buffer.next = 0
            out_row_cnt.next = 0
            out_col_cnt.next = 0
            mat_cnt.next = 0
            acc_cnt.next = 0
            out_valid.next = 0
            result_out.next = 0
            finished.next = 0
            sum_is_zero.next = 0
            buff.next = 0
            sum_ready.next = 0
            reset_cnt.next = reset_cnt + 1
            if reset_cnt == reset_cnt.max-1:
                input_ram_en.next = 1
                input_ram_wr.next = 1
                fill_req.next = 1
                state.next = state.s.INPUT_INIT
            elif reset_cnt == reset_cnt.max-2:
                fill_req.next = 1
        elif state == state.s.INPUT_INIT:
            input_ram_en.next = 1
            input_ram_wr.next = 1
            fill_req.next = 1
            if in_col_cnt == (INPUT_COLS-1):
                in_row_cnt.next = in_row_cnt + 1
                in_col_cnt.next = 0
            else:
                in_col_cnt.next = in_col_cnt + 1
            if (in_row_cnt == INPUT_ROWS-1) and (in_col_cnt == INPUT_COLS-1):
                filter_ram_en.next = 1
                filter_ram_wr.next = 1
                if (mat_cnt == 0):
                    buffer.next = bus0
                elif (mat_cnt == 1):
                    buffer.next = bus1
                elif (mat_cnt == 2):
                    buffer.next = bus2
                elif (mat_cnt == 3):
                    buffer.next = bus3
                elif (mat_cnt == 4):
                    buffer.next = bus4
                elif (mat_cnt == 5):
                    buffer.next = bus5
                elif (mat_cnt == 6):
                    buffer.next = bus6
                elif (mat_cnt == 7):
                    buffer.next = bus7
                elif (mat_cnt == 8):
                    buffer.next = bus8
                elif (mat_cnt == 9):
                    buffer.next = bus9
                elif (mat_cnt == 10):
                    buffer.next = bus10
                elif (mat_cnt == 11):
                    buffer.next = bus11
                else:
                    buffer.next = 0
                mat_cnt.next = mat_cnt + 1
                fill_req.next = 0
                state.next = state.s.FILTER_INIT
            elif (in_row_cnt == INPUT_ROWS-1) and (in_col_cnt == INPUT_COLS-2):
                fill_req.next = 0
        elif state == state.s.FILTER_INIT:
            if (fil_col_cnt == 0) and (fil_row_cnt == 0):
                input_ram_en.next = 0
                input_ram_wr.next = 0
                in_row_cnt.next = 0
                in_col_cnt.next = 0
            if fil_col_cnt == (FILTER_COLS-1):
                fil_row_cnt.next = fil_row_cnt + 1
                fil_col_cnt.next = 0
            else:
                fil_col_cnt.next = fil_col_cnt + 1
            mat_cnt.next = mat_cnt + 1
            if (mat_cnt == 0):
                buffer.next = bus0
            elif (mat_cnt == 1):
                buffer.next = bus1
            elif (mat_cnt == 2):
                buffer.next = bus2
            elif (mat_cnt == 3):
                buffer.next = bus3
            elif (mat_cnt == 4):
                buffer.next = bus4
            elif (mat_cnt == 5):
                buffer.next = bus5
            elif (mat_cnt == 6):
                buffer.next = bus6
            elif (mat_cnt == 7):
                buffer.next = bus7
            elif (mat_cnt == 8):
                buffer.next = bus8
            elif (mat_cnt == 9):
                buffer.next = bus9
            elif (mat_cnt == 10):
                buffer.next = bus10
            elif (mat_cnt == 11):
                buffer.next = bus11
            else:
                buffer.next = 0
            filter_ram_en.next = 1
            filter_ram_wr.next = 1
            if (fil_row_cnt == FILTER_ROWS - 1) and (fil_col_cnt == FILTER_COLS - 1):
                buff.next = 4
                fil_row_cnt.next = 0
                fil_col_cnt.next = 0
                in_col_cnt.next = 0
                in_row_cnt.next = 0
                input_ram_en.next = 1
                input_ram_wr.next = 0
                filter_ram_en.next = 1
                filter_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                sum_is_zero.next = 1
                mult_is_zero.next = 1
                state.next = state.s.CALCULATE
        elif state == state.s.CALCULATE:  # main calc
            if buff == 4:
                buff.next = 3
                in_col_cnt.next = 0
                in_row_cnt.next = 0
                input_ram_en.next = 1
                input_ram_wr.next = 0
                filter_ram_en.next = 1
                filter_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                out_col_cnt.next = 0
                out_row_cnt.next = 0
                sum_is_zero.next = 0
                mult_is_zero.next = 1
                fil_row_cnt.next = 0
                fil_col_cnt.next = 0
                buff.next = 5
            elif buff < 3:
                buff.next = buff + 1
                in_col_cnt.next = out_col_cnt
                in_row_cnt.next = out_row_cnt
                add_a.next = sum
                add_b.next = mult_out
                sum_is_zero.next = 1
            elif buff == 6:
                sum_is_zero.next = 1 # 1
                output_ram_en.next = 1
                output_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                buff.next = 8
                sum_ready.next = 0
                mult_is_zero.next = 1
            elif buff == 7:
                sum_is_zero.next = 0 # 1
                output_ram_en.next = 1
                output_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                buff.next = 6
                sum_ready.next = 0
                mult_is_zero.next = 1
            elif buff == 8:
                add_a.next = sum
                add_b.next = mult_out
                if out_col_cnt == (OUTPUT_COLS - 1):
                    out_row_cnt.next = out_row_cnt + 1
                    out_col_cnt.next = 0
                    buff.next = 7
                else:
                    out_col_cnt.next = out_col_cnt + 1
                    buff.next = 7
                sum_is_zero.next = 1
                mult_is_zero.next = 1
                buff.next = 5
            else:
                if (fil_col_cnt == 0) and (fil_row_cnt == FILTER_ROWS):
                    fil_row_cnt.next = 0
                    fil_col_cnt.next = 0
                    if (out_col_cnt == OUTPUT_COLS-1):
                        in_col_cnt.next = 0
                        in_row_cnt.next = out_row_cnt + 1
                    else:
                        in_col_cnt.next = out_col_cnt + 1
                        in_row_cnt.next = out_row_cnt
                    buff.next = 7 ###2
                    sum_is_zero.next = 1
                elif fil_col_cnt == (FILTER_COLS-1):
                    fil_row_cnt.next = fil_row_cnt + 1
                    fil_col_cnt.next = 0  # tutaj tez wejscie zmieniac
                    in_col_cnt.next = out_col_cnt
                    in_row_cnt.next = out_row_cnt + fil_row_cnt + 1
                else:
                    fil_col_cnt.next = fil_col_cnt + 1
                    in_col_cnt.next = out_col_cnt + fil_col_cnt + 1
                sum_is_zero.next = 0
                mult_is_zero.next = 0
                sum_ready.next = 0
                input_ram_en.next = 1
                input_ram_wr.next = 0
                filter_ram_en.next = 1
                filter_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                if (fil_col_cnt == 0) and (fil_row_cnt == FILTER_ROWS):
                    if (out_row_cnt == OUTPUT_ROWS-1) and (out_col_cnt == OUTPUT_COLS-1):
                        state.next = state.s.BEFORE_FIN
                        buff.next = 0
                    sum_ready.next = 1
                    output_ram_en.next = 1
                    output_ram_wr.next = 1
                    mult_is_zero.next = 1
                    sum_is_zero.next = 0
        elif state == state.s.BEFORE_FIN:
            if buff == 0:
                sum_is_zero.next = 1
                out_row_cnt.next = 0
                out_col_cnt.next = 0
                output_ram_en.next = 1
                output_ram_wr.next = 0
                add_a.next = sum
                add_b.next = mult_out
                buff.next = 6
                sum_ready.next = 0
                mult_is_zero.next = 1
                buff.next = 1
            if buff == 1:
                output_ram_en.next = 1
                output_ram_wr.next = 0
                state.next = state.s.FINISH
        elif state == state.s.FINISH:       # when finished
            acc_cnt.next = acc_cnt + 1
            out_valid.next = 1
            if out_col_cnt == (OUTPUT_COLS-1):
                out_row_cnt.next = out_row_cnt + 1
                out_col_cnt.next = 0
            else:
                out_col_cnt.next = out_col_cnt + 1
            result_out.next = 1
            print("output[", acc_cnt, "] = ", to_float(output_ram_data_out, FRAC_BITS)) ## COMMENT UP TO RUN VERILOG
            output_ram_en.next = 1
            output_ram_wr.next = 0
            if acc_cnt == (OUTPUT_ROWS * OUTPUT_COLS): # - 1
                reset_cnt.next = 0
                result_out.next = 0
                state.next = state.s.IDLE
        elif state == state.s.IDLE:
            sum_is_zero.next = 1
            mult_is_zero.next = 1
            out_valid.next = 0
            input_ram_en.next = 0
            input_ram_wr.next = 0
            filter_ram_en.next = 0
            filter_ram_wr.next = 0
        else:
            # If the FSM is in some unknown state, send it back to the starting state.
            state.next = state.s.FINISH



def CNN_tb():
    idx_row = Bus(20, name='idx_row')
    idx_col = Bus(20, name='idx_col')
    out_cnt = Bus(20, name='out_cnt')
    idx_row.next = 0
    idx_col.next = 0
    out_cnt.next = 0
    for _ in range(152):
        clk.next = 0
        if fill_req:
            data_in.next = to_fixed(Input_mat[idx_row.val][idx_col.val], FRAC_BITS)
            if idx_col == (INPUT_COLS-1):
                idx_row.next = idx_row + 1
                idx_col.next = 0
            else:
                idx_col.next = idx_col + 1
        if out_valid:
            out_cnt.next = out_cnt + 1
            if (out_cnt < OUTPUT_ROWS * OUTPUT_COLS):
                Outputt[int(out_cnt.val)] = to_float(data_out, FRAC_BITS)  ## COMMENT OUT TO RUN VERILOG
                print("dummy")
        yield delay(1)

        clk.next = 1

        yield delay(1)


def print_ref():
    for m in range(OUTPUT_ROWS):
        for n in range(OUTPUT_COLS):
            for x in range(FILTER_ROWS):
                for y in range(FILTER_COLS):
                    Output_mat[m][n] += Filter_mat[x][y] * Input_mat[x + m][y + n]
            print("Out: ", to_fixed(Output_mat[m][n], FRAC_BITS))
    print("OUTPUT REFERENCE: ")
    print(Output_mat)


clk = Wire(name='clk')
data_out = Bus(NUM_OF_BITS, name='data_out')
data_in = Bus(NUM_OF_BITS, name='data_in')
out_valid = Wire(name='out_valid')
fill_req = Wire(name='fill_req')

CNN_Controler(clk, fill_req, out_valid, data_in, data_out)
simulate(CNN_tb())

print_ref()
print(Outputt)

#toVerilog(CNN_Controler, clk_i=Wire(), fill_req=Wire(), out_valid=Wire(), data_i=Bus(16), data_o=Bus(16))  # READ HIGHER
