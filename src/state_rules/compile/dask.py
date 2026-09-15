# meant to create more executable forms
from ..rules import Rules



def tasks(rules: Rules):
    from dask.task_spec import Task, DataNode, TaskRef
    #              why none?
    _ = {k: DataNode(None, v) for k,v in rules.state.items()}
    # if not output split
    def order_args(f, argmap):
        from inspect import signature as sig
        _ = sig(f).parameters
        _ = (argmap[p] for p in _)
        _ = map(TaskRef, _)
        _ = tuple(_)
        return _
    #   assuming not split
    _ = _ | \
        {fm.return_statekey: Task(i, fm.f, *order_args(fm.f, fm.argmap) ) for i,fm in enumerate(rules.funcs) }
    
    def split_output(): ...

    return _



def test(rules: Rules):
    ts = tasks(rules)
    #_ = Task(None, f, 3,4 )
    #from dask.distributed import Client
    from dask.threaded import get
    #c = Client(processes=False)
    return get(ts, ['x', 'y', rules.funcs[0].f ] )
    #return c.get(_, 'x' )
    _ = _()
    return _
    #for k,v 