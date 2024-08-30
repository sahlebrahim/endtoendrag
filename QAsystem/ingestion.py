from haystack import Pipeline
from haystack.components.writers import DocumentWriter
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack_integrations.document_stores.pinecone import PineconeDocumentStore
from haystack.components.converters import PyPDFToDocument

from pathlib import Path # type: ignore
import os
from dotenv import load_dotenv
from QAsystem.utils import pinecone_config



def ingest(document_store):
    
    #configuring pinecone database
    '''document_store = PineconeDocumentStore(
		environment="gcp-starter",
		index="default",
		namespace="default",
		dimension=768
	)
	'''
    
    
    
    #adding the components in pipeline
    indexing = Pipeline()
    
    indexing.add_component("converter", PyPDFToDocument())
    indexing.add_component("splitter", DocumentSplitter(split_by="sentence", split_length=2))
    indexing.add_component("embedder", SentenceTransformersDocumentEmbedder())
    indexing.add_component("writer", DocumentWriter(document_store))


    indexing.connect("converter","splitter")
    indexing.connect("splitter","embedder")
    indexing.connect("embedder","writer")
    indexing.run({"converter":{"sources":[Path("C:\\Users\\Administrator\\endtoendrag\\data\\RAGpaper.pdf")]}})
if __name__ == "__main__":
    document_store = pinecone_config()
    ingest(document_store)
    