import os
import subprocess

def call_promer(
        reference,
        query,
        mum=False,
        mumreference=True,
        maxmatch=False,
        breaklen=60,
        mincluster=20,
        delta=True,
        diagfactor=0.11,
        extend=True,
        maxgap=30,
        minmatch=6,
        masklen=8,
        coords=False,
        optimize=True,
        prefix="out",
        matrix=1,
        executable='promer'
        ):
    """ Calls promer from MUMmer as a subprocess.

    keyword arguments:
    reference -- Set the input reference multi-FASTA DNA file.
    query -- Set the input query multi-FASTA DNA file.
    mum -- Use anchor matches that are unique in both the reference and query \
        (default False).
    mumreference -- Use anchor matches that are unique in in the reference but \
        not necessarily unique in the query (default True).
    maxmatch -- Use all anchor matches regardless of their uniqueness \
        (default False).
    breaklen -- Set the distance an alignment extension will attempt to extend \
        poor scoring regions before giving up, measured in amino acids \
        (default 60)
    mincluster -- Sets the minimum length of a cluster of matches, measured in \
        amino acids (default 20).
    delta -- Toggle the creation of the delta file (default True).
    diagfactor -- Set the clustering diagonal difference separation factor \
        (default 0.11).
    extend -- Toggle the cluster extension step (default True).
    maxgap -- Set the maximum gap between two adjacent matches in a cluster, \
        measured in amino acids (default 30).
    minmatch -- Set the minimum length of a single match, measured in amino \
        acids (default 6).
    masklen -- Set the maximum bookend masking lenth, measured in amino acids \
        (default 8).
    coords -- Automatically generate the original PROmer1.1 ".coords" output \
        file using the "show-coords" program (default False).
    optimize -- Toggle alignment score optimization, i.e. if an alignment \
        extension reaches the end of a sequence, it will backtrack to optimize \
        the alignment score instead of terminating the alignment at the end of \
        the sequence (default True).
    prefix -- Set the prefix of the output files (default 'out').
    matrix -- Set the alignment matrix number to 1 [BLOSUM 45], 2 [BLOSUM 62] \
        or 3 [BLOSUM 80] (default 2)
    executable -- Absolute path to promer executable, if not in $PATH \
        (default promer).

    returns:
    Tuple of paths to files created.
    """

    command = [executable]

    if mum:
        command.append('--mum')
    if mumreference:
        command.append('--mumreference')
    if maxmatch:
        command.append('--maxmatch')
    if isinstance(breaklen, int) and breaklen > 0:
        command.extend(['--breaklen', str(breaklen)])
    else:
        raise ValueError("Parameter 'breaklen' must be an integer > 0 " +
            "(default 60).")
    if isinstance(mincluster, int) and mincluster > 0:
        command.extend(['--mincluster', str(mincluster)])
    else:
        raise ValueError("Parameter 'mincluster' must be an integer > 0 " +
            "(default 20).")
    if delta:
        command.append("--delta")
        delta_file = prefix+'.delta'
    else:
        delta_file = None
    if isinstance(diagfactor, float):
        command.extend(['--diagfactor', str(diagfactor)])
    else:
        raise ValueError("Parameter 'diagfactor' must be a float " +
            "(default 0.11).")
    if extend:
        command.append("--extend")
    if isinstance(maxgap, int) and maxgap >= 0:
        command.extend(["--maxgap", str(maxgap)])
    else:
        raise ValueError("Parameter 'maxgap' must be an integer >= 0 " +
            "(default 30).")
    if isinstance(minmatch, int) and minmatch > 0:
        command.extend(["--minmatch", str(minmatch)])
    else:
        raise ValueError("Parameter 'minmatch' must be an integer > 0 " +
            "(default 6).")
    if isinstance(masklen, int) and masklen >= 0:
        command.extend(["--masklen", str(masklen)])
    else:
        raise ValueError("Parameter 'masklen' must be an integer >= 0 " +
            "(default 8).")
    if coords:
        command.append("--coords")
        coords_file = prefix + '.coords'
    else:
        coords_file = None
    if optimize:
        command.append("--optimize")
    else:
        command.append("--nooptimize")
    if isinstance(prefix, str):
        command.extend(["--prefix", prefix])
    else:
        raise ValueError("Parameter 'prefix' must be a string (default 'out').")
    if matrix in {1, 2, 3}:
        command.extend(["--matrix", str(matrix)])
    else:
        raise ValueError("Parameter 'matrix' must be one of 1, 2, or 3 " +
            "(default 2)")

    if os.path.isfile(reference):
        command.append(reference)
    else:
        raise ValueError("Parameter 'reference', file could not be found.")
    if os.path.isfile(query):
        command.append(query)
    else:
        raise ValueError("Parameter 'reference', file could not be found.")

    call = ' '.join(command)

    subps = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    nucmer_stdout, nucmer_stderr = subps.communicate()

    print("promer was called as:")
    print(call, "\n")
    if nucmer_stdout not in (None, '', r'', b''):
        print("### Standard output from Nucmer..\n")
        print(nucmer_stdout.decode())
    if nucmer_stderr not in (None, '', r'', b''):
        print("### Standard error from Nucmer..\n")
        print(nucmer_stderr.decode())

    return delta_file, coords_file
