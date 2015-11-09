from Bio.SeqFeature import SeqFeature
from Bio.SeqFeature import FeatureLocation
from reportlab.lib import colors
from reportlab.lib.units import cm
"""
colors.Color(red=1/255, green=108/255, blue=154/255) #046C9A
colors.Color(red=255/255, green=0, blue=0) #FF0000
colors.Color(red=0, green=160/255, blue=138/255) #00A08A
colors.Color(red=242/255, green=173/255, blue=0) #F2AD00
colors.Color(red=249/255, green=132/255, blue=0) #F98400
colors.Color(red=91/255, green=188/255, blue=214/255) #5BBCD6
"""

def new_track(plot, record, track_num=1, name=None, start=None, end=None, links=list()):
    """ Shorthand for adding a new track to a plot.
    
    Keyword arguments:
    plot -- A GenomeDiagram.Diagram object
    record -- A SeqRecord object with features
    name -- The label for the track (default record.id)
    start -- Where to start from in the record (default 0)
    end -- Where to end in the record (default len(record))
    
    Returns:
    None the plot object itself is updated.
    """
    
    type_colours = {
        "gene": colors.Color(red=1/255, green=108/255, blue=154/255),
        "mnh120_REPET_SSRs": colors.Color(red=0, green=160/255, blue=138/255),
        "mnh120_REPET_TEs": colors.Color(red=249/255, green=132/255, blue=0)
    }
    if start is None:
        start = 0
    if end is None:
        end = len(record)
    if name is None:
        name = record.id
    
    # set large tick interval
    if end - start > 200000:
        interval = 100000
    elif 80000 < end - start <= 200000:
        interval = 50000
    elif 20000 < end - start <= 80000:
        interval = 10000
    else: 
        interval = 5000
    track = plot.new_track(
        track_num,
        name=name,
        greytrack=False,
        greytrack_labels=1,
        start=start,
        end=end,
        height=0.5,
        scale_fontsize=10,
        scale_largeticks=1.2,
        scale_largetick_interval=interval,
        )
    track_features = track.new_set()
    
    for link, psim in links:       
        colour = colors.Color(red=1, alpha=psim/1000)
        track_features.add_feature(
            SeqFeature(
                id='',
                location=FeatureLocation(
                    link['start'],
                    link['end'],
                    strand=0
                    )
                ),
            color=colour,
            border=colors.Color(red=1, alpha=0.)
            )
   
    for feature in record.features:
        colour = type_colours[feature.type]
        if feature.type == 'gene':
            label_args = {
                'label': True,
                'label_position': 'start',
                'label_angle': 90,
                'label_size': 10,
                'name': feature.id
                }
        else:
            label_args = dict()

        track_features.add_feature(
            feature,
            sigil="BIGARROW",
            arrowshaft_height=1.0,
            color=colour,
            **label_args
            )
    # plot.draw(format="linear", pagesize='A5', fragments=1)
    # plot.write("filename", "PNG")
    return track
