#! /usr/bin/env python

import argparse
import sys
import logging
import logging.config
from cellmaps_utils import logutils
from cellmaps_utils import constants
import cellmaps_seqms_ppi_gen
from cellmaps_seqms_ppi_gen.runner import CellMapsPPIFromSEQMS

logger = logging.getLogger(__name__)


def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: description to display on command line
    :type desc: str
    :param args: command line arguments usually :py:func:`sys.argv[1:]`
    :type args: list
    :return: arguments parsed by :py:mod:`argparse`
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=constants.ArgParseFormatter)
    parser.add_argument('outdir',
                        help='Directory to write results to')
    parser.add_argument('--seqms',
                        help='Path to SEQ-MS fractions TSV file')
    parser.add_argument('--corum', default='https://mips.helmholtz-muenchen.de/corum/#download',
                        help='Path to CORUM complexes file/zip file or url to download from CORUM')
    parser.add_argument('--docker', default='docker',
                        help='Path to Docker command, needed if running EPIC via Docker')
    parser.add_argument('--apptainer', default='apptainer',
                        help='Path to Apptainer command, needed if running EPIC via Apptainer')
    parser.add_argument('--conda', default='conda',
                        help='Path to conda command, needed if running EPIC via Anaconda')
    parser.add_argument('--conda_env', default='baderlab_epic',
                        help='Name of Anaconda environment where EPIC is installed and can be run')
    parser.add_argument('--num_cores', default=1, type=int,
                        help='Number of cores EPIC can use to run')
    parser.add_argument('--runmode', choices=['apptainer', 'docker', 'conda'],
                        help='Specifies where to run EPIC under')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--exitcode', help='Exit code this command will return',
                        default=0, type=int)
    parser.add_argument('--skip_logging', action='store_true',
                        help='If set, output.log, error.log '
                             'files will not be created')
    parser.add_argument('--provenance',
                        help='Path to file containing provenance '
                             'information about input files in JSON format. '
                             'This is required and not including will output '
                             'and error message with example of file')
    parser.add_argument('--verbose', '-v', action='count', default=1,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = WARNING, -vv = INFO, '
                             '-vvv = DEBUG, -vvvv = NOTSET (default ERROR '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_seqms_ppi_gen.__version__))

    return parser.parse_args(args)


def main(args):
    """
    Main entry point for program

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of :py:meth:`cellmaps_seqms_ppi_gen.runner.CellMapsPPIFromSEQMS.run`
             or ``2`` if an exception is raised
    :rtype: int
    """
    desc = """
    Version {version}

    Generates Protein-Protein interaction edgelist from SEQ-MS fractions TSV file
    using EPIC algorithm from the Baderlab

    """.format(version=cellmaps_seqms_ppi_gen.__version__)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_seqms_ppi_gen.__version__

    try:
        logutils.setup_cmd_logging(theargs)
        return CellMapsPPIFromSEQMS(outdir=theargs.outdir,
                                    exitcode=theargs.exitcode,
                                    skip_logging=theargs.skip_logging,
                                    input_data_dict=theargs.__dict__).run()
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
