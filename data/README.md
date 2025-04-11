This directory includes all of the data needed to run the chatbot prototype:

- [`chroma_db/`](./chroma_db/): Vector storage for spec sheet text embeddings with [Chroma](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [`spec_sheets/`](./spec_sheets/): PDFs downloaded from Cree's [indoor lighting catalog](https://www.creelighting.com/products/indoor/)
- [`spec_sheets_text/`](./spec_sheets_text/): `.txt` files containing text extracted from the PDF spec sheets using [pypdf](https://pypdf.readthedocs.io/en/stable/index.html)
- [`product_schema.json`](./product_schema.json): A JSON schema for lighting products intended to be used for structured extraction. A model incorporating this schema is still in the works, so this is not necessary for the current version.