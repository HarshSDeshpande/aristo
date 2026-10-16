"""The closed vocabularies of routes/registry.yaml (T0 "names once"). scripts/validate.py checks
every row against them and scripts/generate-routes.py refuses a word outside them. A new word is
an edit here first, reviewed like any vocabulary change."""

PLANES = ('customer', 'admin', 'box', 'platform')
# routes.md §2, F1–F12 by name.
FAMILIES = ('identity', 'setup', 'live', 'mirrors', 'verify', 'picture', 'findings', 'books',
            'campaigns', 'intake', 'tenants', 'shell')
AT = ('repo', 'org_level', 'org_directory', 'org_root', 'admin', 'sign_in')
# Today's `requires` words, verbatim (T2 moves `member` and `formalize`).
RUNGS = ('session', 'member', 'read', 'admin', 'owner', 'operator', 'formalize')
# CAPABILITY-MODEL §2's catalogue (T2: `steer` joins; `author_card` is renamed `campaign_author`).
CAPS = ('read', 'verify', 'steer', 'campaign_author', 'formalize', 'operate', 'stamp')
# A check is one of these, or `cap:<cap>`, or `any_cap:<cap>+<cap>…`.
CHECKS_UNIT = ('person_only', 'repo_admin_bit', 'write_door', 'admin_is_write_door',
               'target_write_door', 'org_image_door', 'admin_or_staff')
# The machine column (T2, CAPABILITY-MODEL §1): ONE capability, or `none` (no machine passes). The
# kind-named arms (`one_org_seat`, `repo_seat`), `admitted` and the `all_of:` / `any_of:` sets are
# not words: a stray arm word fails validation.
MACHINE = CAPS + ('none',)
READS = ('path', 'org', 'entity', 'repo')
CALLERS = ('page', 'seat', 'ops', 'box', 'cli', 'ci')
STATUSES = (404, 410)
METHODS = ('GET', 'POST', 'PUT', 'DELETE', 'PATCH')
# The id's last segment (vyasa REVIEW-T0 §5 rule 1: a closed verb list), then the verbs T0's
# census needed beyond it (named in the T0 spec PR; renamable with the ids).
VERBS = ('list', 'get', 'put', 'create', 'delete', 'start', 'cancel', 'accept', 'sync', 'reset',
         'lock', 'unlock', 'mint', 'revoke', 'retire', 'check', 'launch', 'author', 'finalize',
         'decline', 'stage', 'withdraw', 'report') + (
         'submit', 'match', 'reject', 'complete', 'disclose', 'redrive', 'publish', 'amend',
         'dispose', 'promote', 'hold', 'detect', 'sweep', 'fold', 'explain', 'unpin', 'revert',
         'seed', 'upload', 'receive', 'login', 'redirect')
# The server qualifier `@repo` (rule 2): only the per-repo twins of the org-root setup routes and
# the per-repo whoami.
QUALIFIERS = ('repo',)


def check_ok(word):
    if word.startswith('cap:'):
        return word[4:] in CAPS
    if word.startswith('any_cap:'):
        return all(c in CAPS for c in word[8:].split('+'))
    return word in CHECKS_UNIT


def machine_ok(word):
    return word in MACHINE
