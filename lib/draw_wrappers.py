from gene_shapes import Triangle
from gene_shapes import OpenTriangle

import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.text import Text

def draw_region(
        seq,
        start=None,
        end=None,
        intron_threshold=1000,
        exon=Triangle(width=1),
        intron=OpenTriangle(width=0.5, y_offset=0.5),
        other_shapes=dict(),
        names_to_print=dict(),
        ):
    """

    Keyword arguments:
    names_to_print -- dict.
    """
    if start is None:
        start = 0
    if end is None:
        end = len(seq)
    feature_patches = list()
    text_patches = list()
    for feature in seq[start:end].features:
        if feature.id in names_to_print:
            if 's' not in names_to_print[feature.id]:
                names_to_print[feature.id]['s'] = feature.id
            start = feature.location.start
            end = feature.location.end
            names_to_print[feature.id]['x'] = start + 0.5 * (end - start)
            text_patches.append(names_to_print[feature.id])
        if feature.type == 'CDS' and exon is not None:
            exons = list()
            introns = list()
            reverse = feature.strand == -1
            parts = sorted(feature.location.parts, key=lambda f: min(f.start, f.end), reverse=reverse)
            for i in range(len(parts)):
                strand = parts[i].strand
                # Draw intron if not the last exon
                if i > 0 and intron is not None:
                    if strand in {None, 0, 1}:
                        strand = 1
                        start = parts[i - 1].end
                        distance = (parts[i].start - parts[i - 1].end)
                    else:
                        strand = -1
                        start = parts[i - 1].start
                        distance = (parts[i].end - parts[i - 1].start)
                    if abs(distance) >= intron_threshold:
                        incl_intron = True
                        verts, codes = intron(
                            start,
                            0.,
                            distance
                            )
                        introns.append([start, distance])
                        p = Path(verts, codes)
                        feature_patches.append(
                            patches.PathPatch(
                                p,
                                **intron.properties
                                )
                            )
                    else:
                        incl_intron = False

                # Now draw the exon
                start = parts[i].start
                if strand in {None, 0, 1}:
                    strand = 1
                    start = parts[i].start
                else:
                    strand = -1
                    start = parts[i].end
                distance = (parts[i].end - parts[i].start) * strand

                if len(exons) == 0 or incl_intron:
                    exons.append([start, distance])
                else:  # Join two exons
                    exons[-1][1] += distance

                for e in exons:
                    verts, codes = exon(e[0], 0., e[1])
                    p = Path(verts, codes)
                    feature_patches.append(
                        patches.PathPatch(
                            p,
                            **exon.properties
                            )
                        )

        elif feature.type in other_shapes:
            part = feature.location
            strand = part.strand
            if strand in {None, 0, 1}:
                strand = 1
                start = part.start
            else:
                strand = -1
                start = part.end
            distance = (part.end - part.start) * strand

            verts, codes = other_shapes[feature.type](start, 0., distance)
            p = Path(verts, codes)
            feature_patches.append(
                patches.PathPatch(
                    p,
                    **other_shapes[feature.type].properties
                    )
                )

    return feature_patches, text_patches
