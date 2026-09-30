class strops:
    @classmethod
    def strip(cls, lines):
        _ = lines
        _ = (l for l in _ if l)
        _ = (l.strip() for l in _)
        _ = '\n'.join(_)
        return _
    @classmethod
    def remnl(cls, s: str, sep=''):
        return s.replace('\n',sep)
    
    @classmethod
    def unquote(cls, s: str):
        if not s: return s
        _ = s
        _ = _.strip('"')
        _ = _.strip("'")
        return _
    uq = unquote

    @classmethod
    def reprunquote(cls, o):
        _ = repr(o)
        _ = strops.uq(_)
        return _
    repruq = reprunquote


