"""Reconcile local PDF identities, literature hits and existing reading receipts."""

import argparse
from calendar import monthrange
from collections import Counter, defaultdict
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


def load_rows(paths):
    for path in paths:
        rows = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise ValueError(f"Expected an array of objects in {path}")
        yield from rows


def canonical_doi(value):
    value = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value or "").strip(), flags=re.I)
    value = value.lower()
    return value if re.fullmatch(r"10\.\d{4,9}/\S+", value) else ""


def date_status(dates, start, end):
    periods = set()
    for raw in dates:
        match = re.match(r"^(\d{4}(?:-\d{2}(?:-\d{2})?)?)(?:\s|$)", str(raw).strip())
        if not match:
            continue
        parts = [int(part) for part in match[1].split("-")]
        try:
            if len(parts) == 3:
                low = high = date(*parts)
            elif len(parts) == 2:
                year, month = parts
                low, high = date(year, month, 1), date(year, month, monthrange(year, month)[1])
            else:
                low, high = date(parts[0], 1, 1), date(parts[0], 12, 31)
        except ValueError:
            continue
        if low >= start and high <= end:
            periods.add("inside")
        elif high < start or low > end:
            periods.add("outside")
        else:
            periods.add("boundary_unresolved")
    if len(periods) == 1:
        return periods.pop()
    return "date_conflict" if periods else "date_unknown"


def scan_pdfs(roots):
    files, errors = defaultdict(list), []
    seen_paths = set()
    for root in roots:
        root = root.resolve()
        if not root.is_dir():
            errors.append({"path": str(root), "error": "Directory unavailable"})
            continue
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() != ".pdf" or not path.is_file():
                continue
            resolved = path.resolve()
            if resolved in seen_paths:
                continue
            seen_paths.add(resolved)
            try:
                with path.open("rb") as handle:
                    digest = sha256()
                    for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                        digest.update(chunk)
                files[digest.hexdigest()].append({"root": str(root), "path": str(path)})
            except OSError as exc:
                errors.append({"path": str(path), "error": str(exc)})
    return files, errors


def reconcile(args):
    cards = list(load_rows(args.cards))
    inventory = list(load_rows(args.inventory))
    online = list(load_rows(args.online))
    aliases = {}
    for row in load_rows(args.aliases):
        alias, doi = canonical_doi(row.get("alias")), canonical_doi(row.get("doi"))
        if not alias or not doi or alias == doi or aliases.get(alias, doi) != doi:
            raise ValueError("Each DOI alias must map unambiguously to a different DOI")
        aliases[alias] = doi
    if aliases.keys() & aliases.values():
        raise ValueError("DOI aliases must point directly to canonical DOIs")

    def normalize(value):
        doi = canonical_doi(value)
        return aliases.get(doi, doi)

    existing_by_hash, papers, file_rows = defaultdict(list), defaultdict(list), []
    new_reading = defaultdict(list)
    for origin, rows in (("inventory", inventory), ("card", cards), ("online", online)):
        for row in rows:
            doi = normalize(row.get("doi"))
            if doi and row.get("role") != "supplement_candidate":
                papers[doi].append((origin, row))
            if origin != "online" and row.get("sha256"):
                existing_by_hash[row["sha256"]].append((origin, row))
    for receipt in load_rows(args.receipts):
        doi = normalize(receipt.get("doi"))
        if doi not in papers or not receipt.get("scope") or not receipt.get("source"):
            raise ValueError("Reading receipts require a known DOI, scope and source")
        new_reading[doi].append(receipt)

    files, errors = scan_pdfs(args.pdf_root)
    by_doi = defaultdict(list)
    for digest, paths in sorted(files.items()):
        matches = existing_by_hash.get(digest, [])
        is_si = any(row.get("role") == "supplement_candidate" for _, row in matches)
        candidates = {normalize(row.get("doi")) for _, row in matches} - {""}
        verified = {
            normalize(row.get("doi")) for origin, row in matches
            if row.get("doi_status") == "zotero_doi_matches_first_two_pdf_pages"
            or row.get("identity_status") == "verified"
            or origin == "card"
        } - {""}
        doi = next(iter(verified)) if len(verified) == len(candidates) == 1 and not is_si else ""
        status = "supplement" if is_si else "linked_doi" if doi else "identity_pending"
        entry = {
            "sha256": digest, "copies": paths, "status": status,
            "doi": doi or None, "candidate_dois": sorted(candidates),
            "catalog_ids": sorted({str(row["doc_id"]) for _, row in matches if row.get("doc_id")}),
            "versions": sorted({str(row["version"]) for _, row in matches if row.get("version")}),
        }
        file_rows.append(entry)
        if doi:
            by_doi[doi].append(digest)

    paper_rows = []
    for doi, sources in sorted(papers.items()):
        metadata = [row for _, row in sources]
        live = [row for kind, row in sources if kind == "online"]
        online_dates = {str(row["published_online"]) for row in live if row.get("published_online")}
        dates = sorted({str(row["date"]) for row in metadata if row.get("date")} | online_dates)
        receipts = [{
            "card_id": row.get("card_id"), "scope": row.get("read_scope"),
            "read_locators": row.get("read_pages"), "visual_locators": row.get("visually_reviewed_pages"),
        } for kind, row in sources if kind == "card" and row.get("read_scope")]
        selected = live + metadata
        sources_by_url = sorted({str(row["source_url"]) for row in live if row.get("source_url")})
        accessible = {str(row["access"]) for row in live if row.get("access")}
        paper_rows.append({
            "doi": doi,
            "title": next((row["title"] for row in selected if row.get("title")), ""),
            "journal": next((row["journal"] for row in selected if row.get("journal")), ""),
            "dates": dates,
            "published_online_dates": sorted(online_dates),
            "window_status": date_status(online_dates or dates, args.start, args.through),
            "origins": sorted({kind for kind, _ in sources}),
            "local_pdf_hashes": by_doi[doi],
            "online_source_urls": sources_by_url,
            "online_access": sorted(accessible),
            "previous_reading": receipts,
            "new_reading": new_reading[doi],
        })
    return {
        "window": {"from": args.start.isoformat(), "through": args.through.isoformat()},
        "scan_errors": errors,
        "counts": {
            "pdf_copies": sum(len(row["copies"]) for row in file_rows),
            "distinct_pdf_hashes": len(file_rows),
            "file_status": dict(Counter(row["status"] for row in file_rows)),
            "doi_records": len(paper_rows),
            "publication_window": dict(Counter(row["window_status"] for row in paper_rows)),
            "in_window_with_local_pdf": sum(bool(row["local_pdf_hashes"]) and row["window_status"] == "inside" for row in paper_rows),
            "in_window_with_previous_reading": sum(bool(row["previous_reading"]) and row["window_status"] == "inside" for row in paper_rows),
            "online_dois": sum("online" in row["origins"] for row in paper_rows),
            "new_online_dois": sum(row["origins"] == ["online"] for row in paper_rows),
            "doi_records_with_new_reading": sum(bool(row["new_reading"]) for row in paper_rows),
        },
        "files": file_rows,
        "papers": paper_rows,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-root", type=Path, action="append", default=[])
    parser.add_argument("--inventory", type=Path, action="append", default=[])
    parser.add_argument("--cards", type=Path, action="append", default=[])
    parser.add_argument("--online", type=Path, action="append", default=[])
    parser.add_argument("--receipts", type=Path, action="append", default=[])
    parser.add_argument("--aliases", type=Path, action="append", default=[])
    parser.add_argument("--from", dest="start", type=date.fromisoformat, required=True)
    parser.add_argument("--through", type=date.fromisoformat, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Path for a new local JSON snapshot")
    args = parser.parse_args()
    if args.start > args.through:
        parser.error("--from must be on or before --through")
    if not any((args.pdf_root, args.inventory, args.cards, args.online)):
        parser.error("supply at least one input")
    try:
        report = reconcile(args)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(json.dumps(report["counts"], ensure_ascii=False, indent=2))
    return 1 if report["scan_errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
