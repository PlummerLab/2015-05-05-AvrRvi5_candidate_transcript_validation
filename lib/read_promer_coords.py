import re

def read_promer_coords(coords_file):
    """ Parse promer coords file.

    Keyword arguments:
    coords_file -- Path to promer output coords file (string, required)

    returns:
    A list of dictionaries with the keys:
        label -- An integer, in ascending order of when they are encountered.
        psim -- % similarity of the alignment (based on the scoring matrix
            that you used in promer).
        pid -- % AA identity in the alignment.
        pstp -- % stop codons in the alignment
        reference -- A dictionary containing the seqid, start position,
            end position, and strand of the alignment for the reference
            sequence provided to promer.
        query -- As with 'reference' but for the promer query sequence.
    """

    start_finder = re.compile(r"=+")
    line_split = re.compile(r"\s+\|\s+|\s+")

    def strand_finder(string):
        if int(string) < 0:
            return '-'
        else:
            return '+'

    links_promer = list()

    with open(coords_file, 'rU') as coords:
        started = False
        for i, line in enumerate(coords):
            if i == 0:
                genomes = line.split()
            line = line.strip()
            if not started:
                if start_finder.match(line) != None:
                    started = True
            else:
                comp = dict()
                line = line_split.split(line)
                comp['label'] = i
                comp['pid'] = float(line[6])  # %identity
                comp['psim'] = float(line[7])  # %similarity
                comp['pstp'] = float(line[8])  # %stop codons
                comp['reference'] = {
                    "start": int(line[0]),
                    "end": int(line[1]),
                    "strand": strand_finder(line[9]),
                    "seqid": line[11]
                    }
                comp['query'] = {
                    "start": int(line[2]),
                    "end": int(line[3]),
                    "strand": strand_finder(line[10]),
                    "seqid": line[12]
                    }
                if comp
                links_promer.append(comp)
    return links_promer
