# chatbot_prototype

Natural Language (LLM / Transformer Model) chat application built on Langchain framework with retrieval augmented generation.

RAG is based on the KEGG (Kyoto Encyclopedia of Genes and Genomes) medicus database via Pinecone.io and MedilinePlus via the DuckDuckGoSearch langchain API.

KEGG Medicus database is a knowledge base for systematic analysis of gene functions, linking genomic information with higher-order functional information.

MedlinePlus is an online health information resource for patients and their families and friends. It is a service of the National Library of Medicine (NLM), the world's largest medical library, which is part of the National Institutes of Health (NIH).

To deploy on your local machine.

1. In a python environment, install all the packages in `requirements.txt`
2. Run `python flask-app.py` in the terminal.
3. Change directories into chatbot-ui.
4. In a new terminal run `npm start`.

Additional requirements. 
1. Open AI API key
2. Pinecone Vector Index of Kegg Medicus Database Information

Access to the pincone vecordatabase for application testing can be requested via katlegothobye@yahoo.com
