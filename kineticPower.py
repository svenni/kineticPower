import math
import os
from fit import FitFile
import fit.messages

mile_to_meters_per_second = 0.44704


def convert_speed(in_speed_m_s):
    if in_speed_m_s is None:
        return 0
    return in_speed_m_s / mile_to_meters_per_second


def convert_speed_to_power(in_speed_mph):
    watts = (5.244820 * in_speed_mph) + (0.019168 * math.pow(in_speed_mph, 3))
    return watts


def add_kinetic_power(in_file):
    fin = FitFile.open(in_file)

    for line in fin:
        if hasattr(line, 'speed'):
            mph = convert_speed(line.speed)
            watts = convert_speed_to_power(mph)
            line.power = watts
    return fin


def save_new_fit_file(fit_data, out_file):
    print 'saving', out_file
    to_delete = []
    for x in fit_data:
        if isinstance(x, fit.messages.activity.DeviceInfo):
            to_delete.append(fit_data.index(x))
        # if isinstance(x, fit.messages.common.FileId):
        #    to_delete.append(fit_data.index(x))
        if isinstance(x, fit.messages.activity.Record):
            if x.speed is None:
                to_delete.append(fit_data.index(x))

    print to_delete
    to_delete.reverse()
    print to_delete
    for x in to_delete:
        del fit_data[x]

    to_delete = []
    for x in fit_data:
        if isinstance(x, fit.messages.activity.DeviceInfo):
            to_delete.append(fit_data.index(x))

    print to_delete

    with FitFile.open(out_file, mode='w') as fout:
        fout.copy(fit_data)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('in_file')
    parser.add_argument('out_file', nargs='?', default=None)

    args = parser.parse_args()

    new_fit = add_kinetic_power(args.in_file)
    outfile = args.out_file
    if outfile is None:
        base, ext = os.path.splitext(args.in_file)
        outfile = base + '_processed' + ext
    save_new_fit_file(new_fit, outfile)
