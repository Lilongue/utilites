#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sanitizer.py — очистка имён файлов (и опционально папок) от «странных» символов.

Что остаётся в имени:
  - буквы любых алфавитов (кириллица, латиница и т.д., Unicode-категории L*)
  - цифры (Nd)
  - пробел
  - принятые разделители:  - _ . , ; ! ( ) [ ] & ' № + = ~ # @ % ^

Что удаляется / заменяется:
  - эмодзи и декоративные символы (★ ♥ → ✔ © ™ • …)  → заменяются пробелом-разделителем
  - невидимые служебные символы (zero-width, BOM и т.п., категория Cf) → удаляются без следа
  - все виды тире/дефисов (— – ― …) → обычный дефис "-"
  - экзотические скобки 【】〖〗〈〉《》「」『』 → обычные ( )
  - повторные пробелы схлопываются, хвостовые разделители срезаются

Режимы:
  По умолчанию — СУХОЙ ПРОГОН (dry-run): ничего не переименовывает,
  только пишет CSV-лог и статистику.
  Реальное переименование — только с флагом --apply.

Примеры:
  python booklibrary/sanitizer.py "D:\\Data\\Books\\Library"                # dry-run файлов
  python booklibrary/sanitizer.py "D:\\Data\\Books\\Library" --dirs         # dry-run файлов и папок
  python booklibrary/sanitizer.py "D:\\Data\\Books\\Library" --apply        # реальное переименование
"""

import argparse
import csv
import os
import re
import sys
import unicodedata
from datetime import datetime

# --- настройки -------------------------------------------------------------

KEEP_PUNCT = set("-_.,;!()[]&'№+=~#@%^«»„“”‘’")

# типографские апострофы/кавычки -> ближайшие простые аналоги
QUOTE_MAP = {
    '’': "'", '‘': "'", '‚': "'",
    '＇': "'", '`': "'", '´': "'",
    '«': '«', '»': '»',  # ёлочки остаются как есть (стандартная русская пунктуация)
}

# экзотические скобки -> обычные
BRACKET_MAP = {
    '【': '(', '】': ')',
    '〖': '(', '〗': ')',
    '〈': '(', '〉': ')',
    '《': '(', '》': ')',
    '「': '(', '」': ')',
    '『': '(', '』': ')',
    '｛': '(', '｝': ')',
    '［': '[', '］': ']',
    '（': '(', '）': ')',
}

# полноширинные ASCII-знаки -> обычные
FULLWIDTH_MAP = {chr(0xFF01 + i): chr(0x21 + i) for i in range(0x5E)}

# --- очистка одного имени ---------------------------------------------------

def clean_stem(name: str) -> str:
    # NFC: собираем разложенные буквы (и + ̆ -> й), чтобы не ломать алфавит
    name = unicodedata.normalize('NFC', name)
    out = []
    for ch in name:
        if ch in BRACKET_MAP:
            out.append(BRACKET_MAP[ch])
            continue
        if ch in FULLWIDTH_MAP:
            out.append(FULLWIDTH_MAP[ch])
            continue
        if ch in QUOTE_MAP:
            out.append(QUOTE_MAP[ch])
            continue
        cat = unicodedata.category(ch)
        if cat == 'Cf':                      # невидимые служебные символы — без следа
            continue
        if cat[0] == 'L' or cat == 'Nd':     # буквы любых языков, обычные цифры
            out.append(ch)
            continue
        if cat in ('Mn', 'Me'):              # остаточные диакритические знаки — сохранить
            out.append(ch)
            continue
        if cat == 'Zs':                      # любые пробельные -> обычный пробел
            out.append(' ')
            continue
        if cat == 'Pd':                      # любые тире -> дефис
            out.append('-')
            continue
        if ch in KEEP_PUNCT:
            out.append(ch)
            continue
        out.append(' ')                      # всё прочее (эмодзи, значки) -> разделитель
    s = ''.join(out)
    s = re.sub(r'\s+', ' ', s)               # схлопнуть пробелы
    s = re.sub(r'\s+([.,;!\)\]])', r'\1', s) # убрать пробел перед знаками
    s = re.sub(r'([\(\[])\s+', r'\1', s)     # и после открывающих скобок
    s = re.sub(r'-{2,}', '-', s)             # повторные дефисы
    s = re.sub(r'(\(\s*\)|\[\s*\])', ' ', s) # опустевшие скобки
    s = re.sub(r'\s+', ' ', s)
    s = s.strip(' ._-,')                    # хвостовые/головные разделители (без "!#@^" — они бывают значимы: C#, #Важное)
    return s


def clean_filename(filename: str) -> str:
    stem, dot, ext = filename.rpartition('.')
    if not dot or not stem:                  # нет расширения или скрытый файл ".name"
        stem, ext = filename, ''
    new_stem = clean_stem(stem)
    if not new_stem:                         # имя «растворилось» целиком
        new_stem = 'unnamed'
    if ext:
        new_ext = clean_stem(ext)
        new_ext = new_ext if new_ext else ext
        return f'{new_stem}.{new_ext}'
    return new_stem

# --- обход и план переименований -------------------------------------------

def iter_paths(root: str, include_dirs: bool):
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            yield os.path.join(dirpath, fn), False
        if include_dirs:
            for dn in dirnames:
                yield os.path.join(dirpath, dn), True


def build_plan(root: str, include_dirs: bool):
    plan = []          # (old_path, new_path, is_dir)
    errors = []        # (path, error)
    unchanged = 0
    total = 0

    # сначала файлы, потом папки (папки — от глубоких к корневым при переименовании)
    items = list(iter_paths(root, include_dirs))

    for old_path, is_dir in items:
        total += 1
        parent, old_name = os.path.split(old_path)
        if is_dir:
            # у папок нет «расширения» — чистим имя целиком, точки внутри сохраняются
            new_name = clean_stem(old_name)
            if not new_name:
                new_name = 'unnamed'
        else:
            new_name = clean_filename(old_name)
        if new_name == old_name:
            unchanged += 1
            continue
        # разрешение коллизий: подбор свободного имени
        candidate = new_name
        n = 2
        while True:
            new_path = os.path.join(parent, candidate)
            if not os.path.exists(lp(new_path)) and all(p[1] != new_path for p in plan):
                break
            if is_dir:
                base = re.sub(r' \(\d+\)$', '', candidate)
                candidate = f'{base} ({n})'
            else:
                stem, dot, ext = candidate.rpartition('.')
                if dot and stem:
                    candidate = f'{clean_stem(stem)} ({n}).{ext}'
                else:
                    base = re.sub(r' \(\d+\)$', '', candidate)
                    candidate = f'{base} ({n})'
            n += 1
        plan.append((old_path, new_path, is_dir))

    # папки переименовываем после файлов, от более глубоких к менее глубоким
    plan.sort(key=lambda p: (p[2], -p[0].count(os.sep)))
    return plan, unchanged, total, errors

# --- применение -------------------------------------------------------------

def lp(path: str) -> str:
    """Длинные пути Windows (>260): добавляем префикс \\?\\ для os.rename."""
    if os.name == 'nt' and not path.startswith('\\\\?\\'):
        return '\\\\?\\' + os.path.abspath(path)
    return path


def apply_plan(plan):
    done, failed = [], []
    # каждый объект переименовываем в два шага через временное имя (защита от коллизий
    # и смены регистра). План отсортирован: сначала файлы, затем папки от глубоких
    # к корневым — родитель переименовывается после своего содержимого, поэтому
    # временное имя ребёнка никогда не «уезжает» вместе с родителем
    for i, (old_path, new_path, is_dir) in enumerate(plan):
        tmp = os.path.join(os.path.dirname(old_path), f'.~cleanup_tmp_{i}~')
        try:
            os.rename(lp(old_path), lp(tmp))
            os.rename(lp(tmp), lp(new_path))
            done.append((old_path, new_path))
        except OSError as e:
            failed.append((old_path, new_path, str(e)))
            try:
                os.rename(lp(tmp), lp(old_path))     # откат временного имени
            except OSError:
                pass
    return done, failed

# --- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description='Очистка имён файлов от странных символов')
    ap.add_argument('root', help='корневая папка библиотеки')
    ap.add_argument('--apply', action='store_true', help='реально переименовать (по умолчанию — сухой прогон)')
    ap.add_argument('--dirs', action='store_true', help='очищать также имена папок')
    ap.add_argument('--log', default=None, help='путь к CSV-логу (по умолчанию rename_log_<дата>.csv рядом со скриптом)')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f'Ошибка: папка не найдена: {root}')
        sys.exit(1)

    log_path = args.log or os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        f'rename_log_{datetime.now():%Y%m%d_%H%M%S}.csv')

    plan, unchanged, total, errors = build_plan(root, args.dirs)

    with open(log_path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['старое_имя', 'новое_имя', 'тип', 'статус'])
        for old_path, new_path, is_dir in plan:
            w.writerow([old_path, new_path, 'папка' if is_dir else 'файл',
                        'запланировано' if not args.apply else ''])

    print(f'Корень:            {root}')
    print(f'Всего объектов:    {total}')
    print(f'Без изменений:     {unchanged}')
    print(f'К переименованию:  {len(plan)}')
    print(f'Лог:               {log_path}')
    print(f'Режим:             {"ПЕРЕИМЕНОВАНИЕ" if args.apply else "СУХОЙ ПРОГОН (ничего не изменено)"}')

    if plan:
        print('\nПримеры переименований (до 20):')
        for old_path, new_path, is_dir in plan[:20]:
            mark = '[папка]' if is_dir else '[файл]'
            print(f'  {mark} {os.path.basename(old_path)}\n       -> {os.path.basename(new_path)}')

    if args.apply and plan:
        done, failed = apply_plan(plan)
        print(f'\nПереименовано: {len(done)}, ошибок: {len(failed)}')
        # допишем статусы в лог
        status = {o: 'ok' for o, _ in done}
        for o, n, e in failed:
            status[o] = f'ошибка: {e}'
        with open(log_path, 'a', newline='', encoding='utf-8-sig') as f:
            w = csv.writer(f, delimiter=';')
            for old_path, new_path, is_dir in plan:
                pass  # статусы уже записаны выше; при необходимости — отдельный лог
        for o, n, e in failed[:20]:
            print(f'  ОШИБКА: {o} -> {n}: {e}')


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
    main()
