#! /usr/bin/env python

import os
import time
import logging
from cellmaps_utils import logutils
from cellmaps_utils.provenance import ProvenanceUtil
from cellmaps_seqms_ppi_gen.exceptions import CellmapsseqmsppigenError

import cellmaps_seqms_ppi_gen

logger = logging.getLogger(__name__)


class CellMapsPPIFromSEQMS(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None,
                 exitcode=None,
                 skip_logging=True,
                 input_data_dict=None,
                 provenance_utils=ProvenanceUtil()):
        """
        Constructor

        :param outdir: Directory to create and put results in
        :type outdir: str
        :param skip_logging: If ``True`` skip logging, if ``None`` or ``False`` do NOT skip logging
        :type skip_logging: bool
        :param exitcode: value to return via :py:meth:`.CellMapsPPIFromSEQMS.run` method
        :type int:
        :param input_data_dict: Command line arguments used to invoke this
        :type input_data_dict: dict
        :param provenance_utils: Wrapper for `fairscape-cli <https://pypi.org/project/fairscape-cli>`__
                                 which is used for
                                 `RO-Crate <https://www.researchobject.org/ro-crate>`__ creation and population
        :type provenance_utils: :py:class:`~cellmaps_utils.provenance.ProvenanceUtil`
        """
        if outdir is None:
            raise CellmapsseqmsppigenError('outdir is None')

        self._outdir = os.path.abspath(outdir)
        self._exitcode = exitcode
        self._start_time = int(time.time())
        if skip_logging is None:
            self._skip_logging = False
        else:
            self._skip_logging = skip_logging
        self._input_data_dict = input_data_dict
        self._provenance_utils = provenance_utils

        logger.debug('In constructor')

    def run(self):
        """
        Runs Cell Maps SEQ-MS Protein-Protein Edgelist Generator


        :return:
        """
        exitcode = 99
        try:
            logger.debug('In run method')
            if os.path.isdir(self._outdir):
                raise CellmapsseqmsppigenError(self._outdir + ' already exists')
            if not os.path.isdir(self._outdir):
                os.makedirs(self._outdir, mode=0o755)
            if self._skip_logging is False:
                logutils.setup_filelogger(outdir=self._outdir,
                                          handlerprefix='cellmaps_seqms_ppi_gen')
            logutils.write_task_start_json(outdir=self._outdir,
                                           start_time=self._start_time,
                                           data={'commandlineargs': self._input_data_dict},
                                           version=cellmaps_seqms_ppi_gen.__version__)

            # TODO: 1) Load SEQ-MS, do clean up noted in UD-2899 and register with FAIRSCAPE
            #       2) Create SEQ-MS input file needed by EPIC (register with FAIRSCAPE too)
            #       3) Obtain CORUM complexes and structure correctly for EPIC (register with FAIRSCAPE)
            #       4) Setup EPIC output folders
            #       5) Run EPIC
            #       6) Extract output and store in generalized TSV file with
            #          SOURCE TARGET SOURCE_UNIPROT SOURCE_ENSEMBL, SOURCE_GENE_SYMBOL, TARGET (same) and SCORE
            #          (register with fairscape)


            # set exit code to value passed in via constructor
            exitcode = self._exitcode
        finally:
            # write a task finish file
            logutils.write_task_finish_json(outdir=self._outdir,
                                            start_time=self._start_time,
                                            status=exitcode)


        return exitcode
