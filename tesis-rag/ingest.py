import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# Usamos la nueva clase de langchain-ollama para los embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def get_vector_store():
    # Inicializa la conexión a Chroma
    return Chroma(persist_directory="./bd_vectorial", embedding_function=embeddings)

def add_single_document(filepath: str):
    """
    Lee un único PDF, lo procesa y lo añade a la base de datos de forma incremental,
    evitando duplicados (borrando previamente si ya existía).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El archivo {filepath} no existe.")

    print(f"📚 Leyendo el documento: {filepath}...")
    loader = PyPDFLoader(filepath)
    documentos = loader.load()

    if not documentos:
        return {"success": False, "message": "El documento está vacío o no se pudo leer."}

    # Limpiar primero en la DB para evitar duplicados si se está resubiendo
    filename = os.path.basename(filepath)
    remove_single_document(filename)

    print("✂️ Cortando texto en fragmentos...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documentos)

    print("🧠 Añadiendo a ChromaDB...")
    db = get_vector_store()
    db.add_documents(chunks)
    
    return {"success": True, "message": f"Documento '{filename}' vectorizado correctamente.", "chunks": len(chunks)}

def remove_single_document(filename: str):
    """
    Elimina los fragmentos de un documento específico de ChromaDB.
    """
    db = get_vector_store()
    source_path = f"documentos\\{filename}" # Langchain suele guardar el metadata source con backslashes en Windows
    source_path_alt = f"./documentos/{filename}"
    
    # Obtenemos la colección subyacente de Chroma para poder borrar por metadata
    collection = db._collection
    
    # Intentar borrar usando ambas rutas comunes
    try:
        collection.delete(where={"source": source_path})
        collection.delete(where={"source": source_path_alt})
    except Exception as e:
        print(f"Nota al borrar documento (puede no existir previamente): {e}")

    return {"success": True, "message": f"Documento '{filename}' eliminado de la IA."}

def get_indexed_documents():
    """
    Consulta la base de datos vectorial para obtener una lista única 
    de los documentos que están actualmente indexados.
    """
    try:
        db = get_vector_store()
        collection = db._collection
        # Obtener un extracto de la colección para ver los metadatos
        result = collection.get(include=["metadatas"])
        
        indexed_files = set()
        if result and "metadatas" in result and result["metadatas"]:
            for meta in result["metadatas"]:
                if meta and "source" in meta:
                    source = meta["source"]
                    # Extraer solo el nombre del archivo
                    filename = os.path.basename(source)
                    indexed_files.add(filename)
                    
        return list(indexed_files)
    except Exception as e:
        print(f"Error consultando documentos indexados: {e}")
        return []

def process_all_documents():
    """
    Sincroniza toda la carpeta asegurando que cada archivo esté indexado.
    (Versión mejorada del ingest original)
    """
    if not os.path.exists("./documentos"):
        return {"success": True, "message": "No hay carpeta de documentos.", "processed": 0}
        
    archivos = [f for f in os.listdir("./documentos") if f.endswith(".pdf")]
    
    for archivo in archivos:
        filepath = os.path.join("./documentos", archivo)
        add_single_document(filepath)
        
    return {"success": True, "message": "Todos los documentos han sido sincronizados.", "processed": len(archivos)}