import foodlog.models as flm

flm.init_db ('sqlite:///:memory:', verbose=True)
for i, kind in enumerate (flm.session.query (flm.Kind)):
    print ('    {0:2d} {1:s}'.format (i, str (kind)))
