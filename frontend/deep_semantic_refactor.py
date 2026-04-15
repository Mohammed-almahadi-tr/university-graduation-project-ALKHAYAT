"""
Deep Semantic Refactor Script
Reads index.css to build a map of {class_name -> (raw_tailwind_utilities, raw_css)}.
Scans all HTML files, collects unique combinations of those class names,
assigns each combo a new human-readable BEM-style name, rewrites the HTML,
and generates a fresh index.css with @apply using ONLY resolved raw Tailwind utilities.
"""
import os
import re
import glob
from collections import defaultdict

FRONTEND_DIR = r"c:\Users\user\Documents\Graduation Project\university-graduation-project-ALKHAYAT\frontend"
INDEX_CSS_PATH = os.path.join(FRONTEND_DIR, "src", "index.css")

# These are non-CSS library class names — keep them verbatim in HTML
ICON_CLASSES = {'material-icons', 'material-symbols-outlined', 'fas', 'far', 'fab', 'fa'}

# ─── Step 1: Parse index.css into a flat map of className → {utilities, raw_css} ────────────

def parse_css(css_content):
    """
    Returns dict: { class_name: {'utilities': set_of_tw_tokens, 'raw': raw_css_string} }
    Only @apply lines are treated as Tailwind utilities. Raw CSS properties are kept separate.
    """
    class_map = {}

    # Match top-level .class-name { ... } blocks (handles nested braces inside values naively)
    block_re = re.compile(r'\.([a-zA-Z0-9_-]+)\s*\{([^{}]*)\}', re.DOTALL)

    for m in block_re.finditer(css_content):
        name = m.group(1)
        body = m.group(2)

        apply_utils = set()
        raw_lines = []

        for line in body.split('\n'):
            stripped = line.strip()
            if not stripped:
                continue
            apply_m = re.match(r'@apply\s+(.+?)\s*;', stripped)
            if apply_m:
                tokens = apply_m.group(1).split()
                apply_utils.update(tokens)
            else:
                raw_lines.append(stripped)

        class_map[name] = {
            'utilities': apply_utils,
            'raw': '\n'.join(raw_lines)
        }

    return class_map


# ─── Step 2: Resolve a set of old class names → merged set of raw TW utilities + raw CSS ──

def _resolve_token(token, class_map, visited):
    """
    Recursively expands a single token: if it exists in class_map, expand its utilities
    and raw CSS (recursing into any @apply that also references custom classes).
    Returns (set_of_tw_utility_tokens, raw_css_string).
    """
    if token in visited:
        # Circular reference guard — skip
        return set(), ''
    if token not in class_map:
        # It is a true Tailwind utility token — keep as-is
        return {token}, ''

    visited = visited | {token}  # immutable update — don't mutate the caller's set
    entry = class_map[token]
    all_utils = set()
    all_raw = [entry['raw']] if entry['raw'] else []

    for sub_token in entry['utilities']:
        sub_utils, sub_raw = _resolve_token(sub_token, class_map, visited)
        all_utils.update(sub_utils)
        if sub_raw:
            all_raw.append(sub_raw)

    return all_utils, '\n'.join(all_raw)


def resolve_combo(combo, class_map):
    """
    Given a tuple of old class names, fully resolve each one (recursively) and
    return the merged (set_of_tw_utility_tokens, combined_raw_css_string).
    """
    all_utils = set()
    all_raw = []

    for cls in combo:
        utils, raw = _resolve_token(cls, class_map, set())
        all_utils.update(utils)
        if raw:
            all_raw.append(raw)

    return all_utils, '\n'.join(all_raw)


# ─── Step 3: Name generator ────────────────────────────────────────────────────────────────

STRUCTURAL_TAG_NAMES = {
    'nav': 'site-navbar',
    'header': 'page-header',
    'footer': 'site-footer',
    'section': 'content-section',
    'form': 'user-form',
    'main': 'main-content',
    'aside': 'sidebar',
    'article': 'article-block',
    'figure': 'figure-block',
}

HEADING_TAG_NAMES = {
    'h1': 'main-title',
    'h2': 'section-title',
    'h3': 'sub-title',
    'h4': 'sub-heading',
    'h5': 'label-heading',
    'h6': 'micro-heading',
}


def pick_base_name(tags, resolved_utils):
    """Heuristically choose a semantic BEM base name from the element tag + utility hints."""
    tags = set(tags)

    for tag, name in STRUCTURAL_TAG_NAMES.items():
        if tag in tags:
            return name

    for tag, name in HEADING_TAG_NAMES.items():
        if tag in tags:
            return name

    if 'p' in tags:
        return 'paragraph'

    if 'button' in tags:
        return 'btn'

    if 'input' in tags or 'textarea' in tags or 'select' in tags:
        return 'form-input'

    if 'ul' in tags or 'ol' in tags:
        return 'list-group'

    if 'li' in tags:
        return 'list-item'

    if 'a' in tags:
        return 'nav-link'

    if 'img' in tags:
        return 'img-block'

    if 'table' in tags:
        return 'data-table'

    if 'thead' in tags or 'th' in tags:
        return 'table-header'

    if 'td' in tags:
        return 'table-cell'

    if 'label' in tags:
        return 'form-label'

    if 'span' in tags:
        return 'inline-text'

    # div / generic – use utility hints
    if 'grid' in resolved_utils:
        return 'grid-layout'
    if 'flex' in resolved_utils:
        if 'flex-col' in resolved_utils:
            return 'column-layout'
        if 'justify-between' in resolved_utils:
            return 'flex-space-between'
        if 'items-center' in resolved_utils:
            return 'flex-row'
        return 'flex-row'
    if any('max-w' in u for u in resolved_utils):
        return 'container-block'
    if 'absolute' in resolved_utils:
        return 'absolute-element'
    if 'relative' in resolved_utils:
        return 'relative-wrapper'
    if 'fixed' in resolved_utils:
        return 'fixed-element'
    if any('rounded' in u for u in resolved_utils):
        return 'rounded-block'

    return 'ui-block'


# ─── Step 4: Scan HTML files for all class combos ─────────────────────────────────────────

CLASS_ATTR_RE = re.compile(
    r'(<([a-zA-Z][a-zA-Z0-9-]*)(?:[^>]*?)\s)class=(["\'])([^"\']*)\3',
    re.IGNORECASE | re.DOTALL
)


def scan_html_combos(html_files):
    """Returns dict: {combo_tuple -> set_of_tags}"""
    combo_tags = defaultdict(set)

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for m in CLASS_ATTR_RE.finditer(content):
            tag = m.group(2).lower()
            raw_classes = m.group(4).split()
            # Separate icon/library classes from CSS classes
            css_classes = [c for c in raw_classes if c not in ICON_CLASSES]
            icon_classes = [c for c in raw_classes if c in ICON_CLASSES]
            if css_classes:
                combo = tuple(sorted(css_classes))
                combo_tags[combo].add(tag)

    return combo_tags


# ─── Step 5: Assign unique semantic names ─────────────────────────────────────────────────

def assign_names(combo_tags, class_map):
    """
    Returns dict: {combo_tuple -> {'name': str, 'utilities': set, 'raw': str}}
    """
    used_names = {}
    name_counter = defaultdict(int)
    combo_info = {}

    # Sort so structural/semantic combos get priority in naming (smaller combos with known tags first)
    sorted_combos = sorted(combo_tags.items(), key=lambda x: (len(x[1]), len(x[0])), reverse=True)

    SUFFIXES = ['', '-alt', '-variant', '-dark', '-light', '-primary', '-secondary']

    for combo, tags in sorted_combos:
        resolved_utils, resolved_raw = resolve_combo(combo, class_map)
        base = pick_base_name(tags, resolved_utils)

        assigned = None
        for suffix in SUFFIXES:
            candidate = base + suffix
            if candidate not in used_names:
                assigned = candidate
                used_names[candidate] = combo
                break

        if assigned is None:
            # Use numbered suffix
            name_counter[base] += 1
            assigned = f'{base}-custom{name_counter[base]}'
            while assigned in used_names:
                name_counter[base] += 1
                assigned = f'{base}-custom{name_counter[base]}'
            used_names[assigned] = combo

        combo_info[combo] = {
            'name': assigned,
            'utilities': resolved_utils,
            'raw': resolved_raw,
        }

    return combo_info


# ─── Step 6: Rewrite HTML files ───────────────────────────────────────────────────────────

def rewrite_html(html_files, combo_info):
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        def replace_class(m):
            full_prefix = m.group(1)
            tag = m.group(2).lower()
            quote = m.group(3)
            raw_classes = m.group(4).split()

            css_classes = tuple(sorted(c for c in raw_classes if c not in ICON_CLASSES))
            icon_classes = [c for c in raw_classes if c in ICON_CLASSES]

            if not css_classes:
                return m.group(0)

            info = combo_info.get(css_classes)
            if info is None:
                return m.group(0)

            new_classes = [info['name']] + icon_classes
            new_attr = f'class={quote}{" ".join(new_classes)}{quote}'
            # Reconstruct: replace just the class=... part
            original = m.group(0)
            old_attr = f'class={quote}{m.group(4)}{quote}'
            return original.replace(old_attr, new_attr, 1)

        new_content = CLASS_ATTR_RE.sub(replace_class, content)
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)


# ─── Step 7: Generate new index.css ───────────────────────────────────────────────────────

def generate_css(css_content, combo_info):
    """
    Emit a fresh index.css:
    - Tailwind directives
    - :root and any top-level non-layer rules preserved
    - @layer components { one block per combo }
    """
    lines = ['@tailwind base;', '@tailwind components;', '@tailwind utilities;', '']

    # Preserve :root block
    root_m = re.search(r':root\s*\{[^}]+\}', css_content)
    if root_m:
        lines.append(root_m.group(0))
        lines.append('')

    # Preserve pattern-bg (used in other @apply chains)
    pattern_m = re.search(r'\.pattern-bg\s*\{[^}]+\}', css_content)
    if pattern_m:
        lines.append('@layer components {')
        lines.append('  ' + pattern_m.group(0).replace('\n', '\n  '))
        lines.append('}')
        lines.append('')

    lines.append('@layer components {')

    for combo, info in sorted(combo_info.items(), key=lambda x: x[1]['name']):
        name = info['name']
        utils = sorted(info['utilities'])
        raw = info['raw'].strip()

        lines.append(f'  .{name} {{')
        if utils:
            lines.append(f'    @apply {" ".join(utils)};')
        if raw:
            for raw_line in raw.split('\n'):
                if raw_line.strip():
                    lines.append(f'    {raw_line}')
        lines.append('  }')

    lines.append('}')
    return '\n'.join(lines) + '\n'


# ─── Main ──────────────────────────────────────────────────────────────────────────────────

def main():
    print('Reading index.css...')
    with open(INDEX_CSS_PATH, 'r', encoding='utf-8') as f:
        css_content = f.read()

    class_map = parse_css(css_content)
    print(f'  Parsed {len(class_map)} CSS class definitions.')

    html_files = glob.glob(os.path.join(FRONTEND_DIR, '*.html'))
    print(f'Scanning {len(html_files)} HTML files...')

    combo_tags = scan_html_combos(html_files)
    print(f'  Found {len(combo_tags)} unique class combos.')

    print('Assigning semantic names...')
    combo_info = assign_names(combo_tags, class_map)

    print('Rewriting HTML files...')
    rewrite_html(html_files, combo_info)

    print('Generating new index.css...')
    new_css = generate_css(css_content, combo_info)
    with open(INDEX_CSS_PATH, 'w', encoding='utf-8') as f:
        f.write(new_css)

    print('Done! Summary:')
    for combo, info in sorted(combo_info.items(), key=lambda x: x[1]['name']):
        print(f"  .{info['name']:50s}  ← {' '.join(combo)[:80]}")


if __name__ == '__main__':
    main()
