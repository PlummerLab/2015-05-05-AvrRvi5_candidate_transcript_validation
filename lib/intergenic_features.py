from Bio.SeqFeature import SeqFeature
from Bio.SeqFeature import FeatureLocation

def intergenic_features(record, start, end, types=["gene"]):
    """ Filters features to get intergenic features between the bounds.
    
    Keyword arguments:
    record -- a SeqRecord object containing features.
    start -- the lower bound to include.
    end -- the upper bound to include.
    
    returns:
    A list of intergenic features.
    """

    new_features = list()
    i = 0
    features = [f for f in record.features if f.type in types]
    while i < len(features):
        this_feature = features[i]
        t_id = this_feature.id
        t_start = this_feature.location.start
        t_end = this_feature.location.end
        
        if i == 0 or len(new_features) == 0:
            last_feature = SeqFeature(id="start", type="gene", location=FeatureLocation(start, start))
            l_id = last_feature.id
            l_start = start
            l_end = start
        else:
            last_feature = record.features[i - 1]
            l_id = last_feature.id
            l_start = last_feature.location.start
            l_end = last_feature.location.end
        
        if ((start < t_start < end) or 
                (start < t_end <= end)):
            new_feature = SeqFeature(
                id=l_id + "-" + t_id,
                type="intergenic",
                location=FeatureLocation(l_end, t_start)
                )
            new_features.append(new_feature)
            if t_end == end:
                break
        elif t_start > end:
            new_feature = SeqFeature(
                id=l_id + "-" + "end",
                type="intergenic",
                location=FeatureLocation(l_end, end)
                )
            new_features.append(new_feature)
            break
        i += 1
    return new_features
