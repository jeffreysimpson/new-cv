#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import json
from operator import itemgetter

import ads
from utf8totex import utf8totex

__all__ = ["get_papers"]


def get_papers(orcid):
    papers = list(ads.SearchQuery(
        orcid=orcid,
        fl=["id", "title", "author", "doi", "year", "pubdate", "pub",
            "volume", "page", "identifier", "doctype", "citation_count",
            "bibcode"],
        max_pages=100,
    ))
    dicts = []
    for paper in papers:
        aid = [":".join(t.split(":")[1:]) for t in paper.identifier
               if t.startswith("arXiv:")]
        for t in paper.identifier:
            if len(t.split(".")) != 2:
                continue
            try:
                list(map(int, t.split(".")))
            except ValueError:
                pass
            else:
                aid.append(t)
        try:
            page = int(paper.page[0])
        except (ValueError, TypeError):
            page = None
            if paper.page is not None and paper.page[0].startswith("arXiv:"):
                aid.append(":".join(paper.page[0].split(":")[1:]))
        dicts.append(dict(
            doctype=paper.doctype,
            authors=list(map(utf8totex, paper.author)),
            year=paper.year,
            pubdate=paper.pubdate,
            doi=paper.doi[0] if paper.doi is not None else None,
            title=utf8totex(paper.title[0]),
            pub=paper.pub,
            volume=paper.volume,
            page=page,
            arxiv=aid[0] if len(aid) else None,
            citations=(paper.citation_count
                       if paper.citation_count is not None else 0),
            url="https://ui.adsabs.harvard.edu/#abs/" + paper.bibcode,
        ))
    return sorted(dicts, key=itemgetter("pubdate"), reverse=True)

    # my_doi_list = ['10.1093/mnras/sty2175',
    #                '10.1093/mnras/sty2171',
    #                '10.1093/mnras/sty2293',
    #                '10.1117/12.2307305',
    #                '10.1093/mnras/sty1281',
    #                '10.1093/mnras/sty865',
    #                '10.1093/mnras/sty847',
    #                '10.1093/mnras/stx2637',
    #                '10.1093/mnras/sty525',
    #                '10.3847/1538-3881/aaa3e4',
    #                '10.1093/mnras/stx2582',
    #                '10.1093/mnras/stx2174'
    #                '10.1093/mnras/stx1892',
    #                '10.1093/mnras/stw2835',
    #                '10.1093/mnras/stw2781',
    #                '10.3847/1538-4365/228/2/24',
    #                '10.1093/mnras/stw2064',
    #                '10.1093/mnras/stw746',
    #                '10.1117/1.JATIS.1.3.035002',
    #                '10.1093/mnras/stv327',
    #                '10.1117/12.2055595',
    #                '10.1093/mnras/stt857',
    #                '10.1111/j.1365-2966.2012.22012.x',
    #                '10.1093/mnrasl/slw073'
    #                ]
if __name__ == "__main__":
    papers = get_papers("0000-0002-8165-2507")
    with open("pubs.json", "w") as f:
        json.dump(papers, f, sort_keys=True, indent=2, separators=(",", ": "))
