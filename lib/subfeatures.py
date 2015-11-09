from Bio.SeqFeature import SeqFeature
from Bio.SeqFeature import CompoundLocation


def subfeatures(feature):
    """ Return a location object from GFF output.

    The BCBio GFF parser adds exons, mRNA, and CDS's to features as
    sub_features which has since been depreciated in Biopython in favour
    of the CompoundLocation object. This function returns a Location
    object that we can use to extract sequences.

    Keyword arguments:
    feature -- A SeqFeature record with the _sub_features attribute.

    Returns:
    An ExactLocation or CompundLocation object.
    """
    new_features = list()

    if not hasattr(feature, "_sub_features"):
        return [feature]
    if feature._sub_features is None or len(feature._sub_features) == 0:
        return [feature]

    sub_features = feature._sub_features
    feature._sub_features = []
    new_features.append(feature)

    sub_features_cds = [f for f in sub_features if f.type.lower() == 'cds']
    sub_features_exons = [f for f in sub_features if f.type.lower() == 'exon']
    sub_features_mrna = [f for f in sub_features if f.type.lower() == 'mrna']
    sub_features_others = [f for f in sub_features
                           if f.type.lower() not in {'cds', 'exon', 'mrna'}]
    new_features.extend(sub_features_others)

    strand = feature.strand
    if len(sub_features_exons) > 0:
        if len(sub_features_exons) > 1:
            locations = [f.location for f in sub_features_exons]
            locations.sort(key=lambda l: l.start)
            if strand == -1:
                """ When calling CompoundLocation.extract() the sequences are
                extracted in the order that they are encountered. For features on
                the - strand, we need to reverse this order. """
                locations.reverse()
            #print(locations)
            locations = CompoundLocation(locations)
        else:
            # One CDS returns an ExactLocation
            locations = sub_features_exons[0].location
        qualifiers = sub_features_exons[0].qualifiers
        qualifiers.pop("phase", None)
        qualifiers.pop("score", None)
        sub_feature = SeqFeature(
            id=sub_features_exons[0].id,
            type="CDS",
            strand=strand,
            qualifiers=qualifiers,
            location=locations
            )
        new_features.append(sub_feature)

    if len(sub_features_cds) > 0:
        if len(sub_features_cds) > 1:
            locations = [f.location for f in sub_features_cds]
            locations.sort(key=lambda l: l.start)
            if strand == -1:
                locations.reverse()
            locations = CompoundLocation(locations)
        else:
            # One CDS returns an ExactLocation
            locations = sub_features_cds[0].location

        qualifiers = sub_features_cds[0].qualifiers
        qualifiers.pop("phase", None)
        qualifiers.pop("score", None)
        sub_feature = SeqFeature(
            id=sub_features_cds[0].id,
            type="CDS",
            strand=strand,
            qualifiers=qualifiers,
            location=locations
            )
        new_features.append(sub_feature)

    if len(sub_features_mrna) > 0:
        for mrna in sub_features_mrna:
            new_features.extend(subfeatures(mrna))

    return new_features
