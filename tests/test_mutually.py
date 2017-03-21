import trafaret as t
# d = t.Dict({
#         t.Key('ami', optional=True, xor_with='ami_config_key'): t.String(regex='(^ami-[a-z0-9]{8}$|\$\{.+\})'),
#         t.Key('ami_config_key', optional=True, xor_with='ami'): t.String,
#         t.Key('label'): t.String})
# # or

d = t.Dict({
    t.Key('ami', optional=True):
    t.String(regex='(^ami-[a-z0-9]{8}$|\$\{.+\})'),
    t.Key('ami_config_key', optional=True):
    t.String,
    t.Key('label'):
    t.String,
}).mutually_exclusive(* [('ami', 'ami_config_key')])

assert d.check({
    'label': 'kyrylo',
    'ami_config_key': 'the_key'
}) == {
    'label': 'kyrylo',
    'ami_config_key': 'the_key'
}
assert d.check({
    'label': 'kyrylo',
    'ami': 'ami-d2384821'
}) == {
    'label': 'kyrylo',
    'ami': 'ami-d2384821'
}
res = t.extract_error(
    d, {'label': 'pred',
        'ami_config_key': 'the_key',
        'ami': 'ami-d2384821'})
assert res['ami'] == 'ami mutually exclusive with ami_config_key'

d = t.Dict({
    t.Key('ami', optional=True):
    t.String(regex='(^ami-[a-z0-9]{8}$|\$\{.+\})'),
    t.Key('ami_config_key', optional=True):
    t.String,
    t.Key('label'):
    t.String,
}).mutually_exclusive(('ami', 'ami_config_key'))

assert d.check({
    'label': 'kyrylo',
    'ami_config_key': 'the_key'
}) == {
    'label': 'kyrylo',
    'ami_config_key': 'the_key'
}
assert d.check({
    'label': 'kyrylo',
    'ami': 'ami-d2384821'
}) == {
    'label': 'kyrylo',
    'ami': 'ami-d2384821'
}
res = t.extract_error(
    d, {'label': 'pred',
        'ami_config_key': 'the_key',
        'ami': 'ami-d2384821'})
assert res['ami'] == 'ami mutually exclusive with ami_config_key'

d = t.Dict({
    t.Key('ami', optional=True):
    t.String(regex='(^ami-[a-z0-9]{8}$|\$\{.+\})'),
    t.Key('ami_config_key', optional=True):
    t.String,
    t.Key('label'):
    t.String,
}).mutually_exclusive(('label', 'ami', 'ami_config_key'))
res = t.extract_error(
    d, {'label': 'pred',
        'ami_config_key': 'the_key',
        'ami': 'ami-d2384821'})
assert res['label'] == 'label mutually exclusive with ami, ami_config_key'
