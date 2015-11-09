def subset_features(record, start, end):
    """ Filters features to include what's in the bounds.

    Because the slice operator on SeqRecord objects does
    not handle features well, we need this function.

    Keyword arguments:
    record -- a SeqRecord object containing features.
    start -- the lower bound to include.
    end -- the upper bound to include.

    returns:
    A list of features.
    """

    new_features = list()
    for feature in record.features:
        f_start = feature.location.start
        f_end = feature.location.end
        if (
                (start <= f_start < end) or
                (start < f_end <= end) or
                ((f_start < start) and (f_end > end))
                ):
            new_features.append(feature)
    return new_features
