# Knowledge base: Teacher Agent (Nigeria, JSS1 mathematics)

Official texts, not copies. `sources.json` lists each document with its issuer, official URL and SHA-256. The script downloads them and checks every file:

```bash
python knowledge-base/fetch_sources.py InputDocs
```

It writes `InputDocs/policy/` and `InputDocs/use-case/`, the layout the ITU reference code ingests (`python -m server.knowledge.ingest --reset`). Ingestion was not run for this submission.

## policy/
| File | Issuer | Year |
|---|---|---|
| Nigeria-Data-Protection-Act-2023.pdf | Nigeria Data Protection Act (Act No. 37) | 2023 |
| NDPC-GAID-2025.pdf | NDPC, General Application and Implementation Directive | 2025 |
| National-Digital-Learning-Policy-2023.pdf | Federal Ministry of Education | 2023 |
| National-AI-Strategy-2025.pdf | Ministry of Communications, Innovation and Digital Economy / NITDA | 2025 |
| ICT-in-Education-Policy-2019.pdf, ICT-in-Education-Guidelines-2019.pdf | Federal Ministry of Education | 2019 |
| National-Policy-on-Education-2014.pdf | Federal Ministry of Education (6th ed., 2013, reprint 2014; scanned, 53 MB) | 2014 |
| Child-Rights-Act-2003.pdf | National Human Rights Commission copy | 2003 |
| ITU-AI-Ready-Report-2.0.pdf | ITU | 2026 |

## use-case/
| File | Note |
|---|---|
| NERDC-Mathematics-JSS1-3.pdf | NERDC curriculum, scanned, no year printed; edition unconfirmed |

## Linked, not downloaded
- ITU-T Y.3172: https://www.itu.int/rec/T-REC-Y.3172/en
- UNESCO, Guidance for generative AI in education and research (2023): https://unesdoc.unesco.org/ark:/48223/pf0000386693
- EU AI Act, Regulation (EU) 2024/1689 (non-binding comparison only): https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng
