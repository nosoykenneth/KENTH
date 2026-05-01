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
    
    filename = os.path.basename(filepath)
    
    if filepath.endswith(".pdf"):
        loader = PyPDFLoader(filepath)
        documentos = loader.load()

        if not documentos:
            return {"success": False, "message": "El documento está vacío o no se pudo leer."}

        # Limpiar primero en la DB para evitar duplicados si se está resubiendo
        remove_single_document(filepath)

        print("✂️ Cortando texto en fragmentos...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documentos)
        
    elif filepath.endswith(".json"):
        import json
        from langchain_core.documents import Document
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, dict):
            data = [data]
            
        remove_single_document(filepath)
        print("✂️ Extrayendo metadatos y cortando JSON...")
        
        chunks = []
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        for item in data:
            contenido = item.get("contenido", "")
            if not contenido: continue
            
            metadata = {
                "source": filepath,
                "modulo": item.get("modulo", ""),
                "submodulo": item.get("submodulo", ""),
                "tema": item.get("tema", "") or item.get("titulo", ""),
                "recurso_recomendado": item.get("recurso_recomendado", "") or item.get("recurso", ""),
                "url_video": item.get("url_video", "")
            }
            
            # Cortar el contenido y heredar metadatos
            doc_chunks = text_splitter.split_text(contenido)
            for chunk_str in doc_chunks:
                chunks.append(Document(page_content=chunk_str, metadata=metadata))
                
        if not chunks:
            return {"success": False, "message": "El JSON no contiene texto válido en 'contenido'."}
            
    else:
        return {"success": False, "message": "Formato de archivo no soportado."}

    print("🧠 Añadiendo a ChromaDB...")
    db = get_vector_store()
    db.add_documents(chunks)
    
    return {"success": True, "message": f"Documento '{filename}' vectorizado correctamente.", "chunks": len(chunks)}

def remove_single_document(filepath: str):
    """
    Elimina los fragmentos de un documento específico de ChromaDB por su filepath.
    """
    db = get_vector_store()
    
    # Obtenemos la colección subyacente de Chroma para poder borrar por metadata
    collection = db._collection
    
    # Intentar borrar usando rutas directas (windows y linux)
    try:
        collection.delete(where={"source": filepath})
        collection.delete(where={"source": filepath.replace("/", "\\")})
        collection.delete(where={"source": filepath.replace("\\", "/")})
    except Exception as e:
        print(f"Nota al borrar documento (puede no existir previamente): {e}")

    filename = os.path.basename(filepath)
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
    (Versión mejorada del ingest original con subcarpetas)
    """
    archivos = []
    teoria_dir = "./documentos/teoria"
    videos_dir = "./documentos/videos"
    
    if os.path.exists(teoria_dir):
        archivos.extend([os.path.join(teoria_dir, f) for f in os.listdir(teoria_dir) if f.endswith(".pdf")])
    if os.path.exists(videos_dir):
        archivos.extend([os.path.join(videos_dir, f) for f in os.listdir(videos_dir) if f.endswith(".json")])
    
    for filepath in archivos:
        add_single_document(filepath)
        
    return {"success": True, "message": "Todos los documentos han sido sincronizados.", "processed": len(archivos)}