import sys

sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # input
    to_input('sample_occ_dem.jpg', to='(-4,0,0)'),
    to_input('sample_occ_mask', to='(-3,0,0)'),

    # block-001
    to_ConvConvRelu(name='ccr_b1', s_filer=64, n_filer=(64, 64), offset="(0,0,0)", to="(0,0,0)", width=(2, 2),
                    height=40, depth=40),
    to_Pool(name="pool_b1", offset="(0,0,0)", to="(ccr_b1-east)", width=1, height=32, depth=32, opacity=0.5),

    *block_2ConvPool(name='b2', botton='pool_b1', top='pool_b2', s_filer=32, n_filer=128, offset="(1,0,0)",
                     size=(25, 25, 4.5), opacity=0.5),

    # Bottleneck
    # block-003
    to_ConvConvRelu(name='ccr_b3', s_filer=16, n_filer=(256, 256), offset="(2,0,0)", to="(pool_b2-east)",
                    width=(8, 8), height=8, depth=8, caption="Bottleneck"),
    to_connection("pool_b2", "ccr_b3"),

    # Decoder
    *block_UpConvConvRelu(name="b4", botton="ccr_b3", top='ccr_res_c_b4', s_filer=32, n_filer=128, offset="(2.1,0,0)",
                  size=(25, 25, 5.0), opacity=0.5),
    to_skip(of='ccr_b2', to='ccr_res_b4', pos=1.25),
    *block_UpConvConvRelu(name="b5", botton="ccr_res_c_b4", top='ccr_res_c_b5', s_filer=64, n_filer=64, offset="(2.1,0,0)",
                  size=(40, 40, 3.5), opacity=0.5),
    to_skip(of='ccr_b1', to='ccr_res_b5', pos=1.25),

    to_input('sample_rec_dem.jpg', to='(19,0,0)', name="rec_dem-west"),
    # to_connection("end_b5", 'rec_dem'),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()

